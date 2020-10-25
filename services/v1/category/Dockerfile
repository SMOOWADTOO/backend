FROM python:latest
WORKDIR /usr/src/homebiz/services/v1/category
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./user.py .
CMD [ "python", "./category.py" ]