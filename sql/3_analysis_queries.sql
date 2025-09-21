-----------------------------------------------------------------------------------------
QUERY 1: Home Advantage — Win % When Playing in Home City
	"Do teams perform better at home? Comparing wins in home city vs away"
------------------------------------------------------------------------------------------
WITH home_matches AS (
    SELECT 
        t.team_name,
        m.winner
    FROM teams t
    INNER JOIN matches m
        ON t.home_city = m.match_city
        AND t.team_name IN (m.team1, m.team2)
),
team_home_performance AS (
    SELECT 
        team_name,
        COUNT(*) AS total_home_matches,
        SUM(CASE WHEN team_name = winner THEN 1 ELSE 0 END) AS home_wins
    FROM home_matches
    GROUP BY team_name
)
SELECT 
    team_name,
    ROUND((home_wins / total_home_matches) * 100, 2) || '%' AS win_percentage
FROM team_home_performance
ORDER BY win_percentage DESC;


------------------------------------------------------------------------------------------
QUERY 2: Toss Decision Impact on Match Outcome (by Venue)
	"Does winning the toss and choosing to bat/field first impact win rate?"
------------------------------------------------------------------------------------------
WITH toss_decision_impact AS (
    SELECT 
        venue,
        toss_decision,
        COUNT(*) AS total_matches,
        SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS wins_after_decision
    FROM matches
    GROUP BY venue, toss_decision
)
SELECT 
    venue,
    toss_decision,
    total_matches,
    wins_after_decision,
    ROUND((wins_after_decision / total_matches) * 100, 2) || '%' AS win_percentage
FROM toss_decision_impact
ORDER BY venue, toss_decision;


------------------------------------------------------------------------------------------
QUERY 3: Player of the Match (POTM) Awards by Team & Player
	"Which teams and players dominate POTM awards?"
------------------------------------------------------------------------------------------
SELECT p.team_name,COUNT(*) as total_potm
FROM players p INNER JOIN matches m
ON p.player_name = m.player_of_match
GROUP BY p.team_name
ORDER BY total_potm DESC;


------------------------------------------------------------------------------------------
QUERY 4: Captain Performance
	"How often do captains win AND get POTM? Showing leadership impact"
------------------------------------------------------------------------------------------
WITH captain_matches_details AS
    (SELECT 
        t.captain,
        t.team_name,
        m.winner,
        m.player_of_match
     FROM teams t INNER JOIN matches m
     ON t.team_name = m.team1
     UNION ALL
     SELECT 
        t.captain,
        t.team_name,
        m.winner,
        m.player_of_match
     FROM teams t INNER JOIN matches m
     ON t.team_name = m.team2
),
captain_win_details AS
   (SELECT 
        captain,
        team_name,
        COUNT(*) AS matches_as_captain,
        SUM(CASE WHEN team_name=winner THEN 1 ELSE 0 END) AS wins_as_captain,
        SUM(CASE WHEN captain=player_of_match THEN 1 ELSE 0 END) AS potm_as_captain
    FROM captain_matches_details
    GROUP BY captain,team_name
)
SELECT
        captain_win_details.*,
        ROUND((wins_as_captain/matches_as_captain)*100,2) || '%' AS win_pct,
        ROUND((potm_as_captain/matches_as_captain)*100,2) || '%' AS potm_pct
FROM captain_win_details 
ORDER BY ROUND((wins_as_captain/matches_as_captain)*100,2) DESC
;        



------------------------------------------------------------------------------------------
QUERY 5: Top 5 All-Rounders (Batting + Bowling Contribution)
	"Who are the most valuable all-rounders? Combining runs scored and wickets taken"
------------------------------------------------------------------------------------------
WITH score_assigned AS
	(SELECT 
    		player_name,
    		team_name,
    		runs_scored,
   		wickets_taken,
    		runs_scored + (wickets_taken*10) AS all_rounder_score     
	FROM players
	WHERE   runs_scored IS NOT NULL AND
      		wickets_taken IS NOT NULL AND
      		runs_scored > 0 AND
      		wickets_taken > 0),
top_5_players AS
	(SELECT 
    		score_assigned.*,
    		ROW_NUMBER() OVER(ORDER BY all_rounder_score DESC) AS rank
	 FROM score_assigned)
SELECT *
FROM top_5_players
WHERE rank <= 5;    



------------------------------------------------------------------------------------------
QUERY 6: IPL 2024 Points Table
	"Simplified points table based on matches won/matches played"
------------------------------------------------------------------------------------------

WITH all_teams AS
    (SELECT 
        team1 AS team
     FROM matches
     UNION ALL
     SELECT 
        team2 AS team
     FROM matches),
match_played AS
    (SELECT 
        team,
        COUNT(*) AS total_matches
     FROM all_teams
     GROUP BY team),
match_won AS
    (SELECT match_played.team,
            match_played.total_matches AS total_matches,
            COUNT(matches.winner) AS won
     FROM match_played LEFT JOIN matches
     ON match_played.team = matches.winner
     GROUP BY match_played.team, match_played.total_matches)
     
SELECT 
        ROW_NUMBER() OVER(ORDER BY won DESC) AS pos,
        team,
        total_matches AS matches,
        COALESCE(won, 0) AS won,
        (total_matches - COALESCE(won, 0)) AS lost,
        COALESCE(won, 0) * 2 AS points
FROM match_won
ORDER BY points DESC;