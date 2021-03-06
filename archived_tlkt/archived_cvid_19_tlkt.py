################################
# C O V I D 1 9  T O O L K I T #
################################

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns 
import statsmodels as sm
import folium as fl
from pathlib import Path
from sklearn.impute import SimpleImputer
sns.set()
# %matplotlib inline

import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
pd.options.plotting.backend



class Covid19_data():

    '''
    Covid19_data is a class which produces an object to explore daily data about Covid-19:

    pass through updated csv

    the class properties automatically clean the data

    the class methods graph the date in three types of graphs
    '''

    def __init__(self, updated_csv):
        self.df = pd.read_csv(updated_csv)
        self.normalized_data_confirmed = [value/self.df['Confirmed'].mean() + 10 for value in  self.df['Confirmed']]
        self.normalized_data_death = [value/self.df['Confirmed'].mean()+3 if value != 0  else value for value  in self.df['Deaths']]
        self.normalized_data_recovered = [value/self.df['Confirmed'].mean() + 3 if value != 0  else value for value  in self.df['Recovered']]
        self.hoverdata_confirmed = self.df['Country/Region'] + " - "+ ['Confirmed cases: ' + str(v) for v in self.df['Confirmed'].tolist()]
        self.hoverdata_death = self.df['Country/Region'] + " - "+ ['Death: ' + str(v) for v in self.df['Deaths'].tolist()]
        self.hoverdata_recovered = self.df['Country/Region'] + " - "+ ['Recovered: ' + str(v) for v in self.df['Recovered'].tolist()]


    def analyze_covid_global(self):

        '''
        Produce a global map that shows where COVID-19's geo location 

        Within each position, there is number of: Confirmed Infections // Deaths // Recovery
        '''
        
        fig = make_subplots()
        fig1 = go.Figure(data=go.Scattergeo(
                lon = self.df['Longitude'],
                lat = self.df['Latitude'],
            name = 'Confirmed cases',
                hovertext = self.hoverdata_confirmed,
                marker = dict(
                    size =  self.normalized_data_confirmed,
                    opacity = 0.5,
                    color = 'purple',
                    line = dict(
                        width=0,
                        color='rgba(102, 102, 102)'
                    ),
                ),
                ))

        fig2 = go.Figure(data=go.Scattergeo(
                lon = self.df['Longitude'],
                lat = self.df['Latitude'],
            name = 'Deaths',
                hovertext = self.hoverdata_death,
                marker = dict(
                    size =  self.normalized_data_death,
                    opacity = 0.5,
                    color = 'red',
                    line = dict(
                        width=0,
                        color='rgba(102, 102, 102)'
                    ),
                ),
                ))


        fig3= go.Figure(data=go.Scattergeo(
                lon = self.df['Longitude'],
                lat = self.df['Latitude'],
                hovertext = self.hoverdata_recovered,
            name = 'Recovered',
                marker = dict(
                    size =  self.normalized_data_recovered,
                    opacity = 0.5,
                    color = 'yellow',
                    line = dict(
                        width=0,
                        color='rgba(102, 102, 102)'
                    ),
                ),
                ))

        fig.add_trace(fig1.data[0])
        fig.add_trace(fig2.data[0])
        fig.add_trace(fig3.data[0])

        fig.update_layout(
                title = 'COVID-19 GLOBAL',
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


    def analyze_covid_distribution(self, category):

        '''
        Produce a pie chart focused on distribution of given parameter

        parameters are: Confirmed Infections // Deaths // Recovered
        '''

        fig = px.pie(self.df, 
                    values= category, 
                    names='Country/Region',
                    title= category + ' Rates Across Countries',
                    hover_data=['Province/State'], 
                    labels={'Province/State':'Province/State'})
        fig.update_traces(textposition='inside')
        fig.show()
        

    def analyze_covid_treemap(self, category):
        
        '''
        Produce a treemap focused on distribution of given parameter

        parameters are: Confirmed Infections // Deaths // Recovered
        '''

        self.df["world"] = "world" # root node
        fig = px.treemap(self.df, 
                                path=['world' , 'Country/Region', 'Province/State'], 
                                color = category,
                                color_continuous_scale=px.colors.sequential.Magenta,
                                title = category, 
                                values= category) 
        fig.show()


    '''
    Analyze country or state
    '''
    def analyze_country(self, country):

        country = self.df.loc[self.df['Country/Region'] == country]
        return country
    
    def analyze_state(self, state):

        state = self.df.loc[self.df['Province/State'] == state]
        return state


'''
timeline variable is a list of dates used to generate labels and is
functional cleaning the dataframes to be plotted on the timeseries charts

update_timeline function extends the list of the timeline to include days beyond the 20th 

update_timeline function does this by using the data_set date and the timeline list
to figure the amount of days between the last day in the timeline and the day in the dataset
and extends the timeline list to number of dates needed
'''



timeline = ['1/22/20', '1/23/20',
       '1/24/20', '1/25/20', '1/26/20', '1/27/20', '1/28/20', '1/29/20',
       '1/30/20', '1/31/20', '2/1/20', '2/2/20', '2/3/20', '2/4/20', '2/5/20',
       '2/6/20', '2/7/20', '2/8/20', '2/9/20', '2/10/20', '2/11/20', '2/12/20',
       '2/13/20', '2/14/20', '2/15/20', '2/16/20', '2/17/20', '2/18/20',
       '2/19/20', '2/20/20', '2/21/20', '2/22/20', '2/23/20', '2/24/20',
       '2/25/20', '2/26/20', '2/27/20', '2/28/20', '2/29/20', '3/1/20',
       '3/2/20', '3/3/20', '3/4/20', '3/5/20', '3/6/20', '3/7/20',
       '3/8/20', '3/9/20', '3/10/20', '3/11/20', '3/12/20',
       '3/13/20', '3/14/20', '3/15/20', '3/16/20', '3/17/20',
       '3/18/20', '3/19/20', '3/20/20'] 

def update_timeline(timeline, dataset_date):
    date_format = "%m/%d/%y"
    sdate = datetime.strptime('3/21/20', date_format)   # start date
    edate = datetime.strptime(dataset_date, date_format)   # end date

    delta = edate - sdate       # as timedelta
    # make a list of dates from timedelta
    d = []
    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        d.append(day)
    # make a list of converted datetime objects to str obj dates
    # and extend timeline list
    string_list = []
    for i in d:
        string_date = datetime.strftime(i, "%m/%d/%y" )
        string_list.append(string_date[1:])
    timeline.extend(string_list)
    del timeline[-1]
    return timeline
       
# these methods are abstractions to be called within the Covid_Timeline_data class.
# they generate necessary dateframes and values as needed for the timeline charts and printout

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

    '''
    Covid_Timeline_data is a class that generates a timeseries object to explore the 
    over all trends of Covid's spread between countries and over time
    '''

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
                         size='Covid-19 impact',
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
                       name = 'Infected',
                       line=dict(
                                  color='purple')))

        fig.add_trace(
            go.Scatter(x=death_df["Timeline"], 
                       y=death_df["Covid-19 impact"], 
                       name = 'Deaths',
                       line=dict(
                                  color='red')))

        fig.add_trace(
            go.Scatter(x=recovered_df["Timeline"], 
                       y=recovered_df["Covid-19 impact"], 
                       name = 'Recovery',
                       line=dict(
                                  color='yellow')))

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


# a class to generate predict models to assist in forecasting covid
# work in progress

class Covid19_Predictor():

    def __init__(self, updated_csv):
        pass








