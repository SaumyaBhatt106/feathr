FROM python:3.10

COPY ./db_handler/ /usr/src/db_handler
COPY ./sql-registry/ /usr/src/sql-registry
COPY ./access_control/ /usr/src/access_control
COPY ./entrypoint.sh /usr/src

WORKDIR /usr/src
RUN pip install -r ./sql-registry/requirements.txt
RUN pip install -r ./access_control/requirements.txt

EXPOSE 8000

RUN ["chmod", "+x", "./entrypoint.sh"]
ENTRYPOINT ["sh", "-c", "./entrypoint.sh"]