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

    sqlQuery = """ WITH venue_filtered AS
                        (SELECT 
                            venue,
                            toss_decision,
                            COUNT(*) AS total_matches,
                            SUM(CASE
                                    WHEN toss_winner=winner THEN 1 ELSE 0 END
                                )AS wins_after_decision
                        FROM matches
                        GROUP BY venue,toss_decision
                        ORDER BY venue,toss_decision
                        )
                    SELECT 
                        venue,
                        toss_decision,
                        total_matches ,
                        wins_after_decision,
                        ROUND((wins_after_decision/total_matches)*100,2) || '%' AS win_percentage
                    FROM venue_filtered
                    ORDER BY venue """

    df = pd.read_sql(sqlQuery , conn)
    df['WIN_PERCENTAGE'] = df['WIN_PERCENTAGE'].str.replace('%','')
    df['WIN_PERCENTAGE'] = pd.to_numeric(df['WIN_PERCENTAGE'] ,errors='coerce')

    df_pivot = pd.pivot(
                        df,
                        index = 'VENUE',
                        columns = 'TOSS_DECISION',
                        values = 'WIN_PERCENTAGE')
    df_pivot = df_pivot.fillna(0.00)

    # PLOTTING
	
    df_pivot.plot(kind='bar',figsize=(16,8))
    plt.title('Win Percentage by Venue and Toss Decision',fontsize=16)
    plt.xlabel('Venue',fontsize=12)
    plt.ylabel('Win Percentage(%)',fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


except Exception as err:
    print('Unable to connect to DB : ' , err)

finally:
    if(cur):
        cur.close()
    if(conn):
        conn.close()
