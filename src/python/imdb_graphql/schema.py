import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy import func, desc
from sqlalchemy.orm import Query as AlchemyQuery

from imdb_graphql.database import session as s
import sqlalchemy_opentracing as tracingM
from imdb_graphql.database import tracer, engine

from .models import (
    Title as TitleModel,
    Movie as MovieModel,
    Series as SeriesModel,
    Episode as EpisodeModel,
    EpisodeInfo as EpisodeInfoModel,
    Rating as RatingModel,
    Name as NameModel,
    TitleType as TitleTypeEnum
)

TitleType = graphene.Enum.from_enum(TitleTypeEnum)


class Title(graphene.Interface):
    imdbID = graphene.String()
    titleType = graphene.String()
    primaryTitle = graphene.String()
    originalTitle = graphene.String()
    isAdult = graphene.Boolean()
    startYear = graphene.Int()
    endYear = graphene.Int()
    runtime = graphene.Int()
    genres = graphene.String()
    averageRating = graphene.Float()
    numVotes = graphene.Int()

exclude_fields = ('titleSearchCol', '_type', )


class Movie(SQLAlchemyObjectType):
    class Meta:
        model = MovieModel
        interfaces = (Title, )
        exclude_fields = exclude_fields


class Episode(SQLAlchemyObjectType):
    class Meta:
        model = EpisodeModel
        interfaces = (Title, )
        exclude_fields = exclude_fields

    seasonNumber = graphene.Int()
    episodeNumber = graphene.Int()
    series = graphene.Field(lambda: Series)


class Series(SQLAlchemyObjectType):
    class Meta:
        model = SeriesModel
        interfaces = (Title, )
        exclude_fields = exclude_fields

    totalSeasons = graphene.Int()
    episodes = graphene.Field(
        graphene.List(Episode),
        season=graphene.List(graphene.Int)
    )

    def resolve_episodes(self, info, **args):
        print('going to resolve query')
        query = Episode.get_query(info)
        print('------- query ', query)
        parrent = tracer.start_span('resolve episodes')
        

        print('----------- going to work on the series query')
        # tracingM.set_parent_span(query, parrent)
        intermediate_q1 = query.join(EpisodeModel.info)
        print('------- intermediate_q1 ', intermediate_q1)

        # query = (
        #     Episode
        #     .get_query(info)
        #     .join(EpisodeModel.info)
        #     .filter_by(seriesID=self.imdbID)
        # )

        # tracingM.set_parent_span(intermediate_q1, parrent)
        intermediate_q2 = (
            intermediate_q1.filter(EpisodeInfoModel.seasonNumber.in_(args['season']))
            if 'season' in args else intermediate_q1
        )
        print('------- intermediate_q2 ', intermediate_q2)

        # tracingM.set_parent_span(intermediate_q2, parrent)
        final_q = (
            intermediate_q2.order_by(
                EpisodeInfoModel.seasonNumber,
                EpisodeInfoModel.episodeNumber
            )
            if 'season' in args and len(args['season']) > 1
            else intermediate_q2.order_by(EpisodeInfoModel.episodeNumber)
        )
        print('------- final_q ', final_q)

        # tracingM.set_parent_span(final_q, parrent)
        # conn.execute(final_q)
        parrent.finish()
        print('----------- just finished the work on the series query')
        return final_q

    def resolve_totalSeasons(self, info):
        # tracingM.set_traced(s)
        return(
            EpisodeInfoModel
            .query
            .with_entities(EpisodeInfoModel.seasonNumber)
            .filter_by(seriesID=self.imdbID)
            .group_by(EpisodeInfoModel.seasonNumber)
            .count()
        )

class Name(SQLAlchemyObjectType):
    class Meta:
        model = NameModel
        interfaces = (graphene.relay.Node, )
        exclude_fields = ('id', )
    
    imdbID = graphene.String()
    birthYear = graphene.Int()
    deathYear = graphene.Int()
    primaryName = graphene.String()
    knownForTitles = graphene.String()
    primaryProfession = graphene.String()


class Query(graphene.ObjectType):
    title = graphene.Field(Title, imdbID=graphene.String(required=True))
    movie = graphene.Field(Movie, imdbID=graphene.String(required=True))
    series = graphene.Field(Series, imdbID=graphene.String(required=True))
    episode = graphene.Field(Episode, imdbID=graphene.String(required=True))
    search = graphene.Field(
        graphene.List(Title),
        title=graphene.String(required=True),
        types=graphene.List(TitleType),
        result=graphene.Int(default_value=5)
    )
    name = graphene.Field(Name, imdbID=graphene.String(required=True))

    def resolve_title(self, info, imdbID):
        # tracingM.set_traced(s)
        a = TitleModel.query.filter_by(imdbID=imdbID).first()
        print('====-ss---==', a)
        return TitleModel.query.filter_by(imdbID=imdbID).first()

    def resolve_movie(self, info, imdbID):
        # tracingM.set_traced(s)
        return Movie.get_query(info).filter_by(imdbID=imdbID).first()

    def resolve_series(self, info, imdbID):
        # tracingM.set_traced(s)
        return Series.get_query(info).filter_by(imdbID=imdbID).first()

    def resolve_episode(self, info, imdbID):
        # tracingM.set_traced(s)
        return Episode.get_query(info).filter_by(imdbID=imdbID).first()

    def resolve_search(self, info, title, types=None, result=None):
        tsquery = func.to_tsquery(f'\'{title}\'')

        # choose all titles with PostgreSQL lexems, generated by tsquery
        query1 = (
            TitleModel
            .query
            .filter(TitleModel.titleSearchCol.op('@@')(tsquery))
        )

        # filters by type
        query2 = (
            query1.filter(TitleModel._type.in_(types))
            if types is not None else query1
        )
        
        query3 = (
            query2
            .join(TitleModel.rating)
            .order_by(
                desc(RatingModel.numVotes >= 1000),
                desc(TitleModel.primaryTitle.ilike(title)),
                desc(RatingModel.numVotes),
                desc(func.ts_rank_cd(TitleModel.titleSearchCol, tsquery, 1))
            )
            .limit(result)
        )

        tracingM.set_traced(s)
        res = query3.all()
        # print('----=------ que', res)
        return res
    
    def resolve_name(self, info, imdbID):
        # tracingM.set_traced(s)
        return NameModel.query.filter_by(imdbID=imdbID).first()


schema = graphene.Schema(query=Query, types=[Movie, Series, Episode, Name])
