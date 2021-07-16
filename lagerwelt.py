# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 19:18:20 2021

@author: jadec
"""

import mysql.connector
from mysql.connector import Error
import streamlit as st
import pandas as pd

# streamlit run "C:/Users/jadec/OneDrive/Workspaces/pythonWorkspace/lagerwelt.py"




# =============================================================================
# Header
# =============================================================================
st.write("""
# Lagerwelt
""")

articles = pd.DataFrame()

def search(articleNr):
    result = articles[5].str.match(articleNr)
    table.write(articles[result])



articles = []

table = st.empty()

def connect():
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
            print( cursor.execute("SELECT * FROM artikel") )
            # print( cursor.fetchall()[0] )
            # a = cursor.fetchall()
            myresult = cursor.fetchall()

            for x in myresult:
                articles.append(x)
                # for i in x:
                    # articles.append(i)
                    
                    
            articles = pd.DataFrame(articles)
            # articles.columns = ["id", "username", "password", "level", "prefix", "firstname", "lastname"]
            table.write(articles)
            bosch = articles[7].str.match('Bosch')
            st.write('Bosch Aggregate: ' + str( bosch.count() ))
    except Error as e:
        print("Error while connecting to MySQL", e)


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
            articles.columns = ["id", "username", "password", "level", "prefix", "firstname", "lastname"]
            st.write(articles)
    except Error as e:
        print("Error while connecting to MySQL", e)
        
        
connect()


searchFor = st.sidebar.text_input("Suche")
search(searchFor)