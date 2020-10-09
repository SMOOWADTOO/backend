FROM python:latest
WORKDIR /usr/src/homebiz/services/v1/shop
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./shop.py .
CMD [ "python", "./shop.py" ]