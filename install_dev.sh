parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

# add in services here, change the folder name below to your services, using "user" service as a sample
cd "$parent_path"/services/v1/user
pip3 install --no-cache-dir -r $parent_path/services/v1/user/requirements.txt

cd "$parent_path"/services/v1/product
pip3 install --no-cache-dir -r $parent_path/services/v1/product/requirements.txt

cd "$parent_path"/services/v1/shop
pip3 install --no-cache-dir -r $parent_path/services/v1/shop/requirements.txt

cd "$parent_path"/services/v1/order
pip3 install --no-cache-dir -r $parent_path/services/v1/order/requirements.txt

cd "$parent_path"/services/v1/review
pip3 install --no-cache-dir -r $parent_path/services/v1/review/requirements.txt

cd "$parent_path"/services/v1/payment
pip3 install --no-cache-dir -r $parent_path/services/v1/payment/requirements.txt

cd "$parent_path"/services/v1/notification
pip3 install --no-cache-dir -r $parent_path/services/v1/notification/requirements.txt

cd "$parent_path"/services/v1/search
pip3 install --no-cache-dir -r $parent_path/services/v1/search/requirements.txt