#include <vector>
#include <set>
#include <map>
#include <mutex>
#include <iostream>
#include <future>
#include <algorithm>
#include <Eigen/Dense>
#include <random>

const double MIN_DISTANCE = .035;

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
    std::set<int> neighbors;
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

        this->dissimilarities[this->nn] = 1;
        for (int neighbor : this->neighbors) {
            if (this->dissimilarities[neighbor] < this->dissimilarities[this->nn]) {
                this->nn = neighbor;
            }
        }
    }
};

Eigen::MatrixXd pairwise_cosine(const Eigen::MatrixXd& array_a, const Eigen::MatrixXd& array_b) {
    Eigen::MatrixXd norm_a = array_a.rowwise().normalized();
    Eigen::MatrixXd norm_b = array_b.rowwise().normalized();

    int rows = norm_a.rows();
    int cols = norm_b.rows();

    Eigen::MatrixXd result(rows, cols);

    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            result(i, j) = 1 - norm_a.row(i).dot(norm_b.row(j));
        }
    }

    return result;
}

float calculate_weighted_dissimilarity(Eigen::MatrixXd points_a, Eigen::MatrixXd points_b) {
    Eigen::MatrixXd dissimilarity_matrix = pairwise_cosine(points_a, points_b);

    return static_cast<float>(dissimilarity_matrix.mean());
}

void merge_cluster(std::pair<int, int> merge, Eigen::MatrixXd& base_arr, std::vector<Cluster*>& clusters) {
    Cluster* main_cluster = clusters[merge.first];
    Cluster* secondary_cluster = clusters[merge.second];

    std::set<int> new_neighbors;
    std::map<int, float> new_dissimilarities;
    std::vector<int> needs_updating;

    std::set<int> possible_neighbors;
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
                base_arr.block(main_cluster->indices[0], 0, main_cluster->indices.size() + secondary_cluster->indices.size(), base_arr.cols()),
                base_arr.block(other_cluster_main->indices[0], 0, other_cluster_main->indices.size() + other_cluster_secondary->indices.size(), base_arr.cols())
            );

            new_dissimilarities[other_cluster_main->id] = new_dissimilarity;
            if (new_dissimilarity <= MIN_DISTANCE) {
                new_neighbors.insert(other_cluster_main->id);
            }

            continue;
        }

        float new_dissimilarity = calculate_weighted_dissimilarity(
            base_arr.block(main_cluster->indices[0], 0, main_cluster->indices.size() + secondary_cluster->indices.size(), base_arr.cols()),
            base_arr.block(other_cluster->indices[0], 0, other_cluster->indices.size(), base_arr.cols())
        );

        new_dissimilarities[other_cluster->id] = new_dissimilarity;
        needs_updating.push_back(other_cluster->id);
        if (new_dissimilarity <= MIN_DISTANCE) {
            new_neighbors.insert(other_cluster->id);
        }
    }

    main_cluster->neighbors = new_neighbors;
    main_cluster->dissimilarities = new_dissimilarities;
    main_cluster->neighbors_needing_updates = needs_updating;
}

void update_cluster_neighbors(std::pair<int, int> update_pair, std::vector<Cluster*>& clusters) {
    int main_id = update_pair.first;
    int other_id = update_pair.second;

    Cluster* main_cluster = clusters[main_id];
    Cluster* other_cluster = clusters[other_id];
    int secondary_cluster_id = main_cluster->nn;

    double new_dissimilarity = main_cluster->dissimilarities[other_id];
    other_cluster->dissimilarities[main_id] = new_dissimilarity;

    other_cluster->neighbors.erase(main_id);
    other_cluster->neighbors.erase(secondary_cluster_id);
    if (new_dissimilarity <= MIN_DISTANCE) {
        other_cluster->neighbors.insert(main_id);
    }
}

void update_cluster_dissimilarities(std::vector<std::pair<int, int> >& merges, Eigen::MatrixXd& base_arr, std::vector<Cluster*>& clusters) {
    for (const auto& merge : merges) {
        merge_cluster(merge, base_arr, clusters);
    }

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

    for (const auto& update_pair : needs_update) {
        update_cluster_neighbors(update_pair, clusters);
    }
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
    for (Cluster* cluster : clusters) {
        Eigen::VectorXd distance_vec = pairwise_cosine(base_arr, base_arr.block(cluster->indices[0], 0, cluster->indices.size(), base_arr.cols())).array().abs();

        std::set<int> neighbors;
        std::map<int, float> dissimilarities;
        for (int i = 0; i < distance_vec.size(); ++i) {
            if (distance_vec[i] <= min_distance && i != cluster->id) {
                neighbors.insert(i);
                dissimilarities[i] = distance_vec[i];
            }
        }

        if (neighbors.size() > 0) {
            cluster->neighbors = neighbors;
            cluster->dissimilarities = dissimilarities;

            Eigen::VectorXd masked_distance_vec = distance_vec;
            masked_distance_vec[cluster->id] = std::numeric_limits<float>::max(); // Masking
            auto min_position = std::min_element(masked_distance_vec.data(), masked_distance_vec.data() + masked_distance_vec.size());

            int nearest_neighbor = std::distance(masked_distance_vec.data(), min_position);
            // std::cout  << masked_distance_vec << std::endl;
            // if (nearest_neighbor >= cluster->id) {
            //     nearest_neighbor += 1;
            // }

            cluster->nn = nearest_neighbor;
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

    update_cluster_nn(clusters);

    remove_secondary_clusters(merges, clusters);

    return RAC_r(base_arr, clusters);
}

std::vector<int> RAC(Eigen::MatrixXd& base_arr) {
    std::vector<Cluster*> clusters;
    for (int i = 0; i < base_arr.rows(); ++i) {
        Cluster* cluster = new Cluster(i);
        clusters.push_back(cluster);
    }

    calculate_initial_disimilarities(base_arr, clusters, MIN_DISTANCE);

    RAC_r(base_arr, clusters);

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
    int no_points = 10;
    Eigen::MatrixXd test = generateRandomMatrix(no_points, 768, 12);

    // Shift and scale the values to the range 0-1
    test = (test + Eigen::MatrixXd::Constant(no_points, 768, 1.)) / 2.;


    // std::cout << test << std::endl;

    std::vector<int> labels = RAC(test);

    // Output number of clusters
    std::set<int> unique_labels(labels.begin(), labels.end());
    std::cout << unique_labels.size() << std::endl;
}
