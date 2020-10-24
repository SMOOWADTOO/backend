# ADD DB URL HERE
export PAYMENT_DB_BASE_URL=""
export STRIPE_KEY=

DIR="$( cd "$( dirname "$0" )" && pwd )"
alias python=python3
python "$DIR/payment.py"