FROM python:3.10

COPY ./sql-registry/ /usr/src/sql-registry
COPY ./db_handler/ /usr/src/db_handler

WORKDIR /usr/src
RUN pip install -r ./sql-registry/requirements.txt

# Start web server
CMD [ "uvicorn","sql-registry.main:app","--host", "0.0.0.0", "--port", "80" ]
