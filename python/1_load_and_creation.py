import pandas as pd
import oracledb
import numpy as np

# 1.READ ALL SHEETS
df_teams = pd.read_excel('ipl_data_2024.xlsx' , sheet_name='teams' , header=0)
df_players = pd.read_excel('ipl_data_2024.xlsx' , sheet_name='players' , header=0)
df_matches = pd.read_excel('ipl_data_2024.xlsx' , sheet_name='matches' , header=0)


# 2.CONNECT TO ORACLE
connStr = 'system/system@localhost:1521/xepdb1'
conn = cur = None
try:
    conn = oracledb.connect(connStr)
    cur = conn.cursor()

# 3.CREATION OF TABLES
    sqlQuery = """ CREATE TABLE teams(team_name VARCHAR2(10) PRIMARY KEY,
                                      home_city VARCHAR2(20) UNIQUE NOT NULL,
                                      captain VARCHAR2(20) NOT NULL,
                                      coach VARCHAR2(20) NOT NULL,
                                      owner VARCHAR2(30) NOT NULL)"""
    cur.execute(sqlQuery)
    sqlQuery = """ CREATE TABLE player_name VARCHAR2(30) PRIMARY KEY,
    				team_name VARCHAR2(10) NOT NULL,
    				matches_played NUMBER,
    				innings NUMBER,
    				runs_scored NUMBER,
    				highest_score NUMBER,
    				batting_average NUMBER(5,2),
    				strike_rate NUMBER(6,2),
    				centuries NUMBER,
    				fifties NUMBER,
    				overs_bowled NUMBER, 
    				wickets_taken NUMBER,
    				bowling_average NUMBER(6,2),
    				economy_rate NUMBER(4,2))"""
    cur.execute(sqlQuery)

    sqlQuery = """ CREATE TABLE matches(match_id NUMBER PRIMARY KEY,
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
                     player_of_match VARCHAR2(30))"""
    cur.execute(sqlQuery)


except Exception as err:
    print('Unable to connect to DB : ' , err)
finally:
    if(cur):
        cur.close()
    if(conn):
        conn.close()