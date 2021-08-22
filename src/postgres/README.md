Download files from https://datasets.imdbws.com/

Schema description at https://www.imdb.com/interfaces/

Create tables
```sh
psql 'dbname=imdb user=imdb options=--search-path=imdb' -f create_tables.sql
```

Load data into tables
```sh
psql 'dbname=imdb user=imdb options=--search-path=imdb' -f load_tables.sql
```
