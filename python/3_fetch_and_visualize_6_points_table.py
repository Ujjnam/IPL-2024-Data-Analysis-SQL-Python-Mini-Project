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

    sqlQuery = """ WITH all_teams AS
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
                    ORDER BY points DESC """

    df = pd.read_sql(sqlQuery, conn)
    def get_color(x):
        return 'lightgreen' if(x >= df['POINTS'].quantile(0.75)) else 'orange' if(x == df['POINTS'].quantile(0.5)) else 'red'

    # PLOTTING

    plt.figure(figsize=(12,8))
    plt.bar(df['TEAM'], df['POINTS'] ,color = [get_color(x) for x in df['POINTS']], edgecolor='black')
    plt.title('IPL 2024 Points Table',fontsize=15,fontweight='bold')
    plt.xlabel('Teams', fontsize=12)
    plt.ylabel('Points' ,fontsize=12)
    plt.xticks( ha='right', color='darkblue', fontsize=10)
    plt.yticks(color='darkred', fontsize=10)
    plt.grid(axis='y',linestyle='--',alpha=0.7)
    plt.tight_layout()
    plt.show()

except Exception as err:
    print('Unable to connect to DB : ' , err)

finally:
    if(cur):
        cur.close()
    if(conn):
        conn.close()
