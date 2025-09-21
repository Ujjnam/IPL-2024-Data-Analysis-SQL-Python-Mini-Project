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

    sqlQuery = """ SELECT 
                        p.team_name,
                        COUNT(*) as total_potm
                   FROM players p INNER JOIN matches m
                   ON p.player_name = m.player_of_match
                   GROUP BY p.team_name
                   ORDER BY total_potm DESC """

    df = pd.read_sql(sqlQuery, conn)
    colors = ['lightgreen','crimson','seagreen','yellow','pink','skyblue','orange','grey','brown','red']
    explode = [0.1,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05]

    # PLOTTING

    plt.figure(figsize=(10,10))
    plt.pie(df['TOTAL_POTM'], labels=df['TEAM_NAME'],explode=explode, wedgeprops={'edgecolor':'black'},
            colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title('IPL 2024: Player of the Match Awards by Team' ,fontsize=16 ,fontweight='bold')
    plt.tight_layout()
    plt.show()

except Exception as err:
    print('Unable to connect to DB : ' , err)

finally:
    if(cur):
        cur.close()
    if(conn):
        conn.close()

