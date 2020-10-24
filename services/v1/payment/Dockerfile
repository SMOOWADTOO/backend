FROM python:latest
WORKDIR /usr/src/homebiz/services/v1/payment
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./payment.py .
CMD [ "python", "./payment.py" ]