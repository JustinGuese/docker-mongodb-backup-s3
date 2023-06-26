FROM python:alpine
RUN apk update
RUN apk install mongodb -y
RUN pip install pymongo boto3
COPY ./mongobackup.py /app/mongobackup.py
WORKDIR /app
CMD ["python", "mongobackup.py"]