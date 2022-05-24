# Mariadb-to-s3

This repository demonstrates some of the mechanisms needed to load a SQL-formatted file into a MariaDB database running in a Docker container, and use another container with MySQL-Client to perform a remote dump in the first container running MariaDB using Shell/Bash script, and use a third container to periodically (Crontab) verify the presence of a dump in the shared folder with MySQL-Client and to send this dump to an S3 Bucket on AWS using Python script.

The sample SQL file was randomly generated using Python.


## Running the Examples

### Docker Images
For this project, it was used one readly-available image of MariaDB and two custom images to implement the MySQL-Client and to implement the Python job orchestrated by Crontab.
1. MariaDB: using the latest mariadb image from DockerHub, the idea in this container is to injest a predefined SQL file and keeps running.

2. MySQL Dumper: it was created a simple [image](https://github.com/viccsouza/Mariadb-to-S3/blob/main/app/dumper/Dockerfile) with MySQL-Client to be able to log into MariaDB container and extract a dump into /data/dumper/ using a shell script file.
```sh
docker build -t client ./app/dumper/
```

3. Python with Crontab: this [image](https://github.com/viccsouza/Mariadb-to-S3/blob/main/app/s3-sender/Dockerfile) will have [python:3.8-alpine3.14](https://hub.docker.com/_/python), crontab and [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) package installed  to check the presence of the dump file and connect with AWS.
```sh
docker build -t s3-sender ./app/s3-sender/
```

### Docker Compose
After building both images for container 2 and 3, the [docker-compose.yml](https://github.com/viccsouza/Mariadb-to-S3/blob/main/docker-compose.yml) file will be read to be started.
```sh
docker-compose up -d
```
These three containers will work as follows:
1. Container 1 goes up and ingests [data](https://github.com/viccsouza/Mariadb-to-S3/blob/main/data/database/datadump.sql) into its database from its entrypoint. The container continues to work.
2. Container 2 goes up, runs the [dump_start.sh](https://github.com/viccsouza/Mariadb-to-S3/blob/main/app/dumper/dump_start.sh) script that connects to container 1 and dumps it in a folder shared with container 3. Soon after this process the container becomes unavailable.
3. Container 3 goes up, starts the [cronjob](https://github.com/viccsouza/Mariadb-to-S3/blob/main/app/s3-sender/crontab) that runs the [python](https://github.com/viccsouza/Mariadb-to-S3/blob/main/app/s3-sender/send-to-s3.py) script to periodically checks the presence of the dump file in the shared folder with Container 2 and checks the existence of the bucket to create it and sends it to the S3 bucket. After this process, the dump file in the shared folder is deleted and the containers keeps checking the presence of a new dump.


### AWS S3 Bucket
There will be a credential file inside the /app/s3-sender/ folder to give the necessary information to the python script connect to AWS create the bucket if it does not exists already. It will be a line seppareted file with the KEY_ID, ACCESS_KEY and BUCKET_NAME in this order.

The ideia is to dump the SQL file in a single folder per day, with the naming respecting the following the pattern YYYYMMAA and the filename respecting the pattern "datadump#.sql", starting with 1, in case there's more than one dump in the day.


## Final Considerations
This work was done in collaboration with the Data Engineering class of the [Encantech Program](https://www.cesar.school/formacao-em-dados-renner/), promoted by [Renner](https://www.lojasrenner.com.br/) with classes taught by [Cesar](https://www.cesar.school/). 
Thanks a bunch for all teachers and students that made this experience so enriching and fun, specially the Data Engineering Classes!
