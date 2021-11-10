CREATE TABLE IF NOT EXISTS public.staging_events(artist TEXT, auth TEXT
        , firstName TEXT, gender TEXT, itemInSession NUMERIC
        , lastName TEXT, length NUMERIC, level TEXT, location TEXT
        , method TEXT, page TEXT, registration NUMERIC, sessionId NUMERIC
        , song TEXT, status NUMERIC, ts NUMERIC, userAgent TEXT
        , userId TEXT);


CREATE TABLE IF NOT EXISTS public.staging_songs(song_id TEXT, num_songs INTEGER
    , title TEXT, artist_name TEXT, artist_latitude NUMERIC
    , year INTEGER, duration NUMERIC, artist_id TEXT
    , artist_longitude NUMERIC, artist_location TEXT
    );


CREATE TABLE IF NOT EXISTS public.songplays(songplay_id INT IDENTITY(1,1)
        , start_time TIMESTAMP NOT NULL, user_id INT NOT NULL
        , level TEXT, song_id TEXT NOT NULL, artist_id TEXT NOT NULL
        , session_id INT NOT NULL, location TEXT, user_agent TEXT
        , PRIMARY KEY(user_id, session_id, start_time));


CREATE TABLE IF NOT EXISTS public.users(user_id INT NOT NULL, first_name TEXT
        , last_name TEXT , gender CHAR, level TEXT);


CREATE TABLE IF NOT EXISTS public.songs(song_id TEXT NOT NULL, title TEXT
        , artist_id TEXT NOT NULL, year INT, duration NUMERIC);


CREATE TABLE IF NOT EXISTS public.artists(artist_id TEXT NOT NULL, name TEXT
        , location TEXT, latitude INT, longitude INT);


CREATE TABLE IF NOT EXISTS public.time(start_time TIMESTAMP NOT NULL
        , hour INT, day INT, week INT, month INT, year INT, weekday INT);
