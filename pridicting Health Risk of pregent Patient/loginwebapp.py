# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 09:23:45 2022

@author: anjal
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
# DB Management

st.header("Hii!welcome to PreFree WebApp!")

st.image("https://th.bing.com/th/id/OIP.SRhgcQZRJkST6QvCoSFFIgHaGE?w=218&h=180&c=7&r=0&o=5&dpr=1.7&pid=1.7")
st.write("**Welcome to the Health Risk Prediction Platform**")
st.markdown("A cutting-edge system designed to analyze and predict health risks in diverse patient populations. Our secure login page ensures that only authorized users can access sensitive health data and utilize advanced predictive tools.")
import base64


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('background.png')


import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():
	"""Simple Login App"""
    
	st.title("Patient Login page")
    
    
    
    
    
    
	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")
		st.write("**Welcome to the Health Cure Centre**")
		st.markdown("""Predicting health risks in pregnant patients involves assessing various factors to identify potential complications and take preventive measures. It's crucial to note that predicting health risks in pregnancy is a complex task, and healthcare professionals use a combination of medical history, physical examinations, and diagnostic tests to make informed predictions. Here are some key aspects related to predicting health risks and ensuring the health and well-being of pregnant patients:""")


	elif choice == "Login":
		st.subheader("Login Section")
        

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))

				task = st.selectbox("Task",["Admin Login","Patient Login","Database"])
				
				if task == "Admin Login":
					st.subheader("Login as Admin") 
                    
                   

				elif task == "Patient Login":
					st.subheader("Patient Login")
					loaded_model=pickle.load(open('D:/pridicting Health Risk of pregent Patient/trained_model.sav','rb'))
					#creating the fuction 
					def health_risks_prediction(inpArray):
						inpFrame=['Enter Age of Patient:','Enter systolic Blood Pressure of Patient:','Enter Diastolic Blood Pressuree of Patient:','Enter Blood Glucose Level of Patient:','Enter Body Temperarature of  Patient:','Enter Heart Rateof Patient:',]
						inpArray=list()
						for i in  range(6):
							temp=input(inpFrame[i])
							inpArray.append(float(temp))
							
						patientPredict=loaded_model.predict([inpArray])
						#print("________________________________________")
						if patientPredict[0]==1.0:
							return ["Risk Level of patient is Low-PATIENT IS HEALTHY :)",patientPredict[0]]
						elif patientPredict[0]==2.0:
							return ("Risk Level of patient is Medium- Need to take rest and take care of yourself ^-^", patientPredict[0])
						elif  patientPredict[0]==3.0:
							return ("Risk Level of patient is High- CONSULT THE DOCTOR", patientPredict[0])
						#print('-----------------------------------------')
					def main():
						#giving a title
						st.title('Predicting Health Risks for Pregnant Patients Web App')
						# getting the input data from the user
						Age=st.text_input('Age of the Patient')
						SystolicBP=st.text_input('Systolic BP of Patient')
						DiastolicBP=st.text_input('Diastolic BP of the Patient')
						BS=st.text_input('Blood glucose Levels of the Patient')
						BodyTemp=st.text_input('Body Temp of the Patient')
						HeartRate=st.text_input('Heart Rate of the Patient')
						# code for Prediction
						diagnosis=''
						# creating a button for Prediction
						if st.button('Health Risks test Result'):
							diagnosis=health_risks_prediction([Age,SystolicBP,DiastolicBP,BS,BodyTemp,HeartRate])
						st.success(diagnosis)
						
					if __name__=='__main__':
						main()
						
						
    
        

				elif task == "Database":
					st.subheader("Database")
					user_result = view_all_users()
					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
					st.dataframe(clean_db)
			else:
				st.warning("Incorrect Username/Password")





	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")



if __name__ == '__main__':
	main()