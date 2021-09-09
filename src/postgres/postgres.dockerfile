FROM postgres:latest
RUN apt-get update
RUN apt-get --yes install python3-dev python3-pip wget git postgresql-server-dev-all
RUN pip3 install git+https://github.com/alberanid/imdbpy psycopg2
