from sqlalchemy import case, Column, Integer, Float, String
from sqlalchemy.orm import column_property, relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from enum import Enum

from .database import Base


class TitleType(Enum):
    MOVIE = 'movie'
    SERIES = 'series'
    EPISODE = 'episode'

class Title(Base):
    __tablename__ = 'title_basics'

    imdbID = Column('tconst', Integer, primary_key=True)
    titleType = Column('titleType', String)
    _type = column_property(
        case(
            {
                'tv series': 'series',
                'tv mini series': 'series',
                'episode': 'episode'
            },
            value=titleType,
            else_='movie'
        )
    )
    primaryTitle = Column('primaryTitle', String)
    originalTitle = Column('originalTitle', String)
    isAdult = Column('isAdult', Integer)
    startYear = Column('startYear', Integer)
    endYear = Column('endYear', Integer)
    runtime = Column('runtimeMinutes', Integer)
    genres = Column('genres', String)
    rating = relationship(
        'Rating',
        foreign_keys=imdbID,
        primaryjoin='Title.imdbID == Rating.imdbID',
        backref=backref('title', uselist=False)
    )
    averageRating = association_proxy('rating', 'averageRating')
    numVotes = association_proxy('rating', 'numVotes')
    titleSearchCol = Column('titleSearchCol')

    __mapper_args__ = {'polymorphic_on': _type}


class Movie(Title):
    __mapper_args__ = {'polymorphic_identity': 'movie'}


class Series(Title):
    __mapper_args__ = {'polymorphic_identity': 'series'}

    episodes = association_proxy('_episodes', 'episode')


class Episode(Title):
    __mapper_args__ = {'polymorphic_identity': 'episode'}

    info = relationship(
        'EpisodeInfo',
        foreign_keys='Episode.imdbID',
        primaryjoin='Episode.imdbID == EpisodeInfo.imdbID',
        backref=backref('episode', uselist=False)
    )

    seasonNumber = association_proxy('info', 'seasonNumber')
    episodeNumber = association_proxy('info', 'episodeNumber')
    series = association_proxy('info', 'series')


class EpisodeInfo(Base):
    __tablename__ = 'title_episode'

    imdbID = Column('tconst', String, primary_key=True)
    seriesID = Column('parentTconst', String)
    seasonNumber = Column('seasonNumber', Integer)
    episodeNumber = Column('episodeNumber', Integer)
    series = relationship(
        'Series',
        foreign_keys=seriesID,
        primaryjoin='Series.imdbID == EpisodeInfo.seriesID',
        backref=backref('_episodes', uselist=True)
    )


class Rating(Base):
    __tablename__ = 'title_ratings'

    imdbID = Column('tconst', Integer, primary_key=True)
    averageRating = Column('averageRating', Float)
    numVotes = Column('numVotes', Integer)

class Name(Base):
    __tablename__ = 'name_basics'

    imdbID = Column('nconst', Integer, primary_key=True)
    birthYear = Column('birthYear', Integer)
    deathYear = Column('deathYear', Integer)
    primaryName = Column('primaryName', String)
    knownForTitles = Column('knownForTitles', String)
    primaryProfession = Column('primaryProfession', String)
