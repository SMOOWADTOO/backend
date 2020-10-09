FROM python:latest
WORKDIR /usr/src/homebiz/services/v1/search
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./search.py .
CMD [ "python", "./search.py" ]