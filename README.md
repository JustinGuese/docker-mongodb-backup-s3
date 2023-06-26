# remarks

my first tip: do not use mongodb. in my past 2-3 years using it administration was horrible. it's easy to set up, but then you will run in countless errors including limitations to CPUs, special RAM bugs etc where they basically just tell you to go and buy their managed expensive service. 
I migrated everything to PSQL, and you should do the same. 

Previous commits show a version using mongodump and mongorestore, but as you might have guessed it, they don't work and corrupt your database.

## restore

1. download the .tar.gz file
2. tar -xvf 2023-06-26_backup.tar.gz
3. navigate in the subfolder to the DB you want to restore
4. you should see a .bson and a .metadata.json file in this folder
5. mongorestore patients.bson -h URL:PORT -db DBNAME
    - optionally -U = user, 


# docker-mongodb-backup-s3

https://hub.docker.com/repository/docker/guestros/mongodb-backup-s3

simple mongodb backup image to be run as cronjob / job

dumps the contents of a mongodb database with [mongodump](https://www.mongodb.com/docs/database-tools/mongodump/) to a file containing the current date (e.g. mongodbbackup-2022-12-12.gz), and uploads it to an s3 bucket. 

## usage

If you want to run it manually, swap out the env variables with your values, and run the following:

`docker run --rm -e MONGO_URI=mongodb://mongo:27017 -e AWS_ACCESS_KEY_ID=secret -e AWS_SECRET_ACCESS_KEY=secret -e S3_BUCKET=mongodb-backup-bucket -e S3_ENDPOINT=https://s3.amazonaws.com guestros/mongodb-backup-s3:latest`

## kubernetes job

if you are running mongodb in a kubernetes cluster, you can schedule a backup cronjob.

0. copy the [cloudcreds-example](cloudcreds-example) to "cloudcreds" and fill it with the matching values.
S3_PATH can be empty, in that case the archive gets saved at root level
S3_ENDPOINT can be left like that if you are going to use it with the AWS s3 target.
1. create the secret after filling in the parameters in the cloudcreds file
    `kubectl create secret generic s3backuptarget --from-env-file=cloudcreds`
2. adapt the crontab values, bucket etc in [kubernetes/mongodb-backup-cronjob.yaml](kubernetes/mongodb-backup-cronjob.yaml)
3. `kubectl apply -f kubernetes/mongodb-backup-cronjob.yaml`