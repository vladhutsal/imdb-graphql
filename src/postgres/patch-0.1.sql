ALTER TABLE title_basics ADD COLUMN "titleSearchCol" tsvector;
UPDATE title_basics SET "titleSearchCol" =
    to_tsvector('english', coalesce("primaryTitle",'') || ' ' || coalesce("originalTitle",''));

CREATE INDEX title_idx ON title_basics USING GIN ("titleSearchCol");
UPDATE title_basics SET "titleSearchCol" =
    setweight(to_tsvector(coalesce("primaryTitle",'')), 'A') ||
    setweight(to_tsvector(coalesce("originalTitle",'')), 'C');
