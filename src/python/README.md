Setup python env:

```
virtualenv -p python3 .venv
. .venv/bin/activate
poetry install
```

For dev run with

`cd imdb_graphql && FLASK_ENV=development flask run`

for prod run with

`cd imdb_graphql && flask run --host=0.0.0.0`

Go to http://127.0.0.1:5000/imdb enter

```
  movie(imdbID: "7040874") {
    __typename,
    imdbID,
    titleType,
    primaryTitle,
    genres,
    averageRating,
    numVotes
  }

```