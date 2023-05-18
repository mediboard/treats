#include <unordered_set>
#include <chrono>
#include <vector>
#include <set>
#include <map>
#include <mutex>
#include <iostream>
#include <thread>
#include <algorithm>
#include <Eigen/Dense>
#include <random>

const double MIN_DISTANCE = .035;

int NO_COSINE_CALLS = 0;
int NO_CORES = 8;

// Store update neighbor times
std::vector<long> UPDATE_NEIGHBOR_DURATIONS;

// Store update NN times
std::vector<long> UPDATE_NN_DURATIONS;

// Store the durations of each call to cosine
std::vector<long> COSINE_DURATIONS;
std::vector<long> INDICES_DURATIONS;
std::vector<long> MERGE_DURATIONS;

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

class Cluster {
public:
    int id;
    bool will_merge;
    int nn;
    std::unordered_set<int> neighbors;
    std::vector<int> indices;
    std::map<int, float> dissimilarities;
    std::vector<int> neighbors_needing_updates;

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
};

Eigen::MatrixXd pairwise_cosine(const Eigen::MatrixXd& array_a, const Eigen::MatrixXd& array_b) {
    // Transpose and normalize the columns
    Eigen::MatrixXd norm_a = array_a.colwise().normalized();
    Eigen::MatrixXd norm_b = array_b.colwise().normalized();

    return Eigen::MatrixXd::Ones(norm_a.cols(), norm_b.cols()) - (norm_a.transpose() * norm_b);
}

float calculate_weighted_dissimilarity(Eigen::MatrixXd points_a, Eigen::MatrixXd points_b) {
    Eigen::MatrixXd dissimilarity_matrix = pairwise_cosine(points_a, points_b);

    return static_cast<float>(dissimilarity_matrix.mean());
}

void merge_cluster(std::pair<int, int>& merge, Eigen::MatrixXd& base_arr, std::vector<Cluster*>& clusters) {
    Cluster* main_cluster = clusters[merge.first];
    Cluster* secondary_cluster = clusters[merge.second];

    std::vector<int> new_neighbors;
    std::map<int, float> new_dissimilarities;
    std::vector<int> needs_updating;

    std::unordered_set<int> possible_neighbors;
    for (auto& id : main_cluster->neighbors) {
        if (id != main_cluster->id && id != secondary_cluster->id) {
            possible_neighbors.insert(id);
        }
    }
    for (auto& id : secondary_cluster->neighbors) {
        if (id != main_cluster->id && id != secondary_cluster->id) {
            possible_neighbors.insert(id);
        }
    }

    for (auto& other_cluster_id : possible_neighbors) {
        Cluster* other_cluster = clusters[other_cluster_id];

        if (other_cluster->will_merge) {
            Cluster* other_cluster_main = other_cluster->id < other_cluster->nn ? other_cluster : clusters[other_cluster->nn];
            Cluster* other_cluster_secondary = other_cluster->id > other_cluster->nn ? other_cluster : clusters[other_cluster->nn];

            float new_dissimilarity = calculate_weighted_dissimilarity(
                base_arr.block(0, main_cluster->indices[0], base_arr.rows(), main_cluster->indices.size() + secondary_cluster->indices.size()),
                base_arr.block(0, other_cluster_main->indices[0], base_arr.rows(), other_cluster_main->indices.size() + other_cluster_secondary->indices.size())
            );

            new_dissimilarities[other_cluster_main->id] = new_dissimilarity;
            if (new_dissimilarity <= MIN_DISTANCE) {
                new_neighbors.push_back(other_cluster_main->id);
            }

            continue;
        }

        float new_dissimilarity = calculate_weighted_dissimilarity(
            base_arr.block(0, main_cluster->indices[0], base_arr.rows(), main_cluster->indices.size() + secondary_cluster->indices.size()),
            base_arr.block(0, other_cluster->indices[0], base_arr.rows(), other_cluster->indices.size())
        );

        new_dissimilarities[other_cluster->id] = new_dissimilarity;
        needs_updating.push_back(other_cluster->id);
        if (new_dissimilarity <= MIN_DISTANCE) {
            new_neighbors.push_back(other_cluster->id);
        }
    }

    std::unordered_set<int> neighbor_set(new_neighbors.begin(), new_neighbors.end());

    main_cluster->neighbors = neighbor_set;
    main_cluster->dissimilarities = new_dissimilarities;
    main_cluster->neighbors_needing_updates = needs_updating;
}

void merge_clusters(std::vector<std::pair<int, int> >& merges, Eigen::MatrixXd& base_arr, std::vector<Cluster*>& clusters) {
    for (std::pair<int, int> merge : merges) {
        merge_cluster(merge, base_arr, clusters);
    }
}

void parallel_merge_clusters(
    std::vector<std::pair<int, int> >& merges, 
    Eigen::MatrixXd& base_arr, 
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
        std::thread merge_thread = std::thread(merge_clusters, std::ref(merge_chunks[i]), std::ref(base_arr), std::ref(clusters));
        threads.push_back(std::move(merge_thread));
    }

    for (int i=0; i<no_threads; i++) {
        threads[i].join();
    }
}

void update_cluster_neighbors(std::pair<int, int>& update_pair, std::vector<Cluster*>& clusters) {
    int main_id = update_pair.first;
    int other_id = update_pair.second;

    Cluster* main_cluster = clusters[main_id];
    Cluster* other_cluster = clusters[other_id];
    int secondary_cluster_id = main_cluster->nn;

    double new_dissimilarity = main_cluster->dissimilarities[other_id];

    other_cluster->neighbors.erase(secondary_cluster_id);
    if (new_dissimilarity <= MIN_DISTANCE) {
        other_cluster->dissimilarities[main_id] = new_dissimilarity;
        other_cluster->neighbors.insert(main_id);
    } else {
        other_cluster->neighbors.erase(main_id);
    }
}

void update_cluster_dissimilarities(std::vector<std::pair<int, int> >& merges, Eigen::MatrixXd& base_arr, std::vector<Cluster*>& clusters) {
    auto start = std::chrono::high_resolution_clock::now();
    if (merges.size() / NO_CORES > 10) {
        parallel_merge_clusters(merges, base_arr, clusters, NO_CORES);
    } else {
        for (std::pair<int, int> merge : merges) {
            merge_cluster(merge, base_arr, clusters);
        }
    }
    auto end = std::chrono::high_resolution_clock::now();
    MERGE_DURATIONS.push_back(std::chrono::duration_cast<std::chrono::microseconds>(end - start).count());

    start = std::chrono::high_resolution_clock::now();
    std::vector< std::pair<int, int> > needs_update;
    for (const auto& merge : merges) {
        int main = merge.first;
        int secondary = merge.second;

        clusters[main]->indices.insert(clusters[main]->indices.end(), clusters[secondary]->indices.begin(), clusters[secondary]->indices.end());

        for (int i=0; i < clusters[main]->neighbors_needing_updates.size(); i++) {
            std::pair<int, int> update_pair = std::make_pair(main, clusters[main]->neighbors_needing_updates[i]);
            needs_update.push_back(update_pair);
        }
    }
    end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    INDICES_DURATIONS.push_back(duration.count());

    // start times
    start = std::chrono::high_resolution_clock::now();
    for (std::pair<int, int>& update_pair : needs_update) {
        update_cluster_neighbors(update_pair, clusters);
    }
    end = std::chrono::high_resolution_clock::now();

    duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    UPDATE_NEIGHBOR_DURATIONS.push_back(duration.count()); 

}

void update_cluster_nn(std::vector<Cluster*>& clusters) {
    for (Cluster* cluster : clusters) {
        if (cluster == nullptr) {
            continue;
        }

        if (cluster->will_merge || (cluster->nn != -1 and clusters[cluster->nn] != nullptr and clusters[cluster->nn]->will_merge)) {
            cluster->update_nn();
        }
    }
}

void calculate_initial_disimilarities(Eigen::MatrixXd& base_arr, std::vector<Cluster*>& clusters, float min_distance) {
    // Compute the batch size
    int batchSize = 1000;  // Adjust this to fit in memory

    for (int batchStart = 0; batchStart < clusters.size(); batchStart += batchSize) {
        int batchEnd = std::min(batchStart + batchSize, static_cast<int>(clusters.size()));

        // Create a block view of the clusters in the current batch
        Eigen::MatrixXd batch = base_arr.block(0, clusters[batchStart]->indices[0], base_arr.rows(), clusters[batchEnd - 1]->indices[0] - clusters[batchStart]->indices[0] + 1);

        // Compute the pairwise cosine dissimilarity
        Eigen::MatrixXd distance_mat = pairwise_cosine(base_arr, batch).array().abs();

        for (int i = batchStart; i < batchEnd; ++i) {
            Cluster* cluster = clusters[i];
            Eigen::VectorXd distance_vec = distance_mat.col(i - batchStart);

            std::unordered_set<int> neighbors;
            std::map<int, float> dissimilarities;
            for (int j = 0; j < distance_vec.size(); ++j) {
                if (distance_vec[j] <= min_distance && j != cluster->id) {
                    neighbors.insert(j);
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

void RAC_r(Eigen::MatrixXd& base_arr, std::vector<Cluster*>& clusters) {
    std::vector<std::pair<int, int> > merges = find_reciprocal_nn(clusters);
    if (merges.size() == 0) {
        return;
    }

    update_cluster_dissimilarities(merges, base_arr, clusters);

    auto start_time = std::chrono::high_resolution_clock::now();
    update_cluster_nn(clusters);
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time);

    UPDATE_NN_DURATIONS.push_back(duration.count());

    remove_secondary_clusters(merges, clusters);

    return RAC_r(base_arr, clusters);
}

std::vector<int> RAC(Eigen::MatrixXd& base_arr) {
    // Transpose bare array for column access
    Eigen::MatrixXd new_base_arr = base_arr.transpose();

    std::vector<Cluster*> clusters;
    for (int i = 0; i < new_base_arr.cols(); ++i) {
        Cluster* cluster = new Cluster(i);
        clusters.push_back(cluster);
    }

    calculate_initial_disimilarities(new_base_arr, clusters, MIN_DISTANCE);

    RAC_r(new_base_arr, clusters);

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
    int no_points = 10000;
    Eigen::MatrixXd test = generateRandomMatrix(no_points, 768, 10);

    // Shift and scale the values to the range 0-1
    test = (test + Eigen::MatrixXd::Constant(no_points, 768, 1.)) / 2.;


    // std::cout << test << std::endl;

    // Start timer
    auto start = std::chrono::high_resolution_clock::now();
    std::vector<int> labels = RAC(test);
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
