#!/bin/sh

s32imdbpy.py --verbose imdb_data/tsv/datasets.imdbws.com/ postgresql://postgres@localhost/imdb

# could we use r-script to upload data instead of previous command?
# apt-get install libcurl4-openssl-dev libxml2-dev libssl-dev
# Rscript -e 'install.packages("tidyverse")'
# Rscript pg_import_format.R
# psql 'dbname=imdb user=postgres options=--search-path=public' -f imdb_data/load_tables.sql

psql 'dbname=imdb user=postgres options=--search-path=public' -f imdb_data/create_tables.sql
psql 'dbname=imdb user=postgres options=--search-path=public' -f imdb_data/patch-0.1.sql
