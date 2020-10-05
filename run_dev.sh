parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

# ADD DB URL HERE
export USER_DB_BASE_URL=""

# AWS env variables
export S3_BUCKET_NAME=""

# add in services here

cd "$parent_path"/services/v1/user
pip3 install --no-cache-dir -r $parent_path/services/v1/user/requirements.txt
python3 user.py &
