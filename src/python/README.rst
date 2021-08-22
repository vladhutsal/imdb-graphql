virtualenv -p python3 .venv
. .venv/bin/activate
poetry install
#python -m imdb_graphql.app
cd imdb_graphql && FLASK_ENV=development flask run
flask run --host=0.0.0.0

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