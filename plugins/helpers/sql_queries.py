 ##################################################################
# insert select queries
class SqlQueries:

    songplay_table_insert = ("""
        /* songplays table is not truncated each time it is loaded from the scheduler  */
        BEGIN TRANSACTION;
        
        DELETE FROM songplays
        USING staging_events
        WHERE staging_events.page = 'NextSong'
        AND songplays.user_id = staging_events.userid
        AND songplays.session_id = staging_events.sessionid
        AND songplays.start_time = (TIMESTAMP 'epoch' + staging_events.ts::NUMERIC /
                                        1000 * INTERVAL '1 second')
        ;
        
        INSERT INTO songplays(start_time, user_id, level, song_id, artist_id
            , session_id, location, user_agent)
        SELECT (TIMESTAMP 'epoch' + events.ts::NUMERIC / 
                    1000 * INTERVAL '1 second') AS start_time
            , events.userId::INT, events.level, songs.song_id, songs.artist_id
            , events.sessionId, events.location, events.userAgent
        FROM staging_events events
        INNER JOIN staging_songs songs
            ON songs.title = events.song
            AND songs.duration = events.length
            AND songs.artist_name = events.artist
            AND events.page = 'NextSong';
            
        END TRANSACTION;
    """)

    user_table_insert = ("""
       /* users table is truncated each time it is loaded from the scheduler */
        INSERT INTO users(user_id, first_name, last_name, gender, level)
            SELECT events.userid::INT, events.firstname, events.lastname, events.gender
                , events.level
            FROM staging_events events
            INNER JOIN
            (
                SELECT userid, MAX(ts) AS max_ts
                FROM staging_events
                WHERE page = 'NextSong'
                GROUP BY 1
            ) cur_lvl
                ON cur_lvl.userid = events.userid
                AND cur_lvl.max_ts = events.ts
                AND events.page = 'NextSong'
            GROUP BY 1, 2, 3, 4, 5;
    """)

    song_table_insert = ("""
        /* songs table is truncated each time it is loaded from the scheduler */
        INSERT INTO songs(song_id, title, artist_id, year, duration)
            SELECT DISTINCT song_id, title, artist_id, year, duration
            FROM staging_songs;
    """)

    artist_table_insert = ("""
        /* artists table is truncated each time it is loaded from the scheduler */
        INSERT INTO artists(artist_id, name, location, latitude, longitude)
            SELECT artist_id, artist_name, artist_location, artist_latitude
                , artist_longitude
            FROM
            (
                SELECT artist_id, artist_name, artist_location, artist_latitude
                    , artist_longitude
                    , SUM(1) OVER (
                        PARTITION BY artist_id
                        ORDER BY year DESC ROWS UNBOUNDED PRECEDING
                      ) AS row_nbr
                FROM staging_songs
            ) xyz
            WHERE row_nbr = 1;
    """)

    time_table_insert = ("""
        /* time table is truncated each time it is loaded from the scheduler */
        INSERT INTO time(start_time, hour, day, week, month, year, weekday)
            SELECT DISTINCT start_time
                , EXTRACT(hour FROM start_time) AS hour -- hour of day
                , EXTRACT(day FROM start_time) AS day -- day of month
                , EXTRACT(week FROM start_time) AS week  -- week of month or year
                , EXTRACT(month FROM start_time) AS month
                , EXTRACT(year FROM start_time) AS year
                , EXTRACT(weekday FROM start_time) AS weekday
            FROM songplays;
    """)
    
 ##################################################################
 # data quality queries

    songplay_join_song_cnt = ("""
        SELECT count(*)
        FROM songplays sp
        INNER JOIN songs sng ON sng.song_id = sp.song_id;
    """)

    songplay_join_artist_cnt = ("""
        SELECT count(*)
        FROM songplays sp
        INNER JOIN artists artst ON artst.artist_id = sp.artist_id;
    """)

    songplay_join_user_cnt = ("""
        SELECT count(*)
        FROM songplays sp
        INNER JOIN users usr ON usr.user_id = sp.user_id;
    """)

    songplay_join_time_cnt = ("""
        SELECT count(*)
        FROM songplays sp
        INNER JOIN time tm ON tm.start_time = sp.start_time;
    """)

