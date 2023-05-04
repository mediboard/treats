#!/bin/bash

# Set your variables
REMOTE_USER="ubuntu"
REMOTE_HOST="34.216.174.116"
KEY_PATH="~/umap_test.pem"

# Read the AWS credentials from the ~/.aws/credentials file
AWS_ACCESS_KEY_ID=$(grep -A2 '\[default\]' ~/.aws/credentials | grep 'aws_access_key_id' | awk -F '= ' '{print $2}')
AWS_SECRET_ACCESS_KEY=$(grep -A2 '\[default\]' ~/.aws/credentials | grep 'aws_secret_access_key' | awk -F '= ' '{print $2}')

# Copy the Python script to the remote machine
scp -i "${KEY_PATH}" workflows/dim_reduction_workflow.py "${REMOTE_USER}@${REMOTE_HOST}:~/"

# Execute commands on the remote machine
ssh -i "${KEY_PATH}" "${REMOTE_USER}@${REMOTE_HOST}" /bin/bash << EOF
  # Update package lists
  sudo apt-get update

  # Install Python 3 and pip
  sudo apt-get install -y python3 python3-pip

  # Create a virtual environment
  python3 -m venv env

  # Activate the virtual environment
  source env/bin/activate

  # Install required Python packages
  pip install boto3 umap-learn numpy

  # Set AWS credentials
  export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
  export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

  # Run the Python script
  python3 dim_reduction_workflow.py

  # Deactivate the virtual environment
  deactivate
EOF
