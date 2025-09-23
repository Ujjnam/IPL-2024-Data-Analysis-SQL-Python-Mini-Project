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

    sqlQuery = """ WITH home_matches AS (
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
                    ORDER BY win_percentage DESC """

    df = pd.read_sql(sqlQuery , conn)
    df['WIN_PERCENTAGE'] = df['WIN_PERCENTAGE'].str.replace('%',"")
    df['WIN_PERCENTAGE'] = pd.to_numeric(df['WIN_PERCENTAGE'])


    # PLOTTING
    def get_color(percentage):
        if(percentage)>=75:
            return 'green'
        elif(percentage>=50 and percentage<75):
            return 'lightgreen'
        else:
            return 'red'
    colors = [get_color(perc) for perc in df['WIN_PERCENTAGE']]

    plt.figure(figsize=(14,6))
    plt.bar(df['TEAM_NAME'],df['WIN_PERCENTAGE'],color=colors, edgecolor='black')
    plt.title('IPL 2024 : Teams performance at Home Ground',fontsize=16 ,fontweight='bold')
    plt.xlabel('Teams',fontsize=12)
    plt.ylabel('Win %', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

except Exception as err:
    print('Unable to connect to DB : ' , err)

finally:
    if(cur):
        cur.close()
    if(conn):
        conn.close()

