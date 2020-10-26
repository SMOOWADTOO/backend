# ADD DB URL HERE
# export SEARCH_DB_BASE_URL=""
export HOMEBIZ_URL="http://www.casafair.org/api/"

DIR="$( cd "$( dirname "$0" )" && pwd )"
alias python=python3
python "$DIR/search.py"