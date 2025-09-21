---------------------------------------------------------------------------------------------
				teams
---------------------------------------------------------------------------------------------
INSERT INTO teams (team_name, home_city, captain, coach, owner) 
VALUES (:1, :2, :3, :4, :5);

---------------------------------------------------------------------------------------------
				players
---------------------------------------------------------------------------------------------
INSERT INTO players (player_name, team_name, matches_played, innings, 
		     runs_scored, highest_score, batting_average,
                     strike_rate, centuries, fifties , overs_bowled, 
                     wickets_taken, bowling_average, economy_rate) VALUES
                     (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14);


-----------------------------------------------------------------------------------------------
				matches
-----------------------------------------------------------------------------------------------
INSERT INTO matches (match_id, match_date, venue, match_city, team1, 
                     team2, toss_winner, toss_decision, winner, result_type, 
                     result_margin, player_of_match) VALUES
                     (:1, to_date(:2 , 'YYYY-MM-DD'), :3, :4, :5, :6, :7, :8, :9, :10, :11, :12);