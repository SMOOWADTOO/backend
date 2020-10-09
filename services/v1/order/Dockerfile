FROM python:latest
WORKDIR /usr/src/homebiz/services/v1/order
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./order.py .
CMD [ "python", "./order.py" ]