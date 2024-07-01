import pandas as pd
import panel as pn

import hvplot.pandas
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statistics as st
from statistics import mean
from sklearn import linear_model
from scipy import stats
from js import console

from datetime import datetime as dt

from pyscript import document
from pyweb import pydom

patch_all()

gun_dataset_og = ("https://media.githubusercontent.com/media/Aryanwin/gun-violence-app/main/GunViolence3.csv")
gun_dataset = pd.read_csv(gun_dataset_og)
gun_data = gun_dataset.filter(["incident_id", "date", "state", "city_or_county", "n_killed", "n_injured"], axis = 1)

finalRisk = 0

def q(selector, root=document):
    return root.querySelector(selector)

returnimage = pydom["#image display"][0]
State1 = pydom["#Statebutton"][0]
city1 = pydom["#citybutton"][0]
date1 = pydom["#datebutton"][0]

#method that converts inputted date in format 
#yyyy/mm/dd into an integer that can be used
def dateconvert(string):
    dateint = 0
    monthlist = [31,28,31,30,31,30,31,31,30,31,30,31]
    
    year = int(string[0:4])
    month = int(string[5:7])
    day = int(string[8:10])
    dateint = dateint + 365*(year-2013) + int((year-2012)/4)
    for i in range(month-1):
        dateint = dateint + monthlist[i]
    dateint = dateint + day
    
    return dateint

gun_datalist = []
for i in range(len(gun_data)):
    gun_datalist.append((dateconvert(gun_data.loc[i,"date"])))

gun_data["intDate"] = gun_datalist

risklist = []
totalrisk = 0
ct = 0
for i in range(len(gun_data)):
    temp = 10*gun_data.loc[i,"n_killed"]+2*gun_data.loc[i,"n_injured"]
    risklist.append(temp)
    totalrisk = totalrisk + temp
    ct+=1
#print(risklist)
meanrisk = totalrisk/ct
#print(maxrisk)

gun_data["risk"] = risklist


def riskCalcAlg(event):
    State = State1.value
    city = city1.value
    date= date1.value
    gun_data_filtered = gun_data.loc[gun_data["state"]==State]
    #print(gun_data_filtered)
    gun_data_filtered2 = gun_data_filtered.loc[gun_data_filtered["city_or_county"]==city]
    #print(gun_data_filtered2)
    
    x = gun_data_filtered2[["intDate"]]
    y = gun_data_filtered2[["risk"]]
    #print(y)
    
    model = linear_model.LinearRegression()

    model.fit(x,y)

    y_pred = model.predict(x)
    
    ##prints out the graph using plt...if yall can figure out how to implement this then great, but for rn it'll stay commented
    plt.plot(gun_data_filtered2["intDate"], y_pred, color='red')
    #plt.scatter(x, y) 
    plt.savefig('gundata.png')
    ##plt.show()
    
    predrisk = model.intercept_ + model.coef_*(dateconvert(date))
    print(model.intercept_)
    print(model.coef_)
    finalRisk = round(predrisk[0][0]/meanrisk,3)*100
    return finalRisk

print(riskCalcAlg("New Hampshire", "Nashua", "2025/03/25"))
print("success!")