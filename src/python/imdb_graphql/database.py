from imdb_graphql.tracing import get_tracer
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy_opentracing as opentrace

engine = create_engine('postgresql://postgres:admin@postgres:5432/imdb')

tracer = get_tracer()
opentrace.init_tracing(tracer)
# opentrace.register_engine(engine)

session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
))

Base = declarative_base()
Base.query = session.query_property()

def init_db():
    from .models import Title, Movie, Series, Episode, EpisodeInfo, Rating, Name
    Base.metadata.reflect(engine)
