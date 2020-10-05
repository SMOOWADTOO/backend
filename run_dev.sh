parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

# ADD DB URL HERE
export USER_DB_BASE_URL=""

# AWS env variables
export S3_BUCKET_NAME=""

# add in services here and change the folder name and app name below to your services, using "user" service as a sample

cd "$parent_path"/services/v1/user
pip3 install --no-cache-dir -r $parent_path/services/v1/user/requirements.txt
python3 user.py &


cd "$parent_path"/services/v1/product
pip3 install --no-cache-dir -r $parent_path/services/v1/product/requirements.txt
python3 product.py &