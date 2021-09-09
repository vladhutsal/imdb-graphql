#!/bin/sh

s32imdbpy.py --verbose imdb_data/tsv/datasets.imdbws.com/ postgresql://postgres@localhost/imdb

psql 'dbname=imdb user=postgres options=--search-path=public' -f imdb_data/create_tables.sql
psql 'dbname=imdb user=postgres options=--search-path=public' -f imdb_data/load_tables.sql
psql 'dbname=imdb user=postgres options=--search-path=public' -f imdb_data/patch-0.1.sql
