parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

# COPY EXPORTS ENV VARS HERE

# HEREEEEE

# add in services here and change the folder name and app name below to your services, using "user" service as a sample

cd "$parent_path"/services/v1/user
python3 user.py &

cd "$parent_path"/services/v1/product
python3 product.py &

cd "$parent_path"/services/v1/shop
python3 shop.py &

cd "$parent_path"/services/v1/order
python3 order.py &

cd "$parent_path"/services/v1/review
python3 review.py &

cd "$parent_path"/services/v1/payment
python3 payment.py &

cd "$parent_path"/services/v1/notification
python3 notification.py &

cd "$parent_path"/services/v1/search
python3 search.py &