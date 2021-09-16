FROM postgres:latest
RUN apt-get update
RUN apt-get --yes install python3-dev python3-pip wget git postgresql-server-dev-all
RUN pip3 install git+https://github.com/alberanid/imdbpy psycopg2

# isntall R
# RUN apt install dirmngr gnupg apt-transport-https ca-certificates software-properties-common
# RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
# RUN add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/'
# RUN apt install r-base
