FROM python:latest
WORKDIR /usr/src/homebiz/services/v1/review
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./review.py .
CMD [ "python", "./review.py" ]