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
st.markdown("Simulate outcomes by assigning points to each player, and see how team standings would change.")

# Sidebar: Player scoring input
st.sidebar.header("🧮 Player Scoring")
unique_players = sorted(df['Selection'].unique())
player_scores = {}

for player in unique_players:
    player_scores[player] = st.sidebar.number_input(f"{player}", min_value=0, max_value=100, value=0, step=1)

# Apply scores to the main dataframe
df['Score'] = df['Selection'].map(player_scores)

# Calculate team total scores
team_scores = df.groupby('Team Name')['Score'].sum().reset_index()
team_scores = team_scores.sort_values(by='Score', ascending=False).reset_index(drop=True)
team_scores.index += 1  # start ranking from 1

# Display leaderboard
st.header("🏆 Simulated Team Leaderboard")
st.table(team_scores.rename(columns={"Score": "Total Points"}))

# Optionally: Show individual team picks and scores
selected_team = st.selectbox("Select a team to view details", sorted(df['Team Name'].unique()))
team_detail = df[df['Team Name'] == selected_team].sort_values('Tier')

st.subheader(f"Picks and Scores for {selected_team}")
st.table(team_detail[['Tier', 'Selection', 'Score']].reset_index(drop=True))
