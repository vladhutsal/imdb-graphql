\copy titles(tconst, titletype, primarytitle, originaltitle, isadult, startyear, endyear, runtimeminutes, genres) from 'tsv/one.tsv'  csv header quote E'\t';
\copy titles(tconst, titletype, primarytitle, originaltitle, isadult, startyear, endyear, runtimeminutes, genres) from 'tsv/title.basics.tsv'  csv header quote E'\b';
\copy akas from 'tsv/akas.tsv' delimiter E'\t' null as 'NULL' csv header quote E'\b';
\copy episodes from 'tsv/episodes.tsv' delimiter E'\t' null as 'NULL' csv header quote E'\b';
\copy ratings from 'tsv/ratings.tsv' delimiter E'\t' null as 'NULL' csv header quote E'\b';
\copy people(nconst, primaryname, birthyear, deathyear, primaryprofession, knownfortitles) from 'tsv/people.tsv' delimiter E'\t' null as 'NULL' csv header quote E'\b';
\copy principals from 'tsv/principals.tsv' delimiter E'\t' null as 'NULL' csv header quote E'\b';
\copy crew from 'tsv/crew.tsv' delimiter E'\t' null as 'NULL' csv header quote E'\b';
