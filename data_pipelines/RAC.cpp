#include <array>
#include <tuple>
#include <unordered_map>
#include <set>
#include <chrono>
#include <vector>
#include <map>
#include <iostream>
#include <thread>
#include <algorithm>
// #define EIGEN_DONT_PARALLELIZE
#include <Eigen/Dense>
#include <Eigen/Sparse>
#include <random>


const double MIN_DISTANCE = .035;
const int NO_POINTS = 10000;

int NO_COSINE_CALLS = 0;
const int NO_CORES = 8;

// Store update neighbor times
std::vector<long> UPDATE_NEIGHBOR_DURATIONS;

// Store update NN times
std::vector<long> UPDATE_NN_DURATIONS;

// Store the durations of each call to cosine
std::vector<long> COSINE_DURATIONS;
std::vector<long> INDICES_DURATIONS;
std::vector<long> MERGE_DURATIONS;
std::vector<long> MISC_MERGE_DURATIONS;

std::array<std::array<int, NO_POINTS>, NO_CORES> MERGING_ARRAYS;

// Function to generate a matrix filled with random numbers.
Eigen::MatrixXd generateRandomMatrix(int rows, int cols, int seed) {
    std::default_random_engine generator(seed);
    std::uniform_real_distribution<double> distribution(0.0,1.0);

    Eigen::MatrixXd mat(rows, cols);
    for(int i=0; i<mat.rows(); ++i) {
        for(int j=0; j<mat.cols(); ++j) {
            mat(i, j) = distribution(generator);
        }
    }

    return mat;
}

double get_arr_value(Eigen::MatrixXd& arr, int i, int j) {
    if (i > j) {
        return arr(j, i);
    }
    return arr(i, j);
}

void set_arr_value(Eigen::MatrixXd& arr, int i, int j, double value) {
    if (i > j) {
        arr(j, i) = value;
        return;
    }
    arr(i, j) = value;
}

class Cluster {
public:
    int id;
    bool will_merge;
    int nn;
    std::vector<int> neighbors;
    std::vector<int> indices;
    std::unordered_map<int, float> dissimilarities;
    std::vector<std::tuple<int, int, double> > neighbors_needing_updates;

    Cluster(int id)
        : id(id), will_merge(false) {
            std::vector<int> indices;
            indices.push_back(id);
            this->indices = indices;

            this->nn = -1;
        }


    void update_nn() {
        if (neighbors.size() == 0) {
            nn = -1;
            return;
        }

        float min = 1;
        int nn = -1;
        for (int neighbor : this->neighbors) {
            float dissimilarity = this->dissimilarities[neighbor];
            if (dissimilarity < min) {
                min = dissimilarity;
                nn = neighbor;
            }
        }

        this->nn = nn;
    }

    void update_nn(Eigen::MatrixXd& distance_arr) {
        if (neighbors.size() == 0) {
            nn = -1;
            return;
        }

        double min = 1;
        int nn = -1;
        for (int neighbor : this->neighbors) {
            float dissimilarity = distance_arr(this->id, neighbor);
            if (dissimilarity < min) {
                min = dissimilarity;
                nn = neighbor;
            }
        }

        this->nn = nn;
    }
};

Eigen::MatrixXd pairwise_cosine(const Eigen::MatrixXd& array_a, const Eigen::MatrixXd& array_b) {
    return Eigen::MatrixXd::Ones(array_a.cols(), array_b.cols()) - (array_a.transpose() * array_b);
}

float calculate_weighted_dissimilarity(Eigen::MatrixXd points_a, Eigen::MatrixXd points_b) {
    Eigen::MatrixXd dissimilarity_matrix = pairwise_cosine(points_a, points_b);

    return static_cast<float>(dissimilarity_matrix.mean());
}

void merge_cluster_apx(
    std::pair<int, int>& merge,
    std::vector<Cluster*>& clusters,
    std::array<int, NO_POINTS>& merging_array,
    Eigen::MatrixXd& distance_arr) {

    Cluster* main_cluster = clusters[merge.first];
    Cluster* secondary_cluster = clusters[merge.second];

    std::vector<int> new_neighbors;

    std::vector<int> static_neighbors;
    static_neighbors.reserve(main_cluster->neighbors.size() + secondary_cluster->neighbors.size());

    std::vector<int> merging_neighbors;
    merging_neighbors.reserve(main_cluster->neighbors.size() + secondary_cluster->neighbors.size());

    for (auto& id : main_cluster->neighbors) {
        if (id != main_cluster->id && id != secondary_cluster->id) {
            int smallest_id = id < clusters[id]->nn ? id : clusters[id]->nn;
            if (clusters[id]->will_merge) {
                if (merging_array[smallest_id] != 1) {
                    merging_array[smallest_id] = 1;
                    merging_neighbors.push_back(smallest_id);
                }
            } else {
                merging_array[id] = 1;
                static_neighbors.push_back(id);
            }
        }
    }

    for (auto& id : secondary_cluster->neighbors) {
        if (id != main_cluster->id && id != secondary_cluster->id) {
            int smallest_id = id < clusters[id]->nn ? id : clusters[id]->nn;

            if (clusters[id]->will_merge) {
                if (merging_array[smallest_id] == 0) {
                    merging_array[smallest_id] = 1;
                    merging_neighbors.push_back(smallest_id);
                }
            } else {
                if (merging_array[id] == 0) {
                    static_neighbors.push_back(id);
                }

                ++merging_array[id];
            }
        }
    }

    std::vector<std::tuple<int, int, double> > needs_update;
    for (auto& static_id : static_neighbors) {
        double primary_dist = distance_arr(main_cluster->id, static_id);
        double secondary_dist = distance_arr(secondary_cluster->id, static_id);

        double avg_dist = (main_cluster->indices.size() * primary_dist + secondary_cluster->indices.size() * secondary_dist) / (main_cluster->indices.size() + secondary_cluster->indices.size());

        distance_arr(main_cluster->id, static_id) = avg_dist;
        if (avg_dist <= MIN_DISTANCE) {
            new_neighbors.push_back(static_id);
        }

        needs_update.push_back(std::make_tuple(main_cluster->id, static_id, avg_dist));

        merging_array[static_id] = 0;
    }

    for (auto& merging_id : merging_neighbors) {
        double main_primary_dist = distance_arr(main_cluster->id, merging_id); 
        double main_secondary_dist = distance_arr(secondary_cluster->id, merging_id);
        double main_avg_dist = (main_cluster->indices.size() * main_primary_dist + secondary_cluster->indices.size() * main_secondary_dist) / (main_cluster->indices.size() + secondary_cluster->indices.size());

        int secondary_merging_id = clusters[merging_id]->nn;
        double secondary_primary_dist = distance_arr(main_cluster->id, secondary_merging_id);
        double secondary_secondary_dist = distance_arr(secondary_cluster->id, secondary_merging_id);
        double secondary_avg_dist = (main_cluster->indices.size() * secondary_primary_dist + secondary_cluster->indices.size() * secondary_secondary_dist) / (main_cluster->indices.size() + secondary_cluster->indices.size());

        double avg_dist = (clusters[merging_id]->indices.size() * main_avg_dist + clusters[secondary_merging_id]->indices.size() * secondary_avg_dist) / (clusters[merging_id]->indices.size() + clusters[secondary_merging_id]->indices.size());

        if (avg_dist <= MIN_DISTANCE) {
            distance_arr(main_cluster->id, merging_id) = avg_dist;
            new_neighbors.push_back(merging_id);
        }

        merging_array[merging_id] = 0;
    }

    main_cluster->neighbors = new_neighbors;
    main_cluster->neighbors_needing_updates = needs_update;
}

void merge_cluster_apx(
    std::pair<int, int>& merge,
    std::vector<Cluster*>& clusters,
    std::array<int, NO_POINTS>& merging_array) {

    Cluster* main_cluster = clusters[merge.first];
    Cluster* secondary_cluster = clusters[merge.second];

    std::vector<int> new_neighbors;

    std::unordered_map<int, float> new_dissimilarities;
    new_dissimilarities.reserve(main_cluster->dissimilarities.size() + secondary_cluster->dissimilarities.size());

    std::vector<int> static_neighbors;
    static_neighbors.reserve(main_cluster->neighbors.size() + secondary_cluster->neighbors.size());

    std::vector<int> merging_neighbors;
    merging_neighbors.reserve(main_cluster->neighbors.size() + secondary_cluster->neighbors.size());

    for (auto& id : main_cluster->neighbors) {
        if (id != main_cluster->id && id != secondary_cluster->id) {
            int smallest_id = id < clusters[id]->nn ? id : clusters[id]->nn;
            if (clusters[id]->will_merge) {
                if (merging_array[smallest_id] != 1) {
                    merging_array[smallest_id] = 1;
                    merging_neighbors.push_back(smallest_id);
                }
            } else {
                merging_array[id] = 1;
                static_neighbors.push_back(id);
            }
        }
    }

    for (auto& id : secondary_cluster->neighbors) {
        if (id != main_cluster->id && id != secondary_cluster->id) {
            int smallest_id = id < clusters[id]->nn ? id : clusters[id]->nn;

            if (clusters[id]->will_merge) {
                if (merging_array[smallest_id] == 0) {
                    merging_array[smallest_id] = 1;
                    merging_neighbors.push_back(smallest_id);
                }
            } else {
                if (merging_array[id] == 0) {
                    static_neighbors.push_back(id);
                }

                ++merging_array[id];
            }
        }
    }

    std::vector<std::tuple<int, int, double> > needs_update;
    for (auto& static_id : static_neighbors) {
        if (merging_array[static_id] > 1) {
            float primary_dist = main_cluster->dissimilarities[static_id]; 
            float secondary_dist = secondary_cluster->dissimilarities[static_id];

            float avg_dist = (main_cluster->indices.size() * primary_dist + secondary_cluster->indices.size() * secondary_dist) / (main_cluster->indices.size() + secondary_cluster->indices.size());

            if (avg_dist <= MIN_DISTANCE) {
                new_dissimilarities[static_id] = avg_dist;
                new_neighbors.push_back(static_id);
            }

            needs_update.push_back(std::make_tuple(main_cluster->id, static_id, avg_dist));
        }

        merging_array[static_id] = 0;
    }

    for (auto& merging_id : merging_neighbors) {
        if (merging_array[merging_id] > 3) {
            // Merging neighbors have the distance here
            float main_primary_dist = main_cluster->dissimilarities[merging_id]; 
            float main_secondary_dist = secondary_cluster->dissimilarities[merging_id];
            float main_avg_dist = (main_cluster->indices.size() * main_primary_dist + secondary_cluster->indices.size() * main_secondary_dist) / (main_cluster->indices.size() + secondary_cluster->indices.size());

            int secondary_merging_id = clusters[merging_id]->nn;
            float secondary_primary_dist = main_cluster->dissimilarities[secondary_merging_id];
            float secondary_secondary_dist = secondary_cluster->dissimilarities[secondary_merging_id];
            float secondary_avg_dist = (main_cluster->indices.size() * secondary_primary_dist + secondary_cluster->indices.size() * secondary_secondary_dist) / (main_cluster->indices.size() + secondary_cluster->indices.size());

            float avg_dist = (clusters[merging_id]->indices.size() * main_avg_dist + clusters[secondary_merging_id]->indices.size() * secondary_avg_dist) / (clusters[merging_id]->indices.size() + clusters[secondary_merging_id]->indices.size());

            if (avg_dist <= MIN_DISTANCE) {
                new_neighbors.push_back(merging_id);
                new_dissimilarities[merging_id] = avg_dist;
            }

        } 

        merging_array[merging_id] = 0;
    }

    main_cluster->neighbors = new_neighbors;
    main_cluster->dissimilarities = new_dissimilarities;
    main_cluster->neighbors_needing_updates = needs_update;
}

void merge_clusters(
    std::vector<std::pair<int, int> >& merges,
    std::vector<Cluster*>& clusters,
    std::array<int, NO_POINTS>& merging_array) {
    for (std::pair<int, int> merge : merges) {
        merge_cluster_apx(merge, clusters, merging_array);
    }
}

void merge_clusters_dist(
    std::vector<std::pair<int, int> >& merges,
    std::vector<Cluster*>& clusters,
    std::array<int, NO_POINTS>& merging_array,
    Eigen::MatrixXd& distance_arr) {
    for (std::pair<int, int> merge : merges) {
        merge_cluster_apx(merge, clusters, merging_array, distance_arr);
    }
}

void parallel_merge_clusters(
    std::vector<std::pair<int, int> >& merges, 
    std::vector<Cluster*>& clusters,
    int no_threads) {

    std::vector<std::thread> threads;

    std::vector<std::vector<std::pair<int, int>>> merge_chunks(no_threads);

    int chunk_size = merges.size() / no_threads;
    int remainder = merges.size() % no_threads; 

    int start = 0, end = 0;
    for (int i = 0; i < no_threads; i++) {
        end = start + chunk_size;
        if (i < remainder) { // distribute the remainder among the first "remainder" chunks
            end++;
        }

        // Create chunks by using the range constructor of std::vector
        if (end <= merges.size()) {
            merge_chunks[i] = std::vector<std::pair<int, int>>(merges.begin() + start, merges.begin() + end);
        }

        start = end;
    }

    for (int i=0; i<no_threads; i++) {
        std::thread merge_thread = std::thread(
            merge_clusters,
            std::ref(merge_chunks[i]),
            std::ref(clusters),
            std::ref(MERGING_ARRAYS[i]));

        threads.push_back(std::move(merge_thread));
    }

    for (int i=0; i<no_threads; i++) {
        threads[i].join();
    }
}

void parallel_merge_clusters(
    std::vector<std::pair<int, int> >& merges,
    Eigen::MatrixXd& distance_arr,
    std::vector<Cluster*>& clusters,
    int no_threads) {

    std::vector<std::thread> threads;

    std::vector<std::vector<std::pair<int, int>>> merge_chunks(no_threads);

    int chunk_size = merges.size() / no_threads;
    int remainder = merges.size() % no_threads; 

    int start = 0, end = 0;
    for (int i = 0; i < no_threads; i++) {
        end = start + chunk_size;
        if (i < remainder) { // distribute the remainder among the first "remainder" chunks
            end++;
        }

        // Create chunks by using the range constructor of std::vector
        if (end <= merges.size()) {
            merge_chunks[i] = std::vector<std::pair<int, int>>(merges.begin() + start, merges.begin() + end);
        }

        start = end;
    }

    for (int i=0; i<no_threads; i++) {
        std::thread merge_thread = std::thread(
            merge_clusters_dist,
            std::ref(merge_chunks[i]),
            std::ref(clusters),
            std::ref(MERGING_ARRAYS[i]),
            std::ref(distance_arr));

        threads.push_back(std::move(merge_thread));
    }

    for (int i=0; i<no_threads; i++) {
        threads[i].join();
    }
}

std::array<int, NO_POINTS> UPDATE_NEIGHBORS;
void update_cluster_neighbors(std::pair<int, std::vector<std::pair<int, double> > >& update_chunk, std::vector<Cluster*>& clusters) {
    Cluster* other_cluster = clusters[update_chunk.first];

    std::vector<int> new_neighbors;
    std::vector<int> all_looped_neighbors;
    for (int i=0; i<update_chunk.second.size(); i++) {
        int neighbor_id = update_chunk.second[i].first;
        int neighbor_nn_id = clusters[neighbor_id]->nn;
        double dissimilarity = update_chunk.second[i].second;

        UPDATE_NEIGHBORS[neighbor_id] = 1;
        UPDATE_NEIGHBORS[neighbor_nn_id] = -1;

        if (dissimilarity <= MIN_DISTANCE) {
            other_cluster->dissimilarities[neighbor_id] = dissimilarity;
            new_neighbors.push_back(neighbor_id);
        } 

        all_looped_neighbors.push_back(neighbor_id);
        all_looped_neighbors.push_back(neighbor_nn_id);
    }

    for (int i=0; i<other_cluster->neighbors.size(); i++) {
        int neighbor_id = other_cluster->neighbors[i];
        if (UPDATE_NEIGHBORS[neighbor_id] == 0) {
            new_neighbors.push_back(neighbor_id);
        }
        all_looped_neighbors.push_back(neighbor_id);
    }

    // Clear array and find NN
    for (int i=0; i<all_looped_neighbors.size(); i++) {
        UPDATE_NEIGHBORS[all_looped_neighbors[i]] = 0;
    }

    other_cluster->neighbors = new_neighbors;
}

void update_cluster_neighbors(
    std::pair<int, std::vector<std::pair<int, double> > >& update_chunk,
    std::vector<Cluster*>& clusters,
    Eigen::MatrixXd& distance_arr) {
    Cluster* other_cluster = clusters[update_chunk.first];

    std::vector<int> new_neighbors;
    std::vector<int> all_looped_neighbors;
    for (int i=0; i<update_chunk.second.size(); i++) {
        int neighbor_id = update_chunk.second[i].first;
        int neighbor_nn_id = clusters[neighbor_id]->nn;
        double dissimilarity = update_chunk.second[i].second;
        

        UPDATE_NEIGHBORS[neighbor_id] = 1;
        UPDATE_NEIGHBORS[neighbor_nn_id] = -1;

        distance_arr(other_cluster->id, neighbor_id) = dissimilarity;
        if (dissimilarity <= MIN_DISTANCE) {
            new_neighbors.push_back(neighbor_id);
        } 

        all_looped_neighbors.push_back(neighbor_id);
        all_looped_neighbors.push_back(neighbor_nn_id);
    }

    for (int i=0; i<other_cluster->neighbors.size(); i++) {
        int neighbor_id = other_cluster->neighbors[i];
        if (UPDATE_NEIGHBORS[neighbor_id] == 0) {
            new_neighbors.push_back(neighbor_id);
        }
        all_looped_neighbors.push_back(neighbor_id);
    }

    // Clear array and find NN
    for (int i=0; i<all_looped_neighbors.size(); i++) {
        UPDATE_NEIGHBORS[all_looped_neighbors[i]] = 0;
    }

    other_cluster->neighbors = new_neighbors;
}

// void update_cluster_neighbors_p(std::vector<std::pair<int, int> >& updates, std::vector<Cluster*>& clusters) {
//     for (std::pair<int, int> update_pair : updates) {
//         update_cluster_neighbors(update_pair, clusters);
//     }
// }   

// void parallel_update_clusters(std::vector<std::pair<int, int> >& updates, std::vector<Cluster*>& clusters, int no_threads) {
//     std::vector<std::thread> threads;

//     std::vector<std::vector<std::pair<int, int>>> update_chunks(no_threads);

//     int chunk_size = updates.size() / no_threads;
//     int remainder = updates.size() % no_threads; 

//     int start = 0, end = 0;
//     for (int i = 0; i < no_threads; i++) {
//         end = start + chunk_size;
//         if (i < remainder) { // distribute the remainder among the first "remainder" chunks
//             end++;
//         }

//         if (end <= updates.size()) {
//             update_chunks[i] = std::vector<std::pair<int, int>>(updates.begin() + start, updates.begin() + end);
//         }
//         start = end;
//     }

//     for (int i=0; i<no_threads; i++) {
//         std::thread update_thread = std::thread(update_cluster_neighbors_p, std::ref(update_chunks[i]), std::ref(clusters));
//         threads.push_back(std::move(update_thread));
//     }

//     for (int i=0; i<no_threads; i++) {
//         threads[i].join();
//     }
// }

std::array<std::pair<int, std::vector<std::pair<int, double> > >, NO_POINTS> SORT_NEIGHBOR;
void update_cluster_dissimilarities(std::vector<std::pair<int, int> >& merges, std::vector<Cluster*>& clusters) {
    auto start = std::chrono::high_resolution_clock::now();
    if (merges.size() / NO_CORES > 10) {
        parallel_merge_clusters(merges, clusters, NO_CORES);
    } else {
        for (std::pair<int, int> merge : merges) {
            merge_cluster_apx(merge, clusters, MERGING_ARRAYS[0]);
        }
    }
    auto end = std::chrono::high_resolution_clock::now();
    MERGE_DURATIONS.push_back(std::chrono::duration_cast<std::chrono::microseconds>(end - start).count());

    for (const auto& merge : merges) {
        int main = merge.first;
        int secondary = merge.second;

        clusters[main]->indices.insert(clusters[main]->indices.end(), clusters[secondary]->indices.begin(), clusters[secondary]->indices.end());

        for (int i=0; i < clusters[main]->neighbors_needing_updates.size(); i++) {
            int neighbor_idx = std::get<1>(clusters[main]->neighbors_needing_updates[i]);
            double dissimilarity = std::get<2>(clusters[main]->neighbors_needing_updates[i]);

            SORT_NEIGHBOR[neighbor_idx].first = neighbor_idx;
            SORT_NEIGHBOR[neighbor_idx].second.push_back(std::make_pair(main, dissimilarity));
        }
    }

    for (int i=0; i<SORT_NEIGHBOR.size(); i++) {
        if (SORT_NEIGHBOR[i].second.size() > 0) {
            update_cluster_neighbors(SORT_NEIGHBOR[i], clusters);
            SORT_NEIGHBOR[i].second.clear();
        }
    }
}

void update_cluster_dissimilarities(
    std::vector<std::pair<int, int> >& merges,
    std::vector<Cluster*>& clusters,
    Eigen::MatrixXd& distance_arr) {

    if (merges.size() / NO_CORES > 10) {
        parallel_merge_clusters(merges, distance_arr, clusters, NO_CORES);
    } else {
        for (std::pair<int, int> merge : merges) {
            merge_cluster_apx(merge, clusters, MERGING_ARRAYS[0], distance_arr);
        }
    }

    for (const auto& merge : merges) {
        int main = merge.first;
        int secondary = merge.second;

        clusters[main]->indices.insert(clusters[main]->indices.end(), clusters[secondary]->indices.begin(), clusters[secondary]->indices.end());

        for (int i=0; i < clusters[main]->neighbors_needing_updates.size(); i++) {
            int neighbor_idx = std::get<1>(clusters[main]->neighbors_needing_updates[i]);
            double dissimilarity = std::get<2>(clusters[main]->neighbors_needing_updates[i]);

            SORT_NEIGHBOR[neighbor_idx].first = neighbor_idx;
            SORT_NEIGHBOR[neighbor_idx].second.push_back(std::make_pair(main, dissimilarity));
        }
    }

    for (int i=0; i<SORT_NEIGHBOR.size(); i++) {
        if (SORT_NEIGHBOR[i].second.size() > 0) {
            update_cluster_neighbors(SORT_NEIGHBOR[i], clusters, distance_arr);
            SORT_NEIGHBOR[i].second.clear();
        }
    }
}

void update_cluster_nn(
    std::vector<Cluster*>& clusters,
    Eigen::MatrixXd& distance_arr) {
    for (Cluster* cluster : clusters) {
        if (cluster == nullptr) {
            continue;
        }

        if (cluster->will_merge || (cluster->nn != -1 and clusters[cluster->nn] != nullptr and clusters[cluster->nn]->will_merge)) {
            if (distance_arr.size() == 0) {
                cluster->update_nn();
            } else {
                cluster->update_nn(distance_arr);
            }
        }
    }
}

std::vector<std::pair<int, int> > find_reciprocal_nn(std::vector<Cluster*>& clusters) {
    std::vector<std::pair<int, int> > reciprocal_nn;

    for (Cluster* cluster : clusters) {
        if (cluster == nullptr) {
            continue;
        }

        if (cluster->nn != -1 && clusters[cluster->nn] != nullptr) {
            cluster->will_merge = (clusters[cluster->nn]->nn == cluster->id);
        }

        if (cluster -> will_merge && cluster->id < cluster->nn) {
            reciprocal_nn.push_back(std::make_pair(cluster->id, cluster->nn));
        }
    }

    return reciprocal_nn;
}

void remove_secondary_clusters(std::vector<std::pair<int, int> >& merges, std::vector<Cluster*>& clusters) {
    for (const auto& merge : merges) {
        int secondary_id = merge.second;
        clusters[secondary_id] = nullptr;
    }
}

void RAC_i(std::vector<Cluster*>& clusters, float min_distance, Eigen::MatrixXd& distance_arr) {
    while (true) {
        std::vector<std::pair<int, int>> merges = find_reciprocal_nn(clusters);
        if (merges.size() == 0) {
            break;
        }

        if (distance_arr.size() != 0) {
            update_cluster_dissimilarities(merges, clusters, distance_arr);
        } else {
            update_cluster_dissimilarities(merges, clusters);
        }

        update_cluster_nn(clusters, distance_arr);

        remove_secondary_clusters(merges, clusters);
    }
}

Eigen::MatrixXd calculate_initial_dissimilarities(
    Eigen::MatrixXd& base_arr,
    std::vector<Cluster*>& clusters,
    float min_distance) {
    Eigen::MatrixXd distance_mat = pairwise_cosine(base_arr, base_arr).array();

    for (int i=0; i<clusters.size(); i++) {
        double min = 2;
        int nn = -1;

        for (int j=0; j<clusters.size(); j++) {
            if (i == j) {
                distance_mat(i, j) = 2;
                continue;
            }

            double distance = distance_mat(i, j);
            if (distance <= min_distance) {
                clusters[i]->neighbors.push_back(j);

                if (distance < min) {
                    min = distance;
                    nn = j;
                }
            }
        }

        clusters[i] -> nn = nn;
    }

    return distance_mat;
}

void calculate_initial_dissimilarities(
    Eigen::MatrixXd& base_arr,
    std::vector<Cluster*>& clusters,
    float min_distance,
    Eigen::SparseMatrix<bool>& connectivity) {
    // Compute the batch size
    int batchSize = 1000;  // Adjust this to fit in memory

    for (int batchStart = 0; batchStart < clusters.size(); batchStart += batchSize) {
        int batchEnd = std::min(batchStart + batchSize, static_cast<int>(clusters.size()));

        // Create a block view of the clusters in the current batch
        Eigen::MatrixXd batch = base_arr.block(0, clusters[batchStart]->indices[0], base_arr.rows(), clusters[batchEnd - 1]->indices[0] - clusters[batchStart]->indices[0] + 1);

        // Compute the pairwise cosine dissimilarity
        Eigen::MatrixXd distance_mat = pairwise_cosine(base_arr, batch).array();
        for (int i = batchStart; i < batchEnd; ++i) {
            Cluster* cluster = clusters[i];
            Eigen::VectorXd distance_vec = distance_mat.col(i - batchStart);

            std::vector<int> neighbors;
            std::unordered_map<int, float> dissimilarities;
            for (int j = 0; j < distance_vec.size(); ++j) {
                // Check connectivity matrix before adding neighbor
                if (distance_vec[j] <= min_distance && j != cluster->id && connectivity.coeff(cluster->id, j)) {
                    neighbors.push_back(j);
                    dissimilarities[j] = distance_vec[j];
                }
            }

            if (!neighbors.empty()) {
                cluster->neighbors = neighbors;
                cluster->dissimilarities = dissimilarities;

                distance_vec[cluster->id] = std::numeric_limits<float>::max(); // Masking
                auto min_position = std::min_element(distance_vec.data(), distance_vec.data() + distance_vec.size());

                int nearest_neighbor = std::distance(distance_vec.data(), min_position);
                cluster->nn = nearest_neighbor;
            }
        }
    }
}


std::vector<int> RAC(Eigen::MatrixXd& base_arr, float min_distance, Eigen::SparseMatrix<bool>& connectivity) {
    // Eigen::setNbThreads(8);
    // Transpose bare array for column access
    base_arr = base_arr.transpose().colwise().normalized().eval();

    std::vector<Cluster*> clusters;
    for (int i = 0; i < base_arr.cols(); ++i) {
        Cluster* cluster = new Cluster(i);
        clusters.push_back(cluster);
    }
    Eigen::setNbThreads(8);
    Eigen::MatrixXd distance_arr;

    if (connectivity.size() != 0) {
        calculate_initial_dissimilarities(base_arr, clusters, min_distance, connectivity);
    } else {
        distance_arr = calculate_initial_dissimilarities(base_arr, clusters, min_distance);
    }

    RAC_i(clusters, min_distance, distance_arr);

    Eigen::setNbThreads(8);
    std::vector<std::pair<int, int> > cluster_idx;
    for (Cluster* cluster : clusters) {
        if (cluster == nullptr) {
            continue;
        }

        for (int index : cluster->indices)  {
            cluster_idx.push_back(std::make_pair(index, cluster->id));
        }
    }

    std::sort(cluster_idx.begin(), cluster_idx.end());

    std::vector<int> cluster_labels;
    for (const auto& [index, cluster_id] : cluster_idx) {
        cluster_labels.push_back(cluster_id);
    }

    return cluster_labels;
}

int main() {
    // 5000 - 1061
    Eigen::MatrixXd test = generateRandomMatrix(NO_POINTS, 768, 10);

    // Shift and scale the values to the range 0-1
    test = (test + Eigen::MatrixXd::Constant(NO_POINTS, 768, 1.)) / 2.;


    // std::cout << test << std::endl;

    // Start timer
    auto start = std::chrono::high_resolution_clock::now();
    Eigen::SparseMatrix<bool> connectivity;
    std::vector<int> labels = RAC(test, MIN_DISTANCE, connectivity);
    // Stop timer
    auto stop = std::chrono::high_resolution_clock::now();

    // Compute the duration
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(stop - start);

    // Output duration
    std::cout << duration.count() << std::endl;

    // Output neighbor update durations
    std::cout << std::accumulate(UPDATE_NEIGHBOR_DURATIONS.begin(), UPDATE_NEIGHBOR_DURATIONS.end(), 0.0) / 1000 << std::endl;

    // Output NN update durations
    std::cout << std::accumulate(UPDATE_NN_DURATIONS.begin(), UPDATE_NN_DURATIONS.end(), 0.0) / 1000 << std::endl;

    // Output indices durations
    std::cout << std::accumulate(INDICES_DURATIONS.begin(), INDICES_DURATIONS.end(), 0.0) / 1000 << std::endl;

    // Output merge durations
    std::cout << std::accumulate(MERGE_DURATIONS.begin(), MERGE_DURATIONS.end(), 0.0) / 1000 << std::endl;

    // Output misc merge durations
    std::cout << std::accumulate(MISC_MERGE_DURATIONS.begin(), MISC_MERGE_DURATIONS.end(), 0.0) / 1000 << std::endl;

    // Output number of clusters
    std::set<int> unique_labels(labels.begin(), labels.end());
    std::cout << unique_labels.size() << std::endl;

    // Output number of cosine calls
    // std::cout << NO_COSINE_CALLS << std::endl;

    // Output max cosine duration
    // std::cout << std::max_element(COSINE_DURATIONS.begin(), COSINE_DURATIONS.end())[0] << std::endl;

    // // Output total cosine duration
    // std::cout << std::accumulate(COSINE_DURATIONS.begin(), COSINE_DURATIONS.end(), 0.0) / 1000 << std::endl;

    // // Output average cosine duration
    // std::cout << std::accumulate(COSINE_DURATIONS.begin(), COSINE_DURATIONS.end(), 0.0) / COSINE_DURATIONS.size() << std::endl;
}
