# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 00:35:58 2022

@author: anjal
"""
import numpy as np
import pickle
loaded_model=pickle.load(open('D:/pridicting Health Risk of pregent Patient/trained_modeln.sav','rb'))
print("---------------------------------") 
print("       DecisionTreeClassifier")
print("Level of Risk:1-3   low->1,high->3")
print("__________________________________")
inpFrame=['Enter Age of Patient:','Enter systolic Blood Pressure of Patient:','Enter Diastolic Blood Pressuree of Patient:','Enter Blood Glucose Level of Patient:','Enter Body Temperarature of  Patient:','Enter Heart Rateof Patient:',]
inpArray=list()
for i in  range(6):
  temp=input(inpFrame[i])
  inpArray.append(float(temp))
patientPredict=loaded_model.predict([inpArray])
print("________________________________________")
if patientPredict[0]==1.0:
  print("Risk Level of patient is Low:",patientPredict[0])
  print("You and your baby are safe")
elif patientPredict[0]==2.0:
  print("Risk Level of patient is Medium:",patientPredict[0])
  print("Need to take rest and take care of ypurself")
elif  patientPredict[0]==3.0:
  print("Risk Level of patient is High:",patientPredict[0])
  print("Need to consult to the doctor")
print('-----------------------------------------') 