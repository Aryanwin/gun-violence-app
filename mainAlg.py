from js import console
console.log("console working")

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

from datetime import datetime as dt

from pyscript import document
from pyweb import pydom
from pyodide_http import patch_all


patch_all()
pn.extension(design="material")
allStates = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

variable_widget = pn.widgets.Select(
    name = "Choose State", value="Illinois", options = list(allStates)
)

gun_dataset_og = ("https://media.githubusercontent.com/media/Aryanwin/gun-violence-app/main/GunViolence3.csv")
console.log("works till here")
gun_dataset = pd.read_csv(gun_dataset_og)
gun_data = gun_dataset.filter(["incident_id", "date", "state", "city_or_county", "n_killed", "n_injured"], axis = 1)
console.log("Downloaded data")

finalRisk = 0
## I know this is lazy but there's no point parsing through 250k lines just for this one-time copy-paste

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


def riskCalcAlg(State, date):
    gun_data_filtered = gun_data.loc[gun_data["state"]==State]
    #print(gun_data_filtered2)
    
    x = gun_data_filtered[["intDate"]]
    y = gun_data_filtered[["risk"]]
    #print(y)
    
    model = linear_model.LinearRegression()

    model.fit(x,y)

    y_pred = model.predict(x)
    
    ##prints out the graph using plt...if yall can figure out how to implement this then great, but for rn it'll stay commented
    plt.plot(gun_data_filtered["intDate"], y_pred, color='red')
    plt.scatter(x, y) 
    plt.savefig('gundata.png')
    plt.show()
    
    predrisk = model.intercept_ + model.coef_*(dateconvert(date))
    #print(model.intercept_)
    #print(model.coef_)
    finalRisk = round(predrisk[0][0]/meanrisk,3)*100
    return finalRisk


avg = variable_widget.value
console.log(variable_widget.value)
#pipeline = avg.hvplot(height=300, width=400, color="blue", legend=False)
pn.Column(variable_widget).servable(
    target="panel"
)
riskCalcAlg(avg,"2024/07/02")
variable_widget.param.watch(console.log(variable_widget.value), "value")
variable_widget.param.watch(riskCalcAlg(avg, "2024/07/02"), "value")
variable_widget.param.watch(console.log(avg), "value")