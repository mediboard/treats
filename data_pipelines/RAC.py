import numpy as np
import concurrent.futures
from multiprocessing import Process, Manager
from cython.parallel import prange
from cython import nogil


MIN_DISTANCE = .24
CLUSTERS = []
NO_DELETED_CLUSTERS = 0

class Cluster:
  def __init__(self, id, ind, neighbors=None, conn_matrix=None):
    self.id = id
    self.will_merge = False
    self.nn = None  # Nearest neighbor
    self.neighbors = neighbors
    self.indices = ind or [] # The indicies in the array - these need to be thread safe, though we can control it
    self.dissimilarities = {}
    self.neighbors_needing_updates = set() 

  def __str__(self):
    return f"Cluster: {self.id}, NN: {self.nn.id if self.nn else None}, indices: {self.indices}"

  def update_dissimilarity(self, other_cluster_id, new_dissimilarity):
    self.dissimilarities[other_cluster_id] = new_dissimilarity

  def get_dissimilarity(self, other_cluster_id):
    return self.dissimilarities[other_cluster_id]

  def update_nn(self):
    if not self.neighbors:
      self.nn = None
      return

    min_dis = min([(self.dissimilarities[x], x) for x in self.neighbors], key=lambda x: x[0])
    self.nn = min_dis[1]
    if min_dis[0] > MIN_DISTANCE:
      self.nn = None


def find_reciprocal_nearest_neighbors():
  merges = []

  if NO_DELETED_CLUSTERS == len(CLUSTERS) - 1:
    return merges

  for cluster in CLUSTERS:
    if not cluster:
      continue

    cluster.will_merge = False
    if cluster.nn != None and CLUSTERS[cluster.nn] != None:
      cluster.will_merge = CLUSTERS[cluster.nn].nn == cluster.id

    if cluster.will_merge and cluster.id < cluster.nn:
      merges.append((cluster.id, cluster.nn))

  return merges


def pairwise_cosine(array_a, array_b):
  norm_a = array_a / np.linalg.norm(array_a, axis=1, keepdims=True)
  norm_b = array_b / np.linalg.norm(array_b, axis=1, keepdims=True)

  return 1 - np.dot(norm_a, norm_b.T)


def calculate_weighted_dissimilarity(points_a, points_b): # These are numpy arrays
  cosines = pairwise_cosine(points_a, points_b)

  return np.mean(cosines)


def merge_cluster(merge, base_arr):
  main_cluster = CLUSTERS[merge[0]]
  secondary_cluster = CLUSTERS[merge[1]]

  new_neighbors = set()
  new_dissimilarities = {}
  needs_updating = set()

  possible_neighbors = [
    c for c in main_cluster.neighbors.union(secondary_cluster.neighbors) if c not in [main_cluster.id, secondary_cluster.id]
  ]

  for other_cluster_id in possible_neighbors:
    other_cluster = CLUSTERS[other_cluster_id]

    if other_cluster.will_merge:
      other_cluster_main = other_cluster if other_cluster.id < other_cluster.nn else CLUSTERS[other_cluster.nn]
      other_cluster_secondary = other_cluster if other_cluster.id > other_cluster.nn else CLUSTERS[other_cluster.nn]

      new_dissimilarity = calculate_weighted_dissimilarity(
        base_arr[main_cluster.indices + secondary_cluster.indices],
        base_arr[other_cluster_main.indices + other_cluster_secondary.indices]
      )

      new_dissimilarities[other_cluster_main.id] = new_dissimilarity
      if new_dissimilarity <= MIN_DISTANCE:
        new_neighbors.add(other_cluster_main.id)

      continue

    new_dissimilarity = calculate_weighted_dissimilarity(
      base_arr[main_cluster.indices + secondary_cluster.indices],
      base_arr[other_cluster.indices]
    )

    new_dissimilarities[other_cluster.id] = new_dissimilarity
    needs_updating.add(other_cluster.id)
    if new_dissimilarity <= MIN_DISTANCE:
      new_neighbors.add(other_cluster.id)

  main_cluster.neighbors = new_neighbors
  main_cluster.dissimilarities = new_dissimilarities
  main_cluster.neighbors_needing_updates = needs_updating


def parallel_merge_clusters(merges, base_arr, num_workers=1):
  with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
    futures = {executor.submit(merge_cluster, merge, base_arr): merge for merge in merges}
    for future in concurrent.futures.as_completed(futures):
      future.result()


def update_cluster_dissimilarities(merges, base_arr):
  # parallel_merge_clusters(merges, base_arr, num_workers=4)
  with nogil:
    for i in prange(len(merges), nogil=True, chunksize=len(merges) // 8):
      merge_cluster(merges[i], base_arr)
  # for merge in merges:
  #   merge_cluster(merge, base_arr)

  needs_update = []
  for main, secondary in merges:
    CLUSTERS[main].indices += CLUSTERS[secondary].indices
    needs_update.append(CLUSTERS[main].neighbors_needing_updates)

  for cluster_id in set.union(*needs_update):
    update_cluster_neighbors(cluster_id)


def update_cluster_neighbors(cluster_id):
  cluster = CLUSTERS[cluster_id]
  for merged_neighbor in [CLUSTERS[c] for c in cluster.neighbors if CLUSTERS[c] and CLUSTERS[c].will_merge]:
    main_neighbor = merged_neighbor if merged_neighbor.id < merged_neighbor.nn else CLUSTERS[merged_neighbor.nn]
    secondary_neighbor = merged_neighbor if merged_neighbor.id > merged_neighbor.nn else CLUSTERS[merged_neighbor.nn]

    dissimilarity = main_neighbor.get_dissimilarity(cluster_id)
    cluster.neighbors.discard(secondary_neighbor.id)
    cluster.neighbors.discard(main_neighbor.id)

    if dissimilarity <= MIN_DISTANCE:
      cluster.neighbors.add(main_neighbor.id)
      cluster.update_dissimilarity(main_neighbor.id, dissimilarity)


def update_nearest_neighbors():
  for cluster in CLUSTERS:
    if cluster == None:
      continue

    if cluster.will_merge or (cluster.nn != None and CLUSTERS[cluster.nn] and CLUSTERS[cluster.nn].will_merge):
      cluster.update_nn()


def calculate_initial_disimilarities(base_arr):
  for cluster in CLUSTERS:
    distance_vec = pairwise_cosine(base_arr, base_arr[cluster.indices]).flatten()
    neighbors = np.where(distance_vec <= MIN_DISTANCE)[0]

    if (len(neighbors) > 1):
      cluster.neighbors = set([n for n in neighbors if n != cluster.id])
      for neighbor in neighbors:
        cluster.dissimilarities[neighbor] = distance_vec[neighbor]

      mask = np.arange(distance_vec.size) != cluster.id
      nearest_neighbor = np.argmin(distance_vec[mask])
      if nearest_neighbor >= cluster.id:
        nearest_neighbor += 1

      cluster.nn = nearest_neighbor


def RAC(X):
  for i in range(X.shape[0]):
    CLUSTERS.append(Cluster(i, [i]))

  calculate_initial_disimilarities(X)

  RAC_r(X)

  indices = [[(ind, cluster.id) for ind in cluster.indices] for cluster in CLUSTERS if cluster != None]

  return [x[1] for x in sorted([item for sublist in indices for item in sublist], key=lambda x: x[0])]


def RAC_r(X):
  merges = find_reciprocal_nearest_neighbors()
  if not merges:
    return

  update_cluster_dissimilarities(merges, X)
  update_nearest_neighbors()

  for _, secondary in merges:
    CLUSTERS[secondary] = None

  return RAC_r(X)


if __name__=='__main__':
  # np.random.seed(43)  # Set the seed for reproducibility

  random_array = np.random.rand(3000, 768)

  labels = RAC(random_array)
  print(len(list(set(labels))))

  from sklearn.cluster import AgglomerativeClustering
  clustering = AgglomerativeClustering(
    n_clusters=None, 
    linkage='average',
    distance_threshold=MIN_DISTANCE, 
    metric='cosine').fit(random_array)
  
  print(len(list(set(clustering.labels_))))
