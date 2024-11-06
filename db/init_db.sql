create table if not exists movies (
    id serial primary key,
    movie_id text not null unique,
    type text not null,
    title text not null,
    poster text not null,
    scenes text[],
    rating real ,
    year_post integer ,
    country text[] ,
    genrs text[] ,
    duration text ,
    plot text ,
    certification text,
    playlist text[] not NULL
 );



