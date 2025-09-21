import pandas as pd
import oracledb
import numpy as np
import matplotlib.pyplot as plt

# CONNECT TO ORACLE
connStr = 'system/system@localhost:1521/xepdb1'
conn = cur = None

try:
    conn = oracledb.connect(connStr)
    cur = conn.cursor()

    sqlQuery = """WITH captain_matches_details AS
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
                  ORDER BY ROUND((wins_as_captain/matches_as_captain)*100,2) DESC """

    df = pd.read_sql(sqlQuery, conn)
    df['WIN_PCT'] = df['WIN_PCT'].str.replace('%','')
    df['WIN_PCT'] = pd.to_numeric(df['WIN_PCT'])

    # PLOTTING

    plt.figure(figsize=(14,6))
    plt.plot(df['CAPTAIN'],df['WIN_PCT'],color = 'blue')
    plt.title('IPL 2024: Captain Performance — Win %',fontsize=15,fontweight='bold')
    plt.xlabel('Captains', fontsize=12)
    plt.ylabel('Win pct' ,fontsize=12)
    plt.xticks(rotation=45, ha='right', color='crimson', fontsize=10)
    plt.yticks(color='green', fontsize=10)
    plt.grid(axis='y',linestyle='--',alpha=0.7)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

except Exception as err:
    print('Unable to connect to DB : ' , err)

finally:
    if(cur):
        cur.close()
    if(conn):
        conn.close()
