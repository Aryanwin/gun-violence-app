import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statistics as st
from statistics import mean
from sklearn import linear_model
from scipy import stats

gun_dataset = pd.read_csv("GunViolence.csv")
gun_data = gun_dataset.filter(["incident_id", "date", "state", "city_or_county", "n_killed", "n_injured"], axis = 1)

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