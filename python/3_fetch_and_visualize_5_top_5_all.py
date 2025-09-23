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

    sqlQuery = """ WITH score_assigned AS
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
                        WHERE rank <= 5 """

    df = pd.read_sql(sqlQuery, conn)
    df['PLAYER_LABEL'] = df['PLAYER_NAME'] + '(' + df['TEAM_NAME'] + ')'

    # PLOTTING

    plt.figure(figsize=(12,8))
    plt.hlines(y = df['PLAYER_LABEL'], xmin=0, xmax=df['ALL_ROUNDER_SCORE'], color='seagreen', alpha=0.7, linewidth=3)
    plt.scatter(df['ALL_ROUNDER_SCORE'], df['PLAYER_LABEL'], color = 'crimson', s=150, edgecolor='crimson', zorder=5)
    plt.title('IPL 2024: Top 5 All-Rounders (Runs + Wickets*10)',fontsize=15, fontweight='bold')
    plt.xlabel('All Rounder Score', fontsize=13)
    plt.ylabel('Players' ,fontsize=13)
    plt.xticks( ha='right', color='blue', fontsize=12)
    plt.yticks(color='green', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7, color='red')
    plt.tight_layout()
    plt.show()
	
except Exception as err:
    print('Unable to connect to DB : ' , err)

finally:
    if(cur):
        cur.close()
    if(conn):
        conn.close()
