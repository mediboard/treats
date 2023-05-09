import numpy as np


MIN_DISTANCE = .23 

class Cluster:
  def __init__(self, id, base_arr, ind, neighbors=None, conn_matrix=None):
    self.id = id
    self.will_merge = False
    self.nn = None  # Nearest neighbor
    self.neighbors = neighbors
    self.indices = ind or [] # The indicies in the array - these need to be thread safe, though we can control it
    self.base_arr = base_arr # Need to make sure this is just a reference and not a copy
    self.dissimilarities = {}


  def __str__(self):
    return f"Cluster: {self.id}, NN: {self.nn.id if self.nn else None}, indices: {self.indices}"


  def update_dissimilarity(self, other_cluster, new_dissimilarity):
    self.dissimilarities[other_cluster.id] = new_dissimilarity


  def get_dissimilarity(self, other_cluster):
    return self.dissimilarities[other_cluster.id]


  def get_points(self):
    return self.base_arr[self.indices]


  def update_nn(self):
    if not self.neighbors:
      self.nn = None
      return

    min_dis = min([(self.dissimilarities[x.id], x) for x in self.neighbors], key=lambda x: x[0])
    self.nn = min_dis[1]
    if min_dis[0] > MIN_DISTANCE:
      self.nn = None


def find_reciprocal_nearest_neighbors(clusters):
  merges = []

  if len(clusters) == 1:
    return merges

  for cluster in clusters:
    # if cluster.nn and cluster.nn.nn == None:
    #   print(cluster.nn)

    cluster.will_merge = False
    if cluster.nn:
      cluster.will_merge = cluster.nn.nn.id == cluster.id

  for cluster in clusters:
    if cluster.will_merge and cluster.id < cluster.nn.id:
      merges.append((cluster, cluster.nn))

  return merges


def pairwise_cosine(array_a, array_b):
  norm_a = array_a / np.linalg.norm(array_a, axis=1, keepdims=True)
  norm_b = array_b / np.linalg.norm(array_b, axis=1, keepdims=True)

  return 1 - np.dot(norm_a, norm_b.T)


def calculate_weighted_dissimilarity(points_a, points_b): # These are numpy arrays
  cosines = pairwise_cosine(points_a, points_b)

  return np.mean(cosines)


def merge_cluster(merge, base_arr):
  main_cluster = merge[0]
  secondary_cluster = merge[1]

  new_neighbors = set()

  possible_neighbors = [
    c for c in main_cluster.neighbors.union(secondary_cluster.neighbors) if c.id not in [main_cluster.id, secondary_cluster.id]
  ]

  for other_cluster in possible_neighbors:

    # We need to add this for parallel logic
    if other_cluster.will_merge:
      # You don't need to update the neighbors of the other cluster since it will have it's own loop
      new_dissimilarity = calculate_weighted_dissimilarity(
        base_arr[main_cluster.indices + secondary_cluster.indices],
        base_arr[other_cluster.indices + other_cluster.nn.indices]
      )

      other_cluster_main = other_cluster if other_cluster.id < other_cluster.nn.id else other_cluster.nn

      main_cluster.update_dissimilarity(other_cluster_main, new_dissimilarity)

      if new_dissimilarity <= MIN_DISTANCE:
        new_neighbors.add(other_cluster_main)

      continue

    new_dissimilarity = calculate_weighted_dissimilarity(
      base_arr[main_cluster.indices + secondary_cluster.indices],
      base_arr[other_cluster.indices]
    )

    main_cluster.update_dissimilarity(other_cluster, new_dissimilarity)
    other_cluster.update_dissimilarity(main_cluster, new_dissimilarity)

    other_cluster.neighbors.discard(secondary_cluster)
    if new_dissimilarity > MIN_DISTANCE:
      other_cluster.neighbors.discard(main_cluster)
      continue

    other_cluster.neighbors.add(main_cluster)
    new_neighbors.add(other_cluster)

  # Update the main cluster - remove secondary cluster
  # This should be done after all of the merge calls
  # main_cluster.indices += secondary_cluster.indices
  main_cluster.neighbors = new_neighbors
  # clusters.remove(secondary_cluster)


def update_cluster_dissimilarities(merges, clusters, base_arr):
  for merge in merges:
    merge_cluster(merge, base_arr)

  for main, secondary in merges:
    main.indices += secondary.indices
    clusters.remove(secondary)


def update_nearest_neighbors(clusters):
  for cluster in clusters:
    if cluster.will_merge or (cluster.nn and cluster.nn.will_merge):
      cluster.update_nn()


def calculate_initial_disimilarities(clusters):
  base_arr = clusters[0].base_arr
  for cluster in clusters:
    distance_vec = pairwise_cosine(base_arr, cluster.get_points()).flatten()
    neighbors = np.where(distance_vec <= MIN_DISTANCE)[0]

    if (len(neighbors) > 1):
      cluster.neighbors = set([clusters[n] for n in neighbors if n != cluster.id])
      for neighbor in neighbors:
        cluster.dissimilarities[neighbor] = distance_vec[neighbor]

      mask = np.arange(distance_vec.size) != cluster.id
      nearest_neighbor = np.argmin(distance_vec[mask])
      if nearest_neighbor >= cluster.id:
        nearest_neighbor += 1

      cluster.nn = clusters[nearest_neighbor]


def RAC(X):
  clusters = []
  for i in range(X.shape[0]):
    clusters.append(Cluster(i, X, [i]))

  calculate_initial_disimilarities(clusters)

  clusters = RAC_r(clusters, X)

  indices = [[(ind, cluster.id) for ind in cluster.indices] for cluster in clusters]

  return [x[1] for x in sorted([item for sublist in indices for item in sublist], key=lambda x: x[0])]


def RAC_r(clusters, X):
  merges = find_reciprocal_nearest_neighbors(clusters)
  if not merges:
    return clusters

  update_cluster_dissimilarities(merges, clusters, X)
  update_nearest_neighbors(clusters)

  return RAC_r(clusters, X)


if __name__=='__main__':
  # Let's run through a full test
  # np.random.seed(48)  # Set the seed for reproducibility

  random_array = np.random.rand(1000, 768)
  labels = RAC(random_array)
  print(len(list(set(labels))))

  from sklearn.cluster import AgglomerativeClustering
  clustering = AgglomerativeClustering(
    n_clusters=None, 
    linkage='average',
    distance_threshold=MIN_DISTANCE, 
    metric='cosine').fit(random_array)
  
  print(len(list(set(clustering.labels_))))


