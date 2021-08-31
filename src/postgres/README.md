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

Update title_basics table to be able do search
```sh
psql 'dbname=imdb user=imdb options=--search-path=imdb' -f patch-0.1.sql
```