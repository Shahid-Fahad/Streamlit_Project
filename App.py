import mysql.connector as mysql
import pandas as pd
import time
from datetime import datetime
from PIL import Image
import json
import base64
import yagmail
import re
from re import search
# import smtplib
import random
import string
import secrets # import package
import streamlit as st

from database import get_database_connection
import uuid
import streamlit.components.v1 as components
from streamlit import caching

import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from sqlalchemy import create_engine
from mysql.connector.constants import ClientFlag

st.set_page_config(
    page_title="Diploma in Data Science Admission Portal",
    page_icon=":dolphin:",
    layout="wide",
    initial_sidebar_state="expanded",
)
cursor, db = get_database_connection()

# cursor.execute('''CREATE TABLE user (
#     id varchar(255) PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     institution VARCHAR(30) NOT NULL,
#     ssc_gpa float,
#     hsc_gpa float,
#     email varchar(255),
#     address varchar(255),
#     contact_number varchar(255),
#     status varchar(255),
#     dos varchar(255)
#     )''')

cols1, cols2, cols3 = st.columns((1, 7, 1))
cols2.title("Diploma in Data Science Admission Portal")


ch = st.sidebar.selectbox('Choose Anyone', ['Apply', 'Admin', 'User'])
if ch=="Apply":
    st.write(" ")
    with st.form(key="myform", clear_on_submit=True):
        name = st.text_input('Full Name')
        ins = st.text_input('Institution')
        dep = st.text_input('Department')
        cg = st.text_input('Cgpa')
        ssc = st.text_input('SSC GPA')
        hsc = st.text_input('HSC GPA')
        email = st.text_input('Email')
        dt = st.date_input("Apply Date")
        but1 = st.form_submit_button("Apply")


    if but1 and (name=="" or ins=="" or ssc=="" or hsc=="" or email=="" or cg=="" or dep==""):
        st.warning("Fill Out Every Box Correctly")
    elif but1:
        num = 5
        unid = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(num))
        status =0
        query = '''INSERT into user(id,name,institution,contact_number,address,ssc_gpa,hsc_gpa,email,status,dos)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        values = (unid, name, ins, dep, cg, ssc, hsc, email, status, dt)
        cursor.execute(query, values)
        db.commit()
        st.balloons()
        st.success('You Have Successfully Applied For Diploma in Data Science Admission')
        st.info(f'Your Unique ID : {unid}')


adm=1
if ch=="Admin":
    username = st.sidebar.text_input('Username', key='user')
    password = st.sidebar.text_input('Password', type='password', key='pass')
    st.session_state.login = st.sidebar.checkbox('Login')

    if st.session_state.login == True:
        if username == "Shzfahad" and password == 'shz123':
            st.sidebar.info('Admin Mode')

            date1 = st.date_input('Starting Date')
            date2 = st.date_input('Ending Date')
            cursor.execute(f"select id,name,institution,contact_number,address,ssc_gpa,hsc_gpa,status from user where dos between '{date1}' and '{date2}'")

            tables = cursor.fetchall()
            st.subheader(f"Pending Appliactions Between {date1} to {date2}")
            for i in tables:
                if i[7]=="0":
                    with st.form(key=i[0]):
                        st.write(f'Name:  {i[1]}')
                        st.write(f'Insitution:  {i[2]}')
                        st.write(f'Department:  {i[3]}')
                        st.write(f'CGPA:  {i[4]}')
                        st.write(f'SSC:  {i[5]}')
                        st.write(f'HSC:  {i[6]}')
                        Accept = st.form_submit_button('Accept')
                        Reject = st.form_submit_button('Reject')
                        if Accept:
                            st.write('Accepted')
                            cursor.execute(f"Update user set status='1' where id='{i[0]}'")
                            db.commit()
                            st.experimental_rerun()

                        if Reject:
                            st.write('Rejected')
                            cursor.execute(f"Update user set status='2' where id='{i[0]}'")
                            db.commit()
                            st.experimental_rerun()
        else:
            st.sidebar.error('Wrong Credintials')

if ch=="User":
    username = st.sidebar.text_input('Name', key='user')
    password = st.sidebar.text_input('Unique ID', type='password', key='pass')
    st.session_state.login = st.sidebar.button('Login')

    cursor.execute("Select id , name,institution,status from user")
    tables = cursor.fetchall()
    flg=0
    if st.session_state.login==True:

        for i in tables:
            if username==i[1] and password == i[0]:
                flg=1
                st.write(f'Name : {i[1]}')
                st.write(f'Institution : {i[2]}')
                st.write(f'ID : {i[0]}')
                if i[3]=="0":
                    st.info("Your Application is Pending")
                elif i[3]=="1":
                    st.balloons()
                    st.success("Your Application is Accepted")
                else:
                    st.error("Your Appliaction is Rejected. Better Luck Next Time")
                break
        if flg==0:
            st.sidebar.error("Wrong Credentials")





