import numpy as np

## TODO
# Add in a connectity matrix to determin NN
# Dissimilarity functions
# Make parts of the function parallel
# Where is the nearest neighbor calculated?


MIN_DISTANCE = .23 

# Assuming a Cluster class with attributes/methods mentioned in the paper
# Where are the points?? We need to map back to them eventually
class Cluster:
  def __init__(self, id, base_arr, ind, neighbors=None, conn_matrix=None):
    self.id = id
    self.will_merge = False
    self.nn = None  # Nearest neighbor
    self.neighbors = neighbors
    self.indices = ind or [] # The indicies in the array - these need to be thread safe, though we can control it
    self.base_arr = base_arr # Need to make sure this is just a reference and not a copy

    # How do we store the disimilarities between neighbors? 
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
  """
  Find and return the reciprocal nearest neighbors among the given clusters.

  :param clusters: List of Cluster objects
  :return: List of tuples, each containing a pair of reciprocal nearest neighbors
  """
  merges = []

  if len(clusters) == 1:
    return merges

  for cluster in clusters:
    if cluster.nn and cluster.nn.nn == None:
      print(cluster.nn)

    cluster.will_merge = False
    if cluster.nn:
      cluster.will_merge = cluster.nn.nn.id == cluster.id

  # Find the reciprocal nearest neighbors and add them to the merge list
  for cluster in clusters:
    if cluster.will_merge and cluster.id < cluster.nn.id:
      merges.append((cluster, cluster.nn))

  return merges


def pairwise_cosine(array_a, array_b):
  # Normalise both arrays

  norm_a = array_a / np.linalg.norm(array_a, axis=1, keepdims=True)
  norm_b = array_b / np.linalg.norm(array_b, axis=1, keepdims=True)

  return 1 - np.dot(norm_a, norm_b.T)


def calculate_weighted_dissimilarity(points_a, points_b): # These are numpy arrays
  # We'll ignore the heavy memory requirements for now
  cosines = pairwise_cosine(points_a, points_b)

  return np.mean(cosines)


def merge_cluster(merge, clusters, base_arr):
  main_cluster = merge[0] if merge[0].id < merge[1].id else merge[1]
  secondary_cluster = merge[1] if merge[0].id < merge[1].id else merge[0]

  new_neighbors = set()

  # Look at all the neighbors - minus themselves
  possible_neighbors = [c for c in main_cluster.neighbors.union(secondary_cluster.neighbors) if c.id not in [main_cluster.id, secondary_cluster.id]]
  for other_cluster in possible_neighbors:
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
  main_cluster.indices += secondary_cluster.indices
  main_cluster.neighbors = new_neighbors
  clusters.remove(secondary_cluster)


def update_cluster_dissimilarities(merges, clusters, base_arr):
  for merge in merges:
    merge_cluster(merge, clusters, base_arr)


# Or do the merge right before this step so we don't have to do weird fetches
# This does seem to affect parallelization
# def update_cluster_dissimilarities(clusters, base_arr):
#   for cluster in [c for c in clusters if c.will_merge and c.id < c.nn.id]:
#     new_neighbors = set()

#     for other_cluster in cluster.neighbors.union(cluster.nn.neighbors):

#       if other_cluster.will_merge and other_cluster.id != cluster.id:
#         new_dissimilarity = calculate_weighted_dissimilarity(
#           base_arr[cluster.indices + cluster.nn.indices], 
#           base_arr[other_cluster.indices + other_cluster.nn.indices]
#         )

#         cluster.update_dissimilarity(other_cluster, new_dissimilarity)
#         other_cluster.update_dissimilarity(cluster, new_dissimilarity)

#         other_cluster.neighbors.discard(cluster.nn)
#         if new_dissimilarity > MIN_DISTANCE:
#           other_cluster.neighbors.discard(cluster)
#           continue

#         other_cluster.neighbors.add(cluster)

#         new_neighbors.add(other_cluster)

#       elif not other_cluster.will_merge and other_cluster.id != cluster.id:
#         new_dissimilarity = calculate_weighted_dissimilarity(
#           base_arr[cluster.indices + cluster.nn.indices],
#           base_arr[other_cluster.indices]
#         )

#         cluster.update_dissimilarity(other_cluster, new_dissimilarity)
#         other_cluster.update_dissimilarity(cluster, new_dissimilarity)

#         other_cluster.neighbors.discard(cluster.nn)
#         if new_dissimilarity > MIN_DISTANCE:
#           other_cluster.neighbors.discard(cluster)
#           continue

#         other_cluster.neighbors.add(cluster)

#         new_neighbors.add(other_cluster)

#     cluster.neighbors = new_neighbors

#   for cluster in [c for c in clusters if c.will_merge and c.id > c.nn.id]:
#     clusters.remove(cluster) 
#     cluster.nn.indices += cluster.indices 


def update_nearest_neighbors(clusters):
  for cluster in clusters:
    if cluster.will_merge or (cluster.nn and cluster.nn.will_merge):
      cluster.update_nn()


def calculate_initial_disimilarities(clusters):
  # We can't just do a pairwise distance matrix for the whole thing
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
      if nearest_neighbor > cluster.id:
        nearest_neighbor += 1

      cluster.nn = clusters[nearest_neighbor]


def RAC(X):
  clusters = []
  for i in range(X.shape[0]):
    clusters.append(Cluster(i, random_array, [i]))

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
  # np.random.seed(49)  # Set the seed for reproducibility

  random_array = np.random.rand(500, 768)
  labels = RAC(random_array)
  print(len(list(set(labels))))

  from sklearn.cluster import AgglomerativeClustering
  clustering = AgglomerativeClustering(
    n_clusters=None, 
    linkage='average',
    distance_threshold=MIN_DISTANCE, 
    metric='cosine').fit(random_array)
  
  print(len(list(set(clustering.labels_))))

