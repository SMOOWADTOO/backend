parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

# add in services here

cd "$parent_path"/services/v1/user
pip3 install --no-cache-dir -r $parent_path/services/v1/user/requirements.txt