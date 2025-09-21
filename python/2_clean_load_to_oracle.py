import pandas as pd
import oracledb
import numpy as np


# 1.READ ALL SHEETS
df_teams = pd.read_excel('ipl_data_2024.xlsx' , sheet_name='teams' , header=0)
df_players = pd.read_excel('ipl_data_2024.xlsx' , sheet_name='players' , header=0)
df_matches = pd.read_excel('ipl_data_2024.xlsx' , sheet_name='matches' , header=0)

# 2.CLEAN TEAMS
df_teams = df_teams.drop_duplicates().reset_index(drop=True)
for col in df_teams.columns:
    if(df_teams[col].dtype == 'object'):
        df_teams[col] = df_teams[col].str.strip()

# 3.CLEAN PLAYERS
df_players = df_players.drop_duplicates(subset=['player_name']).reset_index(drop=True)
for col in df_players.columns:
    if(df_players[col].dtype == 'object'):
        df_players[col] = df_players[col].str.strip()

# CONVERT COLUMNS TO NUMERIC
numeric_col_players = ['matches_played','innings','runs_scored','highest_score','batting_average','strike_rate',
                       'centuries','fifties','overs_bowled','wickets_taken','bowling_average','economy_rate']
for col in numeric_col_players:
    df_players[col] = pd.to_numeric(df_players[col] , errors='coerce')
    df_players[col] = df_players[col].replace({np.nan: None})

# 4.CLEAN MATCHES
df_matches = df_matches.drop_duplicates(subset=['match_date','team1','team2']).reset_index(drop=True)
for col in df_matches.columns:
    if(df_matches[col].dtype == 'object'):
        df_matches[col] = df_matches[col].str.strip()

# CONVERT COLUMNS TO NUMERIC
numeric_col_matches = ['match_id','result_margin']
for col in numeric_col_matches:
    df_matches[col] = pd.to_numeric(df_matches[col] , errors='coerce')

# 5.CONNECT TO ORACLE
connStr = 'system/system@localhost:1521/xepdb1'
conn = cur = None

try:
    conn = oracledb.connect(connStr)
    cur = conn.cursor()

    # 6.INSERTION OF DATA INTO TABLES

    data_to_insert_teams = df_teams.to_records(index=False).tolist()
    data_to_insert_players = df_players.to_records(index=False).tolist()
    df_matches['match_date'] = pd.to_datetime(df_matches['match_date'])
    df_matches['match_date'] = df_matches['match_date'].dt.strftime('%Y-%m-%d')
    data_to_insert_matches = df_matches.to_records(index=False).tolist()

    sqlQuery = """ INSERT INTO teams (team_name, home_city, captain, coach, owner) VALUES
                                      (:1, :2, :3, :4, :5)"""
    cur.executemany(sqlQuery , data_to_insert_teams)

    sqlQuery = """ INSERT INTO players (player_name, team_name, matches_played, innings, runs_scored, highest_score, batting_average,
                                        strike_rate, centuries, fifties , overs_bowled, wickets_taken, bowling_average, economy_rate) VALUES
                                       (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14)"""
    cur.executemany(sqlQuery , data_to_insert_players)

    sqlQuery = """ INSERT INTO matches (match_id, match_date, venue, match_city, team1, team2, toss_winner, toss_decision, winner,
                                        result_type, result_margin, player_of_match) VALUES
                                        (:1, to_date(:2 , 'YYYY-MM-DD'), :3, :4, :5, :6, :7, :8, :9, :10, :11, :12)"""
    cur.executemany(sqlQuery , data_to_insert_matches)
    conn.commit()

except Exception as err:
    print('Unable to connect to DB : ' , err)

finally:
    if(cur):
        cur.close()
    if(conn):
        conn.close()
