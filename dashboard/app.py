# Streamlit dashboard to visualse the data
# License:  MIT
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import requests
import json
import time

st.set_page_config(page_title="Football Analytics", layout="wide")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.image("logos/football-logo.jpg", width=400)
historic_data = pd.read_csv("data/premireleague.csv")

# convert the 'Date' column to datetime format
historic_data['date']= pd.to_datetime(historic_data['date'],format = '%Y-%m-%d').dt.date

min_date = historic_data["date"].min()
max_date = historic_data["date"].max()

historic_data[['home_goals', 'away_goals']] = historic_data['result_full'].str.split(pat='-', expand=True)
historic_data['home_goals'] = historic_data['home_goals'].astype('int')
historic_data['away_goals'] = historic_data['away_goals'].astype('int')

# Create a new empty column 'test_result'
historic_data['home_win'] = 0
historic_data['away_win'] = 0
historic_data['Draw'] = 0


# Iterate over each row of the dataframe
for index, row in historic_data.iterrows():
    # Get the values of column1 and column2 for the current row
    value1 = row['home_goals']
    value2 = row['away_goals']

    if value1 > value2:
            historic_data.at[index, 'home_win'] = 1
    elif value1 < value2:
            historic_data.at[index, 'away_win'] = 1
    else:
            historic_data.at[index, 'Draw'] = 1

url = "http://models:7979"

def logo_selector(team_selection):
        if team_selection == "Blackpool":
                logo = "logos/blackpool.png"
        elif team_selection == "Liverpool":
                logo = "logos/liverpool.png"
        elif team_selection == "Manchester United":
                logo = "logos/manchester_united.png"
        elif team_selection == "Stoke City":
                logo = "logos/stokecity.png"
        elif team_selection == "Fulham":
                logo = "logos/fulham.png"
        elif team_selection == "Blackburn Rovers":
                logo = "logos/BlackburnRovers.jpg"
        elif team_selection == "Manchester City":
                logo = "logos/Manchester_City.jpg"
        elif team_selection == "Sunderland":
                logo = "logos/sunderland.png"
        elif team_selection == "Bolton Wanderers":
                logo = "logos/bolton_wanderers.png"
        elif team_selection == "Arsenal":
                logo = "logos/Arsenal.png"
        elif team_selection == "Birmingham City":
                logo = "logos/birminghamcity.png"
        elif team_selection == "Tottenham Hotspur":
                logo = "logos/Tottenham_Hotspur.png"
        elif team_selection == "West Bromwich Albion":
                logo = "logos/West_Bromwich_Albion.png"
        elif team_selection == "West Ham United":
                logo = "logos/West_Ham_United.png"
        elif team_selection == "Aston Villa":
                logo = "logos/Aston_Villa.png"
        elif team_selection == "Everton":
                logo = "logos/Everton.png"
        elif team_selection == "Newcastle United":
                logo = "logos/Newcastle_United.png"
        elif team_selection == "Wigan Athletic":
                logo = "logos/Wigan_Athletic.png"
        elif team_selection == "Wolverhampton Wanderers":
                logo = "logos/Wolverhampton_Wanderers.png"
        elif team_selection == "Chelsea":
                logo = "logos/Chelsea.png"
        elif team_selection == "Swansea City":
                logo = "logos/Swansea_City.png"
        elif team_selection == "Queens Park Rangers":
                logo = "logos/Queens_Park_Rangers.png"
        elif team_selection == "Norwich City":
                logo = "logos/Norwich_City.png"
        elif team_selection == "Reading":
                logo = "logos/Reading.png"
        elif team_selection == "Southampton":
                logo = "logos/Southampton.png"
        elif team_selection == "Crystal Palace":
                logo = "logos/Crystal_Palace.png"
        elif team_selection == "Cardiff City":
                logo = "logos/Cardiff_city.png"
        elif team_selection == "Hull City":
                logo = "logos/Hull_City.png"
        elif team_selection == "Burnley":
                logo = "logos/Burnley.png"
        elif team_selection == "Leicester City":
                logo = "logos/Leicester_City.png"
        elif team_selection == "Watford":
                logo = "logos/Watford.jpg"
        elif team_selection == "AFC Bournemouth":
                logo = "logos/AFC_Bournemouth.png"
        elif team_selection == "Middlesbrough":
                logo = "logos/Middlesbrough.png"
        elif team_selection == "Brighton and Hove Albion":
                logo = "logos/Brighton_and_HoveAlbion.png"
        elif team_selection == "Huddersfield Town":
                logo = "logos/Huddersfield_Town.png"
        elif team_selection == "Sheffield United":
                logo = "logos/Sheffield_United.png"
        elif team_selection == "Leeds United":
                logo = "logos/Leeds_United.png"
        return logo


filters = st.expander("Filters")
start_date, end_date = filters.columns(2)
start = start_date.date_input("Select Start Date",value=min_date, min_value=min_date,max_value=max_date, key="s_date")
end = end_date.date_input("Select End Date",value=max_date,min_value=min_date,max_value=max_date, key="e_date")


league_tab, about_tab = st.tabs(["League","About Us"])
with league_tab:
    league_con = st.container()
    st.write("### League Table")



    solo_view_tab, comparison_view_tab = st.tabs(['Solo View', 'Comparison View'])

    with solo_view_tab:


        teams_container = st.container()
        team_select = teams_container.selectbox("Select Team",pd.unique(historic_data['home_team']),key = 't_team_s')
        col_1,col_2,col_3 = teams_container.columns(3)
        team_logo = col_2.image(logo_selector(team_select),width = 400)
        team_data= historic_data.loc[(historic_data['home_team'] == str(team_select))].loc[(historic_data['date'] >= start) & (historic_data['date'] <= end),['home_win','away_win','Draw','home_goals','home_shots','home_shots_on_target','home_tackles','home_clearances','home_corners','home_fouls_conceded','home_offsides','home_passes','home_possession','home_red_cards','home_touches','home_yellow_cards']].sum()
        total_matches =team_data[['away_win','home_win','Draw']].sum()
        total_matches = pd.Series(total_matches, index=['Matches'])
        team_data = pd.concat([team_data, total_matches]).reindex(['Matches','home_win','away_win','Draw','home_goals','home_shots','home_shots_on_target','home_tackles','home_clearances','home_corners','home_fouls_conceded','home_offsides','home_passes','home_possession','home_red_cards','home_touches','home_yellow_cards'])
        team_data = pd.DataFrame(team_data)
        team_data.columns = ['Stats']
        team_data.rename(index = {'home_win':'Wins',
                                                'away_win':'Losses',
                                                'home_goals':'Goals Scored',
                                                'home_clearances':'Clearances',
                                                'home_corners': 'Corners',
                                                'home_fouls_conceded':'Fouls Conceded',
                                                'home_offsides':'Offsides',
                                                'home_passes':'Passes',
                                                'home_possession':'Posession',
                                                'home_red_cards':'Red Cards',
                                                'home_shots':'Shots',
                                                'home_shots_on_target':'Shots On Target',
                                                'home_tackles':'Tackles',
                                                'home_touches':'Touches',
                                                'home_yellow_cards':'Yellow Cards'}, inplace = True)
        team_table = teams_container.table(team_data.astype(int))

        st.write('---')
        st.write('#### Previous Match Records')
        matches_container = st.container()
        matches_data = historic_data.loc[(historic_data['home_team'] == str(team_select))].loc[(historic_data['date'] >= start) & (historic_data['date'] <= end),['season','date','away_team','result_full','link_match']]
        matches_pdata = pd.DataFrame(matches_data)
        # matches_table = matches_container.table(matches_pdata)


        matches_container.dataframe(
                        matches_pdata,
                        column_config={
                                "link_match": st.column_config.LinkColumn(
                                "Match Link",
                                validate="^https://[a-z]+\.streamlit\.app$",
                                max_chars=100,
                                ),
                        },
                        hide_index=True,
                        use_container_width=True
                        )


        st.write('---')
        st.write('#### Performance')
        
        performance_select = st.selectbox("Select Metric",['Wins','Losses','Draws','Goals','Shots','Shots On Target','Tackles','Clearances','Corners','Fouls Conceded','Offsides','Passes','Possession','Red Cards','Touches','Yellow Cards'],key = 't_perforamce_s')


        

        team_data_filtered = historic_data.loc[(historic_data['home_team'] == str(team_select))].loc[(historic_data['date'] >= start) & (historic_data['date'] <= end),['date','home_win','away_win','Draw','home_goals','home_shots','home_shots_on_target','home_tackles','home_clearances','home_corners','home_fouls_conceded','home_offsides','home_passes','home_possession','home_red_cards','home_touches','home_yellow_cards']]
        # Group the data by date and calculate the cumulative sum
        team_data_filtered_grouped = team_data_filtered.groupby('date').sum().reset_index()
        
        if performance_select == 'Wins':
                y_var = team_data_filtered_grouped['home_win']
        elif performance_select == 'Losses':
                y_var = team_data_filtered_grouped['away_win']
        elif performance_select == 'Draws':
                y_var = team_data_filtered_grouped['Draw']      
        elif performance_select == 'Goals':
                y_var = team_data_filtered_grouped['home_goals']
        elif performance_select == 'Shots':
                y_var = team_data_filtered_grouped['home_shots']
        elif performance_select == 'Shots On Target':
                y_var = team_data_filtered_grouped['home_shots_on_target']
        elif performance_select == 'Tackles':
                y_var = team_data_filtered_grouped['home_tackles']
        elif performance_select == 'Clearances':
                y_var = team_data_filtered_grouped['home_clearances']
        elif performance_select == 'Corners':
                y_var = team_data_filtered_grouped['home_corners']
        elif performance_select == 'Fouls Conceded':
                y_var = team_data_filtered_grouped['home_fouls_conceded']
        elif performance_select == 'Offsides':
                y_var = team_data_filtered_grouped['home_offsides']
        elif performance_select == 'Passes':
                y_var = team_data_filtered_grouped['home_passes']
        elif performance_select == 'Possession':
                y_var = team_data_filtered_grouped['home_possession']
        elif performance_select == 'Red Cards':
                y_var = team_data_filtered_grouped['home_red_cards']
        elif performance_select == 'Touches':
                y_var = team_data_filtered_grouped['home_touches']
        elif performance_select == 'Yellow Cards':
                y_var = team_data_filtered_grouped['home_yellow_cards']

        # Create a line plot for home_data_filtered_grouped
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=team_data_filtered_grouped['date'], y=y_var.cumsum()))

        # Update the layout and legend
        fig.update_layout(
        title=str(performance_select) + ' over Time',
        xaxis_title='Date',
        yaxis_title=str(performance_select),
        legend_title='Line Type'
        )

        # Change the hover labels
        fig.update_traces(hovertemplate='Date: %{x}<br>Count: %{y}')

        # Display the line plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)


        
    with comparison_view_tab:
        home_select, away_select = st.columns(2)
        home_team_selection = home_select.selectbox("Select Home Team",pd.unique(historic_data['home_team']),key = 'h_team_s')
        away_team_selection = away_select.selectbox("Select Away Team",pd.unique(historic_data['away_team']),key = 'a_team_s')

        col1,col2,col3,col4,col5,col6 = st.columns(6)
        home_logo = col2.image(logo_selector(home_team_selection),width =400)
        away_logo = col5.image(logo_selector(away_team_selection),width =400)

        home_select_data,away_select_data = st.columns(2)
        home_data = historic_data.loc[(historic_data['home_team'] == str(home_team_selection))& (historic_data['away_team'] == str(away_team_selection))].loc[(historic_data['date'] >= start) & (historic_data['date'] <= end),['home_win','away_win','Draw','home_goals','home_shots','home_shots_on_target','home_tackles','home_clearances','home_corners','home_fouls_conceded','home_offsides','home_passes','home_possession','home_red_cards','home_touches','home_yellow_cards']].sum()
        total_matches_home =home_data[['away_win','home_win','Draw']].sum()
        total_matches_home = pd.Series(total_matches_home, index=['Matches'])
        home_data = pd.concat([home_data, total_matches_home]).reindex(['Matches','home_win','away_win','Draw','home_goals','home_shots','home_shots_on_target','home_tackles','home_clearances','home_corners','home_fouls_conceded','home_offsides','home_passes','home_possession','home_red_cards','home_touches','home_yellow_cards'])
        home_data = pd.DataFrame(home_data)
        home_data.columns = ['Stats']
        home_data.rename(index = {'home_win':'Wins',
                                            'away_win':'Losses',
                                            'home_goals':'Goals Scored',
                                            'home_clearances':'Clearances',
                                            'home_corners': 'Corners',
                                            'home_fouls_conceded':'Fouls Conceded',
                                            'home_offsides':'Offsides',
                                            'home_passes':'Passes',
                                            'home_possession':'Posession',
                                            'home_red_cards':'Red Cards',
                                            'home_shots':'Shots',
                                            'home_shots_on_target':'Shots On Target',
                                            'home_tackles':'Tackles',
                                            'home_touches':'Touches',
                                            'home_yellow_cards':'Yellow Cards'}, inplace = True)
        home_table = home_select_data.table(home_data.astype(int))


        col1,col2,col3 = away_select.columns(3)

        away_data = historic_data.loc[(historic_data['home_team'] == str(home_team_selection))&(historic_data['away_team'] == str(away_team_selection))].loc[(historic_data['date'] >= start) & (historic_data['date'] <= end),['away_win','home_win','Draw','away_goals','away_shots','away_shots_on_target','away_tackles','away_clearances','away_corners','away_fouls_conceded','away_offsides','away_passes','away_possession','away_red_cards','away_touches','away_yellow_cards']].sum()
        total_matches_away = away_data[['away_win','home_win','Draw']].sum()
        total_matches_away = pd.Series(total_matches_away, index=['Matches'])
        away_data = pd.concat([away_data, total_matches_away]).reindex(['Matches','away_win','home_win','Draw','away_goals','away_shots','away_shots_on_target','away_tackles','away_clearances','away_corners','away_fouls_conceded','away_offsides','away_passes','away_possession','away_red_cards','away_touches','away_yellow_cards'])
        away_data = pd.DataFrame(away_data)
        away_data.columns = ['Stats']
        away_data.rename(index = {'away_win':'Wins',
                                            'home_win':'Losses',
                                            'away_goals':'Goals Scored',
                                            'away_clearances':'Clearances',
                                            'away_corners': 'Corners',
                                            'away_fouls_conceded':'Fouls Conceded',
                                            'away_offsides':'Offsides',
                                            'away_passes':'Passes',
                                            'away_possession':'Posession',
                                            'away_red_cards':'Red Cards',
                                            'away_shots':'Shots',
                                            'away_shots_on_target':'Shots On Target',
                                            'away_tackles':'Tackles',
                                            'away_touches':'Touches',
                                            'away_yellow_cards':'Yellow Cards'}, inplace = True)

        away_table = away_select_data.table(away_data.astype(int))



        st.write('---')
        st.write('#### Previous Match Records')
        matches_container_comp = st.container()
        matches_data_comp = historic_data.loc[(historic_data['home_team'] == str(home_team_selection))&(historic_data['away_team'] == str(away_team_selection))].loc[(historic_data['date'] >= start) & (historic_data['date'] <= end),['season','date','home_team','away_team','result_full','link_match']]
        matches_pdata_comp = pd.DataFrame(matches_data_comp)


        matches_container_comp.dataframe(
                        matches_pdata_comp,
                        column_config={
                                "link_match": st.column_config.LinkColumn(
                                "Match Link",
                                validate="^https://[a-z]+\.streamlit\.app$",
                                max_chars=100,
                                ),
                        },
                        hide_index=True,
                        use_container_width=True
                        )


        st.write('---')
        st.write('#### Performance')
        
        performance_select_comp = st.selectbox("Select Metric",['Wins','Losses','Draws','Goals','Shots','Shots On Target','Tackles','Clearances','Corners','Fouls Conceded','Offsides','Passes','Possession','Red Cards','Touches','Yellow Cards'],key = 'h_perforamce_s')

        home_data_filtered = historic_data.loc[(historic_data['home_team'] == str(home_team_selection))].loc[(historic_data['date'] >= start) & (historic_data['date'] <= end),['date','home_win','away_win','Draw','home_goals','home_shots','home_shots_on_target','home_tackles','home_clearances','home_corners','home_fouls_conceded','home_offsides','home_passes','home_possession','home_red_cards','home_touches','home_yellow_cards']]
        away_data_filtered = historic_data.loc[(historic_data['away_team'] == str(away_team_selection))].loc[(historic_data['date'] >= start) & (historic_data['date'] <= end),['date','away_win','home_win','Draw','away_goals','away_shots','away_shots_on_target','away_tackles','away_clearances','away_corners','away_fouls_conceded','away_offsides','away_passes','away_possession','away_red_cards','away_touches','away_yellow_cards']]
        
        # Group the data by date and calculate the cumulative sum
        home_data_filtered_grouped = home_data_filtered.groupby('date').sum().reset_index()
        away_data_filtered_grouped = away_data_filtered.groupby('date').sum().reset_index()
        
        if performance_select_comp == 'Wins':
                h_y_var = home_data_filtered_grouped['home_win']
                a_y_var = away_data_filtered_grouped['away_win']
        elif performance_select_comp == 'Losses':
                h_y_var = home_data_filtered_grouped['away_win']
                a_y_var = away_data_filtered_grouped['away_win']
        elif performance_select_comp == 'Draws':
                h_y_var = home_data_filtered_grouped['Draw']
                a_y_var = away_data_filtered_grouped['Draw']      
        elif performance_select_comp == 'Goals':
                h_y_var = home_data_filtered_grouped['home_goals']
                a_y_var = away_data_filtered_grouped['away_goals']
        elif performance_select_comp == 'Shots':
                h_y_var = home_data_filtered_grouped['home_shots']
                a_y_var = away_data_filtered_grouped['away_shots']
        elif performance_select_comp == 'Shots On Target':
                h_y_var = home_data_filtered_grouped['home_shots_on_target']
                a_y_var = away_data_filtered_grouped['away_shots_on_target']
        elif performance_select_comp == 'Tackles':
                h_y_var = home_data_filtered_grouped['home_tackles']
                a_y_var = away_data_filtered_grouped['away_tackles']
        elif performance_select_comp == 'Clearances':
                h_y_var = home_data_filtered_grouped['home_clearances']
                a_y_var = away_data_filtered_grouped['away_clearances']
        elif performance_select_comp == 'Corners':
                h_y_var = home_data_filtered_grouped['home_corners']
                a_y_var = away_data_filtered_grouped['away_corners']
        elif performance_select_comp == 'Fouls Conceded':
                h_y_var = home_data_filtered_grouped['home_fouls_conceded']
                a_y_var = away_data_filtered_grouped['away_fouls_conceded']
        elif performance_select_comp == 'Offsides':
                h_y_var = home_data_filtered_grouped['home_offsides']
                a_y_var = away_data_filtered_grouped['away_offsides']
        elif performance_select_comp == 'Passes':
                h_y_var = home_data_filtered_grouped['home_passes']
                a_y_var = away_data_filtered_grouped['away_passes']
        elif performance_select_comp == 'Possession':
                h_y_var = home_data_filtered_grouped['home_possession']
                a_y_var = away_data_filtered_grouped['away_possession']
        elif performance_select_comp == 'Red Cards':
                h_y_var = home_data_filtered_grouped['home_red_cards']
                a_y_var = away_data_filtered_grouped['away_red_cards']
        elif performance_select_comp == 'Touches':
                h_y_var = home_data_filtered_grouped['home_touches']
                a_y_var = away_data_filtered_grouped['away_touches']
        elif performance_select_comp == 'Yellow Cards':
                h_y_var = home_data_filtered_grouped['home_yellow_cards']
                a_y_var = away_data_filtered_grouped['away_yellow_cards']


        # Create a line plot for home_data_filtered_grouped
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=home_data_filtered_grouped['date'], y=h_y_var.cumsum(), name='Home'))

        # Create a line plot for away_data_filtered_grouped
        fig.add_trace(go.Scatter(x=away_data_filtered_grouped['date'], y=a_y_var.cumsum(), name='Away'))

        # Update the layout and legend
        fig.update_layout(
        title=str(performance_select_comp) + ' over Time',
        xaxis_title='Date',
        yaxis_title=str(performance_select_comp),
        legend_title='Line Type'
        )

        # Change the hover labels
        fig.update_traces(hovertemplate='Date: %{x}<br>Count: %{y}')

        # Display the line plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)



        st.write('---')
        st.write('#### Predictions')
        predictions_con = st.container()
        pred_request = {
                "home":str(home_team_selection),
                "away":str(away_team_selection)
                }

        with st.spinner('Querying API...'):
            pred_output = requests.post(url, json=pred_request)

        response_data = json.loads(pred_output.text)
        home_goal,content,away_goal = st.columns(3)

        col1_h,col2_h,col3_h  = home_goal.columns(3)
        h_goal_team = col1_h.title(str(home_team_selection))
        h_goal_display = col3_h.title(response_data["Home Goals"])
        col1_a,col2_a,col3_a = away_goal.columns(3) 
        a_goal_display = col2_a.title(response_data["Away Goals"])
        a_goal_team = col3_a.title(str(away_team_selection))
        col1_c,col2_c = content.columns(2)
        content_display = col2_c.title(":blue[-]")
        
        st.write('### Probabilities')
        prob_container = st.container()
        prob_container.write(str(str('#### %Win: ') + str(response_data["Win"])))
        prob_container.write(str(str('#### %Draw: ') + str(response_data["Draw"])))
        prob_container.write(str(str('#### %Lose: ') + str(response_data["Lose"])))
        prob_container.write(str(str('#### %Scoreline: ') + str(response_data["Prob of Scoreline"])))

        #matches_ = pd.DataFrame([response_data['home_goals']]).head()

        #prob_container.dataframe(
        #                matches_,
        #                hide_index=True,
        #                use_container_width=True
        #                )

        #pred_table = pd.DataFrame([pred_output.json()])
        #st.table(pred_table)
        



with about_tab:
    matches_con = st.container()
    st.write("### About")
    st.write("This investigation aims to analyse the English Premier League and demonstrate how a microservice architecture lets us pull from a range of languages and frameworks to deliver a cohesive solution. It is based on 2021/2022 season, but work is under way to develop a system to incrementally update a model on a season-by-season basis. We are using Bayesian models to produce simulations e.g. average outcome of 5 000 games between Liverpool and Man City, or 1-in-100 game event between Burnley and Spurs.")
