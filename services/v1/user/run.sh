# ADD DB URL HERE
export USER_DB_BASE_URL="mysql+mysqlconnector://root:root@localhost:3306"
export USER_SVC_SECRET_KEY="h0mebiZ"

DIR="$( cd "$( dirname "$0" )" && pwd )"
alias python=python3
python "$DIR/user.py"