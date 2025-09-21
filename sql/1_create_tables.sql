-----------------------------------------------------------------------------
				teams
-----------------------------------------------------------------------------
CREATE TABLE teams(team_name VARCHAR2(10) PRIMARY KEY,
                                      home_city VARCHAR2(20) UNIQUE NOT NULL,
                                      captain VARCHAR2(20) NOT NULL,
                                      coach VARCHAR2(20) NOT NULL,
                                      owner VARCHAR2(30) NOT NULL);

----------------------------------------------------------------------------
				players
----------------------------------------------------------------------------
CREATE TABLE players(player_name VARCHAR2(50) PRIMARY KEY,
                     team_name VARCHAR2(10) NOT NULL,
                     matches_played NUMBER(2),
                     innings NUMBER(2),
                     runs_scored NUMBER(4),
                     highest_score NUMBER(3),
                     batting_average NUMBER(5,2),
                     strike_rate NUMBER(5,2),
                     centuries NUMBER(2),
                     fifties NUMBER(2),
                     overs_bowled NUMBER(3,1),
                     wickets_taken NUMBER(3),
                     bowling_average NUMBER(6,2),
                     economy_rate NUMBER(4,2));

-----------------------------------------------------------------------------
				matches
-----------------------------------------------------------------------------
CREATE TABLE matches(match_id NUMBER PRIMARY KEY,
                     match_date DATE NOT NULL,
                     venue VARCHAR2(50) NOT NULL,
                     match_city VARCHAR2(30) NOT NULL,
                     team1 VARCHAR2(10) NOT NULL,
                     team2 VARCHAR2(10) NOT NULL,
                     toss_winner VARCHAR2(10),
                     toss_decision VARCHAR2(10),
                     winner VARCHAR2(10),
                     result_type VARCHAR2(10),
                     result_margin NUMBER(4),
                     player_of_match VARCHAR2(30));