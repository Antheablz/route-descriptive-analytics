#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from yaml import safe_load
import matplotlib.pyplot as plt
import numpy as np
import sys

"""
Created on Wed Feb 8 14:44:33 2023
Based on: https://www.kaggle.com/datasets/arbazmohammad/world-airports-and-airlines-datasets
Sample input: --AIRLINES="airlines.yaml" --AIRPORTS="airports.yaml" --ROUTES="routes.yaml" --QUESTION="q1" --GRAPH_TYPE="bar"
@author: rivera
@author: Anthea Blais V00959149
"""

#add doc strings before submitting 
def main():
    """ main function, gets command line inputs and goes to correct functions based on given question
    """
     #small error handling incase not enough command line input was given
    if len(sys.argv) <= 1:
          print("error please send in a question number!")
    else:    
        #stores command line input (question number and graph type) in a variable. 
        question = sys.argv[4]
        graphType = sys.argv[5]
        #opens files and turns each into a dataframe
        airlines_df = pd.DataFrame(data=openYAMLfile(file="airlines.yaml"))
        airports_df = pd.DataFrame(data=openYAMLfile(file="airports.yaml"))
        routes_df = pd.DataFrame(data=openYAMLfile(file="routes.yaml"))
      
         #goes to the correct function to answer question based on the question number
        if "q1" in question:
              question1(airlines_df=airlines_df, airports_df=airports_df, routes_df=routes_df,graph=graphType)
              
        elif "q2" in question:
                question2(airlines_df=airlines_df, airports_df=airports_df, routes_df=routes_df,graph=graphType)
                
        elif "q3" in question:
             question3(airlines_df=airlines_df, airports_df=airports_df, routes_df=routes_df,graph=graphType)
             
        elif "q4" in question:
             question4(airlines_df=airlines_df, airports_df=airports_df, routes_df=routes_df,graph=graphType)
             
        elif "q5" in question:
             question5(airlines_df=airlines_df, airports_df=airports_df, routes_df=routes_df,graph=graphType)
        
def question1(airlines_df, airports_df, routes_df, graph)-> None:
     """ generates the asnwer to question 1.

          Parameters
            ----------
               airlines_df: dataframe, required
                    dataframe generated from the airlines.yaml file
               airports_df: dataframe, required
                    dataframe generated from the airports.yaml file
               routes_df: datafram, required
                    dataframe generated from the routes.yaml file
               graph: str, required
                    the type of graph that will be generated in the pdf
     """
     #separate the columns of each dataframe, and drop unneeded columns
     airlines_df = pd.json_normalize(airlines_df['airlines'])
     airlines_df.drop(['airline_country'],inplace=True,axis=1)
     airlines_df = airlines_df.sort_values(['airline_name'], ascending=True)
     airports_df = pd.json_normalize(airports_df['airports'])
     airports_df.drop(['airport_name','airport_city','airport_icao_unique_code','airport_altitude'],inplace=True,axis=1)
     routes_df = pd.json_normalize(routes_df['routes'])

     #merging the the routes and airports dataframe, then merge with airlines dataframe
     inner_merged = pd.merge(routes_df,airports_df,left_on='route_to_airport_id', right_on='airport_id',how='inner')
     another_merged = pd.merge(inner_merged,airlines_df,left_on='route_airline_id', right_on='airline_id',how='inner')
     filtered = another_merged[another_merged['airport_country'] == 'Canada'] #filter by the airport country Canada
     
     #grouping and sorting the final dataframe to obtain result
     answer:pd.DataFrame = filtered.groupby(['airline_name', 'airline_icao_unique_code'],as_index=False).size().sort_values(['size','airline_name'],ascending=[False,True]).head(20) #changed

     answer['subject'] = answer['airline_name'] + ' (' + answer['airline_icao_unique_code'] + ')' #formatting what is shown on pdf
     answer = answer.iloc[:,[3,2]]      #swapping the last two columns, subject column contains formatted contents for .csv file

     createCSVfile(df=answer,fileName='q1.csv',columnNames=['subject','size']) #creating the file 
     
     #determines what graph to output
     if 'bar' in graph:
          createBarPlot(fileName='q1.pdf',title='Bar Plot of q1',xlabels=answer['subject'],ylabels=answer['size'],rotate=10,width=55,height=20)
     elif 'pie' in graph:
          createPiePlot(df=answer,fileName='q1.pdf',title='Pie Plot of q1',names=answer['subject'],values=answer['size'])


def question2(airlines_df, airports_df, routes_df, graph)-> None:
     """ generates the asnwer to question 2.

          Parameters
            ----------
               airlines_df: dataframe, required
                    dataframe generated from the airlines.yaml file
               airports_df: dataframe, required
                    dataframe generated from the airports.yaml file
               routes_df: datafram, required
                    dataframe generated from the routes.yaml file
               graph: str, required
                    the type of graph that will be generated in the pdf
     """
     #separate the columns of each dataframe, and drop unneeded columns
     airlines_df = pd.json_normalize(airlines_df['airlines'])
     airlines_df.drop(['airline_name','airline_icao_unique_code','airline_country'],inplace=True,axis=1)
     airports_df = pd.json_normalize(airports_df['airports'])
     airports_df.drop(['airport_name','airport_city','airport_icao_unique_code','airport_altitude'],inplace=True,axis=1)
     routes_df = pd.json_normalize(routes_df['routes'])

     airports_df['airport_country'] = airports_df['airport_country'].str.lstrip() #remove leading whitespace from column

     #merging the the routes and airports dataframe, then merge with airlines dataframe
     inner_merged = pd.merge(routes_df,airports_df,left_on='route_to_airport_id', right_on='airport_id',how='inner')
     another_merged = pd.merge(inner_merged,airlines_df,left_on='route_airline_id', right_on='airline_id',how='inner')
     
     #obtain final answer by grouping and sorting the data
     answer = another_merged.groupby(['airport_country'],as_index=False).size().sort_values(['size','airport_country'],ascending=[True,True]).head(30)

     createCSVfile(df=answer,fileName='q2.csv', columnNames=['airport_country','size'])   #creates the .csv file

     #determines what graph to output
     if 'bar' in graph:
          createBarPlot(fileName='q2.pdf',title='Bar Plot of q2',xlabels=answer['airport_country'],ylabels=answer['size'],rotate=60,width=50,height=30)
     elif 'pie' in graph:
          createPiePlot(df=answer,fileName='q2.pdf',title='Pie Plot of q2',names=answer['airport_country'],values=answer['size'])

def question3(airlines_df, airports_df, routes_df, graph)-> None:
     """ generates the asnwer to question 3.

          Parameters
            ----------
              airlines_df: dataframe, required
                    dataframe generated from the airlines.yaml file
               airports_df: dataframe, required
                    dataframe generated from the airports.yaml file
               routes_df: datafram, required
                    dataframe generated from the routes.yaml file
               graph: str, required
                    the type of graph that will be generated in the pdf
     """
     #separate the columns of each dataframe, and drop unneeded columns
     airlines_df = pd.json_normalize(airlines_df['airlines'])
     airlines_df.drop(['airline_name','airline_icao_unique_code','airline_country'],inplace=True,axis=1)
     airports_df = pd.json_normalize(airports_df['airports'])
     airports_df.drop(['airport_altitude'],inplace=True,axis=1)
     routes_df = pd.json_normalize(routes_df['routes'])

     #merging the the routes and airports dataframe, then merge with airlines dataframe
     inner_merged = pd.merge(routes_df,airports_df,left_on='route_to_airport_id', right_on='airport_id',how='inner')
     another_merged = pd.merge(inner_merged,airlines_df,left_on='route_airline_id', right_on='airline_id',how='left')

     #obtain final answer by grouping and sortting data
     answer = another_merged.groupby(['airport_name', 'airport_icao_unique_code','airport_city','airport_country'],as_index=False).size().sort_values(['size','airport_name'],ascending=[False,True]).head(10)

     answer['subject'] = answer['airport_name'] + ' (' + answer['airport_icao_unique_code'] + '), ' + answer['airport_city'] + ', ' + answer['airport_country'] #formats what is put into .csv file
     
     createCSVfile(df=answer,fileName='q3.csv',columnNames=['subject','size']) #creates the .csv file
     
     #determines what graph to output
     if 'bar' in graph:
          createBarPlot(fileName='q3.pdf',title='Bar Plot of q3',xlabels=answer['airport_name'],ylabels=answer['size'],rotate=14,width=50,height=20)
     elif 'pie' in graph:
          createPiePlot(df=answer,fileName='q3.pdf',title='Pie Plot of q3',names=answer['airport_name'],values=answer['size'])

def question4(airlines_df, airports_df, routes_df, graph)-> None:
     """ generates the asnwer to question 4.

          Parameters
            ----------
               airlines_df: dataframe, required
                    dataframe generated from the airlines.yaml file
               airports_df: dataframe, required
                    dataframe generated from the airports.yaml file
               routes_df: datafram, required
                    dataframe generated from the routes.yaml file
               graph: str, required
                    the type of graph that will be generated in the pdf
     """
     #separate the columns of each dataframe, and drop unneeded columns
     airlines_df = pd.json_normalize(airlines_df['airlines'])
     airlines_df.drop(['airline_name','airline_icao_unique_code','airline_country'],inplace=True,axis=1)
     airports_df = pd.json_normalize(airports_df['airports'])
     airports_df.drop(['airport_name','airport_icao_unique_code', 'airport_altitude'],inplace=True,axis=1)
     routes_df = pd.json_normalize(routes_df['routes'])

     #merging the the routes and airports dataframe, then merge with airlines dataframe
     inner_merged = pd.merge(routes_df,airports_df,left_on='route_to_airport_id', right_on='airport_id',how='inner')
     another_merged = pd.merge(inner_merged,airlines_df,left_on='route_airline_id', right_on='airline_id',how='left')

     #determines the final answer by grouping and sortting data
     answer = another_merged.groupby(['airport_city','airport_country'],as_index=False).size().sort_values(['size','airport_city'],ascending=[False,True]).head(15) #changed
     answer['subject'] = answer['airport_city'] + ', ' + answer['airport_country']   #formats what is put into .csv file

     createCSVfile(df=answer,fileName='q4.csv', columnNames=['subject','size']) #creates the .csv file

     #determines what graph to output
     if 'bar' in graph:
          createBarPlot(fileName='q4.pdf',title='Bar Plot of q4',xlabels=answer['subject'],ylabels=answer['size'],rotate=20,width=40,height=20)
     elif 'pie' in graph:
          createPiePlot(df=answer,fileName='q4.pdf',title='Pie Plot of q4',names=answer['subject'],values=answer['size'])

def question5(airlines_df, airports_df, routes_df, graph)-> None:
     """ generates the asnwer to question 5.

          Parameters
            ----------
               airlines_df: dataframe, required
                    dataframe generated from the airlines.yaml file
               airports_df: dataframe, required
                    dataframe generated from the airports.yaml file
               routes_df: datafram, required
                    dataframe generated from the routes.yaml file
               graph: str, required
                    the type of graph that will be generated in the pdf
     """
     #separate the columns of each dataframe, and drop unneeded columns
     airlines_df = pd.json_normalize(airlines_df['airlines'])
     airlines_df.drop(['airline_name','airline_icao_unique_code','airline_country'],inplace=True,axis=1)
     airports_df = pd.json_normalize(airports_df['airports'])
     airports_df.drop(['airport_name','airport_city'],inplace=True,axis=1)
     routes_df = pd.json_normalize(routes_df['routes'])
   
     #merging the the routes and airlines dataframe, then merging again to create two dataframes contianing origin and destination airport IDs
     allMerged_df = pd.merge(routes_df,airlines_df, left_on='route_airline_id',right_on='airline_id', how='inner')
     fromAirport_merged = pd.merge(allMerged_df, airports_df, left_on='route_from_aiport_id', right_on='airport_id',how='inner')
     toAirport_merged = pd.merge(fromAirport_merged,airports_df,left_on='route_to_airport_id', right_on='airport_id', how='inner')

     #filtering by the airport countries to equal Canada
     filtered = toAirport_merged[(toAirport_merged['airport_country_x'] == 'Canada') & (toAirport_merged['airport_country_y'] == 'Canada')]
     
     temp =(filtered['airport_altitude_y'].astype(float) - filtered['airport_altitude_x'].astype(float)).abs()     #finds the difference between both altitudes
     merged_pd = pd.concat([filtered,temp],axis=1,join='inner')  #joins the difference with rest of dataframe values
     merged_pd.columns = [*merged_pd.columns[:-1],'diff']        #names the last column 
     answer = merged_pd.sort_values(by=['diff'],ascending=False) #sorts based on the last columns
     answer['subject'] = answer['airport_icao_unique_code_x'] + '-' + answer['airport_icao_unique_code_y']    #formats what is put into .csv file
     
     temp = answer.head(10)   #only want top 10 results
     createCSVfile(df=answer.head(10), fileName='q5.csv',columnNames=['subject','diff'])  #creating the file

     #determines what graph to output
     if 'bar' in graph:
          createBarPlot(fileName='q5.pdf',title='Bar Plot of q5',xlabels=temp['subject'],ylabels=temp['diff'],rotate=15 ,width=22,height=12)
     elif 'pie' in graph:
          createPiePlot(df=temp,fileName='q5.pdf',title='Pie Plot of q5',names=temp['subject'],values=temp['diff'])


def createCSVfile(df,fileName,columnNames) -> None:
     """ Creates a csv for each question.

          Parameters
            ----------
              df: dataframe, required
                    dataframe that contains content for the csv file
              fileName: str, required
                    name (number of question answered) of the .csv file 
              columnNames: list[str], required
                    column names in dataframe which data is pullled from to go in .csv file
     """
     headerNames = ['subject','statistic']
     df.to_csv(fileName,header = headerNames,columns=columnNames,index=False)

def createBarPlot(fileName,title,xlabels,ylabels,rotate,width,height)-> None:
     """ Creates a bar graph for each question.

          Parameters
            ----------
               fileName: str, required
                    name (number of question answered) of the pdf file
               title: str, required
                    name of the graph
               xlabels: series, required
                    column for the x-axis data 
               ylabels: series, required
                    column for the y-axis data
               rotate:
                    how much you want the x-axis labels to rotate
               width:
                    how wide the graph will be
               height:
                    how tall the graph will be
     """
     plt.rcParams.update({'font.size': 20})
     plt.rcParams['figure.figsize'] = (width,height)

     #formats the graph based on parameters passed to function
     plt.xticks(rotation = rotate) 
     plt.xlabel('Subjects')
     plt.ylabel('Statistic')
     plt.title(title)
     plt.tight_layout()
     plt.bar(xlabels,ylabels,align='center')
     plt.savefig(fileName)

def createPiePlot(df,fileName,title,names,values)-> None:
     """ Creates a pie graph for each question.

          Parameters
            ----------
               df: dataframe, required
               fileName: str, required
                    name (number of question answered) of the pdf file
               title: str, required
                    name of the graph
               names: series, required
                    column which labels the sections of the pie char
               values: series, required
                    column which the pie chart values are calculated with
     """

     plt.rcParams.update({'font.size': 5})

     #formats the graph based on parameters passed to function
     plt.title(title)
     plt.tight_layout()
     plt.axis('equal')
     #checks if the graph comes from number 5 since the displayed values in 5 need to be modified
     if '5' in fileName:
          plt.pie(data=df,x=values,labels=names,autopct=lambda x: '{:.0f} meters'.format(x*df['diff'].sum()/100),pctdistance=.8)  
     else:
          plt.pie(data=df,x=values,labels=names,autopct='%1.1f%%',pctdistance=.8)

     plt.savefig(fileName)

def openYAMLfile(file)-> None:
     """ Opens all of the yaml files

          Parameters
            ----------
               file: str, required
                    name of the file that will be opened
     """
     try:
          with open(file, 'r') as stream:
               return(safe_load(stream))
     except FileNotFoundError:          #throws an exception if the file is not found
          print("Error: file not found")


if __name__ == '__main__':
    main()