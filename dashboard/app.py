# Streamlit dashboard to visualse the data
# License:  MIT

import streamlit as st
import requests

st.set_page_config(page_title="Football Analytics", layout="wide")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """

st.title("Football Analytics")

teams = ["Arsenal", "Chelsea", "Liverpool"]
url = "http://model-server:7979"

league_tab, matches_tab, predictions_tab = st.tabs(["League", "Matches", "Predictions"])

with league_tab:
    league_con = st.container()
    st.write("### League Table")

with matches_tab:
    matches_con = st.container()
    st.write("### Matches")

with predictions_tab:
    predictions_con = st.container()
    st.write("### Predictions")
    select_home, select_away = predictions_con.columns(2)
    home_team = select_home.selectbox("Select Home Team", teams, key="h_team")
    away_team = select_away.selectbox("Select Away Team", teams, key="a_team")
    pred_request = {
            "home":str(home_team), 
            "away":str(away_team)
            }
    with st.spinner('Querying API...'):
        pred_output = requests.post(url, json = pred_request)
    st.write(pred_output.text)

