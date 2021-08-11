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

# streamlit run "C:/Users/jadec/OneDrive/Workspaces/pythonWorkspace/lagerwelt.py"




# =============================================================================
# Header
# =============================================================================
st.write("""
# Lagerwelt
""")

articles = pd.DataFrame()

def search(articleNr):
    result = articles['Artikelnummer'].str.match(articleNr)
    table.write(articles[result])



articles = []

table = st.empty()


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
            articles.columns = ["artikel_Id", "Marke", "Ampere", "ArtikelArt", "Lagerplatz", "Artikelnummer", "Anzahl", "Hersteller", "Zustand", "OE", "EbayPlus", "webshop", "URL", "proofed", "vehicleId", "oeId"]
            articles = articles.drop(columns=['artikel_Id', 'proofed', 'vehicleId', 'oeId', 'webshop', 'URL'])
            table.write(articles)
            
            fig = px.pie(articles, values="Anzahl", names='ArtikelArt', title='Artikel Typen')
            st.write(fig)
            

            
            getBrandsChart()
            getManufacturerChart()
            
            

            
            
            # result = articles['Marke'].str.contains('VW')
            # result = result.append( articles['Marke'].str.contains('Mercedes') )
            # global vws
            # vws = articles[result]
            # mercedeses['Marke'] = 'Mercedes-Benz'
            # fig = px.pie(articles['Marke'], values="Anzahl", names='Marke', title='Marke')
            # st.write(fig)
            
            
            # bosch = articles[7].str.match('Bosch')
            # st.write('Bosch Aggregate: ' + str( bosch.count() ))
    except Error as e:
        print("Error while connecting to MySQL", e)



# =============================================================================
# Get benutzer table
# =============================================================================
def connect3():
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