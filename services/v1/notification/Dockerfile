FROM python:latest
WORKDIR /usr/src/homebiz/services/v1/notification
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./notification.py .
CMD [ "python", "./notification.py" ]