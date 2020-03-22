
'''
Module for testing functionality of import
'''



from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from datetime import date, timedelta, datetime


def generate_dataframe(self, data):
    # generate confirmed dataframe
    time = [];value = []#;confirmed_country=[];confirmed_province= []
    # c_col_value = list(self.confirmed_data.columns)
    for i in self.timeline:
        time.append(datetime.strptime(i, '%m/%d/%y'))
        value.append(data[i].sum())
    df = pd.DataFrame({'Timeline':time,'Covid-19 impact':value})
    return df

def generate_value(self, data):
    value = []
    for i in self.timeline:
        value.append(data[i].sum())
    return value[-1]


class Covid_Timeline_data():

    def __init__(self, updated_confirmed_timeline, updated_death_timeline, updated_recovered_timeline, timeline):
        self.confirmed_data = pd.read_csv(updated_confirmed_timeline)
        self.death_data = pd.read_csv(updated_death_timeline)
        self.recovered_data = pd.read_csv(updated_recovered_timeline)
        self.timeline = timeline

    def analyze_covid_spread(self):

        time = [];value = [];country= []
        col_value = list(self.confirmed_data.columns)
        for i in range(len(self.confirmed_data)):
            row_value = list(self.confirmed_data.iloc[i])
            D = dict(zip(col_value,row_value))
            time.extend(self.timeline)
            value.extend(D[t] for t in  self.timeline)
            country.extend(D['Country/Region'] for i in  range(len(self.timeline)))
        df = pd.DataFrame({'Timeline':time,'Covid-19 impact':value,'Country':country})
        df['Covid-19 impact'].replace({0:np.nan})
        fig = px.scatter(df, 
                         x="Timeline", 
                         y="Covid-19 impact", 
                         color = 'Country',
                         title = 'Spread of Covid-19 Infections Across Countries',
                         width=1000)
        fig.show()


    def analyze_covid_timelines(self):

       # generate confirmed dataframe
        confirmed_df = generate_dataframe(self,self.confirmed_data)

        # generate death dataframe
        death_df = generate_dataframe(self,self.death_data)

        # generate recovered dataframe
        recovered_df = generate_dataframe(self,self.recovered_data)

        # generate time series plot
        fig = make_subplots()

        fig.add_trace(
            go.Scatter(x=confirmed_df["Timeline"], 
                       y=confirmed_df["Covid-19 impact"], 
                       name = 'Infected'))

        fig.add_trace(
            go.Scatter(x=death_df["Timeline"], 
                       y=death_df["Covid-19 impact"], 
                       name = 'Deaths'))

        fig.add_trace(
            go.Scatter(x=recovered_df["Timeline"], 
                       y=recovered_df["Covid-19 impact"], 
                       name = 'Recovery'))

        fig.update_xaxes(title_text="Time")
        fig.update_yaxes(title_text="Amount Of People")
        fig.update_layout(height=500, 
                          width=800, 
                          title_text="Anlaysis of COVID-19 Over Time",
                           legend=dict(
                                        itemsizing = "constant",
                                        font=dict(
                                                    family="Courier New, monospace",
                                                    size=20,
                                                    color="black"
                                                )
                                    )
                        )

                 
        fig.show()
        print('================ Totals Report =====================================')
        print('== Information to {} on novel COVID-19 =========\n'.format(self.confirmed_data[self.confirmed_data.columns[-1]].name))
        print('Tota confirmed: {}\nTotal Deaths: {}\nTotal Recovered: {}\n'.format(generate_value(self, self.confirmed_data), generate_value(self,self.death_data), generate_value(self,self.recovered_data)))
        print('==================================================================')
