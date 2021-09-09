#!/bin/sh

mkdir data
wget -r -A "*tsv.gz" https://datasets.imdbws.com -P src/postgres/tsv/
