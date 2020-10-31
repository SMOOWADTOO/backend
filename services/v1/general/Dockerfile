FROM python:latest
WORKDIR /usr/src/ridey/microservices/general
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./general.py .
CMD [ "python", "./general.py" ]