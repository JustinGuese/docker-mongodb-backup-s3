#!/bin/bash
mongodump --uri="$MONGO_URI" --gzip --archive=mongodbbackup-$(date +%Y-%m-%d).gz
AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY aws s3 cp mongodbbackup-$(date +%Y-%m-%d).gz s3://$S3_BUCKET/$S3_PATH --endpoint-url=$S3_ENDPOINT