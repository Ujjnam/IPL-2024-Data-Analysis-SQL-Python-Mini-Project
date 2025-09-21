🏏 IPL 2024 Data Analysis: SQL + Python Mini Project.

	A beginner-friendly Oracle SQL & Python project to practice database design, complex analytical queries, business reporting, and data visualization using real IPL 2024 data. 

Perfect for SQL learners, Python beginners, and portfolio builders!

📊 Project Overview
This project loads IPL 2024 match, team, and player data into Oracle Database, runs 6 insightful analytical queries, and generates beautiful matplotlib visualizations to uncover trends like:

- 🏠 Do teams win more at home?
- 🎯 Does toss decision impact match outcome by venue?
- 🌟 Which teams & players dominate Player of the Match awards?
- 👑 How do captains perform — wins + personal impact?
- 💪 Who are the Top 5 All-Rounders (Batting + Bowling)?
- 🥇 Final Points Table based on wins

## 🗃️ File Structure

```
ipl-data-analysis/
│
├── data/
│   └── ipl_data_2024.xlsx          # Raw Excel data
│
├── sql/
│   ├── create_tables.sql           # DDL: Create TEAMS, PLAYERS, MATCHES
│   ├── insert_data.sql             # DML: Bulk insert using INSERT ALL
│   └── analysis_queries.sql        # 6 analytical queries with comments
│
├── python/
│   ├── 1_load_and_creation.py      # Reads Excel → creates Oracle tables
│   ├── 2_clean_load_to_oracle.py   # Cleans data (NaN → None) → bulk insert
│   ├── 3_fetch_and_visualize_1_home_advantage.py
│   ├── 3_fetch_and_visualize_2_toss_decision.py
│   ├── 3_fetch_and_visualize_3_potm_count.py
│   ├── 3_fetch_and_visualize_4_captain_perf.py
│   ├── 3_fetch_and_visualize_5_top_5_all.py
│   └── 3_fetch_and_visualize_6_points_table.py
│
├── plots/
│   ├── 1_Teams_performance_at_Home_Ground.png
│   ├── 2_Win_Percentage_by_Venue_and_Toss_Decision.png
│   ├── 3_Player_of_match_awards_by_Team.png
│   ├── 4_Captain_win_percentage.png
│   ├── 5_Top_5_AllRounders.png
│   └── 6_IPL_2024_Points_Table.png
│
└── README.md                       # You're here!
```

🚀 How to Run?
- Prerequisites
✅ Oracle Database (XE 21c or later recommended)
✅ Python 3.8+
✅ Libraries: oracledb, pandas, matplotlib, openpyxl

Steps
1. Set up Oracle DB
	- Ensure you can connect via: system/system@localhost:1521/xepdb1
	  (Modify connection string in Python files if needed)

2. Run Python Scripts (in order)
	- python/1_load_and_creation.py
	- python/2_clean_load_to_oracle.py
	- python/3_fetch_and_visualize_1_home_advantage.py
	- python/3_fetch_and_visualize_2_toss_decision.py
	- python/3_fetch_and_visualize_3_potm_count.py
	- python/3_fetch_and_visualize_4_captain_perf.py
	- python/3_fetch_and_visualize_5_top_5_all.py
	- python/3_fetch_and_visualize_6_points_table.py

3. View Queries
	- All queries saved in /sql folder

4. View Plots
	- All charts saved in /plots folder
	- Also displayed interactively during script run

🛠️ Skills Demonstrated

✅ SQL: Complex JOINs, CTEs, Window Functions (ROW_NUMBER, SUM OVER), Aggregations, Conditional Logic (CASE).
✅ Python: Data cleaning, Oracle DB connectivity (oracledb), Error handling.
✅ Pandas: DataFrame manipulation, SQL result ingestion, data type conversion.
✅ Matplotlib: Bar, Horizontal Bar, Grouped Bar, Lollipop charts — with colors, labels, grids.
✅ Data Storytelling: Turning raw data into business insights with visualizations.

🤝 Contributing

Found a bug? Want to add Query 7?
👉 Fork this repo, make improvements, and submit a Pull Request!

🙌 Acknowledgements

- IPL 2024 Official Data Sources
- Oracle Database Express Edition
- Matplotlib & Pandas communities

📬 Feedback / Questions?
	Open an Issue or DM me on LinkedIn — I’d love to hear how this helped you!






