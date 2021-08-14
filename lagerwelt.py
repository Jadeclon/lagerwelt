# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 19:18:20 2021

@author: jadec
"""

import mysql.connector
from mysql.connector import Error
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# streamlit run "C:/Users/jadec/OneDrive/Workspaces/pythonWorkspace/lagerwelt.py"




# =============================================================================
# Header
# =============================================================================
st.write("""
# Lagerwelt
""")

result = 0
tableDf = pd.DataFrame()

# =============================================================================
# Search function
# =============================================================================
def search(articleNr):
    global tableDf
    result = articles['Artikelnummer'].str.match(articleNr)
    tableDf = articles[result]
    table.write(articles[result])
    
    
    
def filterTable(row, opperator, value):
    print("FILTERING")
    if row == 'Anzahl':
        if opperator == '<':
            boo = tableDf[row] < int(value)
        elif opperator == '>':
            boo = tableDf[row] > int(value)
        elif opperator == '=':
            boo = tableDf[row] == int(value)
    elif row == 'Marke' or row == 'Zustand' or row == 'Lagerplatz' or row == 'Hersteller':
        if opperator == '=':
            boo = tableDf[str(row)] == str(value)
        
    table.write(tableDf[boo == True])
    tableCaption.write('*' + str( tableDf[boo == True].count()[0] ) + ' Artikel gefunden*')



articles = []

table = st.empty()
tableCaption = st.empty()


# =============================================================================
# Brands Pie Chart
# =============================================================================
def getBrandsChart():
    result = articles['Marke'].str.contains('Mercedes')
    # global mercedeses
    mercedeses = articles[result]
    mercedeses['Marke'] = 'Mercedes-Benz'
    
    result = articles['Marke'].str.contains('Volkswagen|VW')
    vws = articles[result]
    vws['Marke'] = 'Volkswagen'
    
    result = articles['Marke'].str.contains('BMW')
    bmws = articles[result]
    bmws['Marke'] = 'BMW'
    
    result = articles['Marke'].str.contains('Opel')
    opel = articles[result]
    opel['Marke'] = 'Opel'
    
    result = articles['Marke'].str.contains('Volkswagen|VW|Mercedes|BMW|Opel')
    # global andere
    andere = articles[result == False]
    andere['Marke'] = 'Andere'
    
    # global marken
    marken = vws
    marken = marken.append(mercedeses)
    marken = marken.append(bmws)
    marken = marken.append(opel)
    marken = marken.append(andere)
    
    fig = px.pie(marken, values="Anzahl", names='Marke', title='Marke')
    st.write(fig)



def getManufacturerChart():
    manufacturerList = ['Bosch', 'Valeo', 'MD', 'Denso']
    result = articles['Hersteller'].str.contains(manufacturerList[0])
    bosch = articles[result]
    bosch['Hersteller'] = 'Bosch' # Alle einheitlich benennen
    
    result = articles['Hersteller'].str.contains(manufacturerList[1])
    valeo = articles[result]
    valeo['Hersteller'] = 'Valeo' # Alle einheitlich benennen
    
    result = articles['Hersteller'].str.contains(manufacturerList[2])
    md = articles[result]
    md['Hersteller'] = 'MD-Teile' # Alle einheitlich benennen
    
    result = articles['Hersteller'].str.contains(manufacturerList[3])
    denso = articles[result]
    denso['Hersteller'] = 'Denso' # Alle einheitlich benennen
    
    result = articles['Hersteller'].str.contains('Bosch|Valeo|MD|Denso')
    andere = articles[result == False]
    andere['Hersteller'] = 'Andere' # Alle einheitlich benennen
    
    manufacturer = pd.DataFrame()
    manufacturer = manufacturer.append(bosch)
    manufacturer = manufacturer.append(valeo)
    manufacturer = manufacturer.append(md)
    manufacturer = manufacturer.append(denso)
    manufacturer = manufacturer.append(andere)
    
    fig = px.pie(manufacturer, values='Anzahl', names='Hersteller', title='Hersteller')
    st.write(fig)
    


def getOnEbayChart():
    global result
    result = articles['onEbay'] > 0
    isLima = articles['ArtikelArt'] == 'Lichtmaschine'
    isStarter = articles['ArtikelArt'] == 'Starter'
    st.write("Verschiedene Artikel auf Ebay: " + str( articles[result == True].count()[0] ))
    st.write("")
    st.write("Nicht eingestellte Artikel auf Ebay: " + str( articles[result == False].count()[0] ))
    st.write("> davon Lichtmaschinen: " + str( articles[(result == False) & (isLima == True)].count()[0] ))
    st.write("> davon Starter: " + str( articles[(result == False) & (isStarter == True)].count()[0] ))






# =============================================================================
# Get articles table
# =============================================================================
def connect():
    global articles
    global result
    try:
        connection = mysql.connector.connect(host='sql150.main-hosting.eu',
                                             database='u794832960_lagerwelt',
                                             user='u794832960_jadeclon',
                                             password='Hammsene5')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            print( cursor.execute("SELECT * FROM artikel") )
            # print( cursor.fetchall()[0] )
            # a = cursor.fetchall()
            myresult = cursor.fetchall()

            for x in myresult:
                articles.append(x)
                # for i in x:
                    # articles.append(i)
                    
                    
            articles = pd.DataFrame(articles)
            articles.columns = ["artikel_Id", "Marke", "Ampere", "ArtikelArt", "Lagerplatz", "Artikelnummer", "Anzahl", "Hersteller", "Zustand", "OE", "EbayPlus", "webshop", "URL", "proofed", "vehicleId", "oeId", "pawn", "onEbay"]
            articles = articles.drop(columns=['artikel_Id', 'proofed', 'vehicleId', 'oeId', 'webshop', 'URL'])
            table.write(articles)
            
            # df = go.Figure(data=[go.Table(
            #     header=dict(values=list(articles.columns),
            #                 fill_color='blue',
            #                 align='left'),
            #     cells=dict(values=articles.transpose().values.tolist(),
            #                fill_color='red',
            #                align='left'))
            # ])
            # st.write(df)
            
            totalArticles = articles['Anzahl'].sum();
            totalArticleEntries = articles.count()[0]
            
            fig = px.pie(articles, values="Anzahl", names='ArtikelArt', title = str(totalArticleEntries) + ' verschiedene Artikel, insgesamt ' + str(totalArticles))
            st.write(fig)
            st.write("")
            

            
            getBrandsChart()
            getManufacturerChart()
            getOnEbayChart()

            # bosch = articles[7].str.match('Bosch')
            # st.write('Bosch Aggregate: ' + str( bosch.count() ))
    except Error as e:
        print("Error while connecting to MySQL", e)



# =============================================================================
# Get benutzer table
# =============================================================================
def getUsersTable():
    global articles
    try:
        connection = mysql.connector.connect(host='sql150.main-hosting.eu',
                                             database='u794832960_lagerwelt',
                                             user='u794832960_jadeclon',
                                             password='Hammsene5')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            print( cursor.execute("SELECT * FROM benutzer") )
            # print( cursor.fetchall()[0] )
            # a = cursor.fetchall()
            myresult = cursor.fetchall()

            for x in myresult:
                articles.append(x)
                # for i in x:
                    # articles.append(i)
                    
                    
            articles = pd.DataFrame(articles)
            # benutzer.columns = ["id", "username", "password", "level", "prefix", "firstname", "lastname"]
            st.write(articles)
    except Error as e:
        print("Error while connecting to MySQL", e)
        
        
        
        
connect()


searchFor = st.sidebar.text_input("Suche")
search(searchFor)





# filterFor = st.sidebar.text_input("Filter for row")
# filterOpperator = st.sidebar.text_input("Opperator")
# filterValue = st.sidebar.text_input("Value")
# if len(filterFor) > 0:
#     filterTable(filterFor, filterOpperator, filterValue)
























