# ADD DB URL HERE
export SHOP_DB_BASE_URL="mysql+mysqlconnector://root:root@localhost:3306"

DIR="$( cd "$( dirname "$0" )" && pwd )"
alias python=python3
python "$DIR/shop.py"