import boto3
import pickle
from io import BytesIO
from botocore.exceptions import NoCredentialsError
import umap
import numpy as np
import os

# Read the credentials from the environment
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

def load_embeddings(bucket_name, object_name):
  s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

  try:
    # Create an in-memory binary stream to store the downloaded object
    in_memory_file = BytesIO()

    # Download the object from S3 into the in-memory binary stream
    s3.download_fileobj(bucket_name, object_name, in_memory_file)
    in_memory_file.seek(0)  # Reset file pointer to the beginning

    # Load the numpy array from the in-memory binary stream using pickle
    np_array = pickle.load(in_memory_file)

    return np_array

  except NoCredentialsError:
    print('Credentials not available')

    return None


def reduce_dimensions(embeddings):
  # Use UMAP to reduce the dimensions of 
  reducer = umap.UMAP(n_components=5, n_neighbors=15, min_dist=.25, metric='cosine', n_jobs=-1)

  embeddings_umap = reducer.fit_transform(embeddings)

  return embeddings_umap


def save_result(umap_embeddings, object_name, bucket_name):
  # Save the result to an S3 bucket
  s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

  try:
    # Create an in-memory binary stream and save the numpy array to it using pickle
    in_memory_file = BytesIO()
    pickle.dump(umap_embeddings, in_memory_file)
    in_memory_file.seek(0)  # Reset file pointer to the beginning
    
    # Upload the in-memory binary stream to S3
    s3.upload_fileobj(in_memory_file, bucket_name, object_name)
    print(f'Successfully uploaded {object_name} to {bucket_name}')

    return True

  except NoCredentialsError:
    print('Credentials not available')

    return False


def dim_reduction_workflow():
  bucket_name = 'medboard-data'
  file_path = 'embeddings/embeddings_np_2.pkl'
  embed_name = 'embeddings/np_2_umap.pkl'

  print("Loading embeddings...")
  embeddings = load_embeddings(bucket_name, file_path)

  print("Reducing embeddings...")
  embeddings_umap = reduce_dimensions(embeddings)

  print("Saving embeddings...")
  save_result(embeddings_umap, embed_name, bucket_name)

if __name__ == '__main__':
  dim_reduction_workflow()

