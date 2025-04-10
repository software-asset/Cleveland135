import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO

# Raw data input as a CSV string
data = """Team Name,Selection,Tier
Team1,Rory McIlroy,Tier 1
Team1,Jordan Spieth,Tier 2
Team1,Wyndham Clark,Tier 3
Team1,Brian Harman,Tier 4
Team1,Sahith Theegala,Tier 5
Team1,Keegan Bradley,Tier 6
Team10,Scottie Scheffler,Tier 1
Team10,Patrick Cantlay,Tier 2
Team10,Min Woo Lee,Tier 3
Team10,Sepp Straka,Tier 4
Team10,Patrick Reed,Tier 5
Team10,Tom Hoge,Tier 6
Team11,Ludvig Aberg,Tier 1
Team11,Shane Lowry,Tier 2
Team11,Tony Finau,Tier 3
Team11,Corey Conners,Tier 4
Team11,Matt Fitzpatrick,Tier 5
Team11,Keegan Bradley,Tier 6
Team12,Collin Morikawa,Tier 1
Team12,Cameron Smith,Tier 2
Team12,Sam Burns,Tier 3
Team12,Corey Conners,Tier 4
Team12,Matt Fitzpatrick,Tier 5
Team12,Justin Rose,Tier 6
Team13,Rory McIlroy,Tier 1
Team13,Viktor Hovland,Tier 2
Team13,Wyndham Clark,Tier 3
Team13,Jason Day,Tier 4
Team13,Matt Fitzpatrick,Tier 5
Team13,Keegan Bradley,Tier 6
Team14,Ludvig Aberg,Tier 1
Team14,Viktor Hovland,Tier 2
Team14,Min Woo Lee,Tier 3
Team14,Sepp Straka,Tier 4
Team14,Matt Fitzpatrick,Tier 5
Team14,Justin Rose,Tier 6
TEam15,Scottie Scheffler,Tier 1
TEam15,Shane Lowry,Tier 2
TEam15,Russell Henley,Tier 3
TEam15,Corey Conners,Tier 4
TEam15,Patrick Reed,Tier 5
TEam15,Lucas Glover,Tier 6
Team16,Rory McIlroy,Tier 1
Team16,Shane Lowry,Tier 2
Team16,Tony Finau,Tier 3
Team16,Cameron Young,Tier 4
Team16,Sahith Theegala,Tier 5
Team16,Billy Horschel,Tier 6
Team17,Ludvig Aberg,Tier 1
Team17,Jordan Spieth,Tier 2
Team17,Akshay Bhatia,Tier 3
Team17,Sepp Straka,Tier 4
Team17,Maverick McNealy,Tier 5
Team17,Kevin Yu,Tier 6
Team18,Scottie Scheffler,Tier 1
Team18,Viktor Hovland,Tier 2
Team18,Tony Finau,Tier 3
Team18,Robert Macintyre,Tier 4
Team18,Daniel Berger,Tier 5
Team18,Keegan Bradley,Tier 6
Team2,Rory McIlroy,Tier 1
Team2,Shane Lowry,Tier 2
Team2,Akshay Bhatia,Tier 3
Team2,Corey Conners,Tier 4
Team2,Sahith Theegala,Tier 5
Team2,Billy Horschel,Tier 6
Team3,Scottie Scheffler,Tier 1
Team3,Jordan Spieth,Tier 2
Team3,Russell Henley,Tier 3
Team3,Corey Conners,Tier 4
Team3,Patrick Reed,Tier 5
Team3,Keegan Bradley,Tier 6
Team4,Xander Schauffele,Tier 1
Team4,Viktor Hovland,Tier 2
Team4,Tony Finau,Tier 3
Team4,Adam Scott,Tier 4
Team4,Max Homa,Tier 5
Team4,Justin Rose,Tier 6
Team5,Scottie Scheffler,Tier 1
Team5,Tommy Fleetwood,Tier 2
Team5,Russell Henley,Tier 3
Team5,Sepp Straka,Tier 4
Team5,Harris English,Tier 5
Team5,Lucas Glover,Tier 6
Team6,Ludvig Aberg,Tier 1
Team6,Cameron Smith,Tier 2
Team6,Russell Henley,Tier 3
Team6,Byeong-Hun An,Tier 4
Team6,Matt Fitzpatrick,Tier 5
Team6,Billy Horschel,Tier 6
Team7,Rory McIlroy,Tier 1
Team7,Patrick Cantlay,Tier 2
Team7,Min Woo Lee,Tier 3
Team7,Jason Day,Tier 4
Team7,Sahith Theegala,Tier 5
Team7,Michael Kim,Tier 6
Team8,Scottie Scheffler,Tier 1
Team8,Shane Lowry,Tier 2
Team8,Wyndham Clark,Tier 3
Team8,Robert Macintyre,Tier 4
Team8,Maverick McNealy,Tier 5
Team8,J.J. Spaun,Tier 6
Team9,Scottie Scheffler,Tier 1
Team9,Patrick Cantlay,Tier 2
Team9,Dustin Johnson,Tier 3
Team9,Jason Day,Tier 4
Team9,Sahith Theegala,Tier 5
Team9,Justin Rose,Tier 6"""

# Prepare data
df = pd.read_csv(StringIO(data))
df['Team Name'] = df['Team Name'].str.strip().str.upper()

st.title("🏌️ Golf Pool Simulator Dashboard")
st.markdown("Simulate outcomes, compare teams, and explore live pool analytics.")

# Sidebar scoring templates
scoring_template = st.sidebar.selectbox("Choose a scoring model", ["Manual Input", "Top 10 Bonus", "Cut Penalty", "Flat Points"])

unique_players = sorted(df['Selection'].unique())
player_scores = {}

if scoring_template == "Manual Input":
    st.sidebar.header("🧮 Player Scoring")
    for player in unique_players:
        player_scores[player] = st.sidebar.number_input(f"{player}", min_value=0, max_value=100, value=0, step=1)
elif scoring_template == "Top 10 Bonus":
    top_10 = st.sidebar.multiselect("Select Top 10 Finishers", unique_players)
    for player in unique_players:
        player_scores[player] = 20 if player in top_10 else 5
elif scoring_template == "Cut Penalty":
    made_cut = st.sidebar.multiselect("Select Players Who Made The Cut", unique_players)
    for player in unique_players:
        player_scores[player] = 15 if player in made_cut else 0
elif scoring_template == "Flat Points":
    for player in unique_players:
        player_scores[player] = 10

# Apply scores
df['Score'] = df['Selection'].map(player_scores)

# Team total scores
team_scores = df.groupby('Team Name')['Score'].sum().reset_index()
team_scores = team_scores.sort_values(by='Score', ascending=False).reset_index(drop=True)
team_scores.index += 1

# Leaderboard
st.header("🏆 Simulated Team Leaderboard")
st.table(team_scores.rename(columns={"Score": "Total Points"}))

# What-if scenario
st.header("🔮 What-If Scenario Simulator")
sim_player = st.selectbox("Pick a player to simulate a different outcome", unique_players)
sim_score = st.slider(f"Assign a new score to {sim_player}", 0, 100, player_scores[sim_player])
sim_df = df.copy()
sim_df.loc[sim_df['Selection'] == sim_player, 'Score'] = sim_score
sim_results = sim_df.groupby('Team Name')['Score'].sum().reset_index().sort_values(by='Score', ascending=False).reset_index(drop=True)
sim_results.index += 1
st.subheader(f"Leaderboard with {sim_player} scoring {sim_score} pts")
st.table(sim_results.rename(columns={"Score": "Total Points"}))

# Team comparison tool
st.header("📊 Team Comparison Tool")
team1 = st.selectbox("Compare Team 1", sorted(df['Team Name'].unique()), key="comp1")
team2 = st.selectbox("Compare Team 2", sorted(df['Team Name'].unique()), key="comp2")
t1 = df[df['Team Name'] == team1].sort_values('Tier')
t2 = df[df['Team Name'] == team2].sort_values('Tier')
st.subheader(f"{team1} Picks vs {team2}")
st.columns(2)[0].table(t1[['Tier', 'Selection', 'Score']].reset_index(drop=True))
st.columns(2)[1].table(t2[['Tier', 'Selection', 'Score']].reset_index(drop=True))

# Pick popularity heatmap
st.header("🔥 Player Pick Popularity Heatmap")
pivot = pd.pivot_table(df, index='Selection', columns='Tier', aggfunc='size', fill_value=0)
fig, ax = plt.subplots(figsize=(12, 14))
sns.heatmap(pivot, cmap="RdYlGn_r", annot=True, fmt='d', linewidths=0.5, ax=ax)
ax.set_title("Heatmap of Player Picks per Tier")
st.pyplot(fig)

# Download CSV
st.download_button("📥 Download Leaderboard as CSV", team_scores.rename(columns={"Score": "Total Points"}).to_csv(index=False), file_name="leaderboard.csv")

# Team viewer
st.header("🔎 Team Detail Viewer")
selected_team = st.selectbox("Select a team to view picks", sorted(df['Team Name'].unique()), key="teamview")
team_detail = df[df['Team Name'] == selected_team].sort_values('Tier')
st.subheader(f"Picks and Scores for {selected_team}")
st.table(team_detail[['Tier', 'Selection', 'Score']].reset_index(drop=True))
