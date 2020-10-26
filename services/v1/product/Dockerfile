FROM python:latest
WORKDIR /usr/src/homebiz/services/v1/product
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./product.py .
CMD [ "python", "./product.py" ]