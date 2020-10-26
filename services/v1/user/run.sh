# ADD DB URL HERE
export DB_BASE_URL=
export USER_DB_NAME=homebiz
export USER_SVC_SECRET_KEY="h0mebiZ"

DIR="$( cd "$( dirname "$0" )" && pwd )"
alias python=python3
python "$DIR/user.py"