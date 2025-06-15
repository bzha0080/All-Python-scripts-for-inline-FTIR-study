import csv
from time import sleep
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy as scipy
import matplotlib.ticker
from matplotlib import rcParams
import matplotlib
matplotlib.use('Agg')
import os
import datetime
import pandas as pd
from numpy import sqrt
import matplotlib.ticker
from syringepump import *
from SF10 import *
from datetime import datetime

# Open the reaction parameter file and load the data to data frame
parameterFile_path = r'\\ad.monash.edu\home\User001\bzha0080\Desktop\Monash\02. ongoing project\16. Self-initiation\timesweep code\CSExperimentParameter_MA.xlsx'

parameter_df =  pd.read_excel(parameterFile_path, index_col=0)
PumpName = parameter_df.iloc[:,0]; PumpPort = parameter_df.iloc[:,1]
V_reactor = parameter_df.iloc[:,2][1]; V_dead = parameter_df.iloc[:,3][1]
residence_time = parameter_df.iloc[:,4]

# Pumpreactionsolution = SF10(port=f'{PumpPort[1]}',name=f'{PumpName[1]}')

# Concentration sweep flow rate calculation
flow_rate_reaction_solution = [] 

for i in range(1,len(residence_time)+1):
   tres = residence_time[i]
   flow_reactionsolution = V_reactor*60/tres
   flow_rate_reaction_solution.append(flow_reactionsolution)

sleep_time_list = []
stablize_time = residence_time[1] *1.3 + (V_dead+V_reactor)*60/flow_rate_reaction_solution[0]
sleep_time_list.append(stablize_time)

for i in range(2,len(residence_time)+1):
   sleep_time_one = (V_reactor+V_dead)/(V_reactor*60/residence_time[i])*60 + 240  #extra 60 seconds to collect data at that residence time
   sleep_time_list.append(sleep_time_one)

print(sleep_time_list)

print(f'the flowrate of monomer involved is {flow_rate_reaction_solution}\n')

def volumecalculation():
   total_volume_reaction_solution = 0

   for i in range(len(sleep_time_list)):
      total_volume_reaction_solution += flow_rate_reaction_solution[i]*sleep_time_list[i]/60

   return total_volume_reaction_solution


def pumpstart():
   data_amount_before_timesweep = round((sleep_time_list[0] + V_dead/(V_reactor*60/residence_time[2])*60)/18)
   print(f'the amount of data points before time sweep are {data_amount_before_timesweep}')

   Pumpreactionsolution.start()
   sleep(0.5)
   Pumpreactionsolution.changeFlowrate(0)
   sleep(0.5)

   for i in range(len(flow_rate_reaction_solution)):

      today = datetime.now()
      CurrentTime = today.strftime("%H:%M:%S")
      Pumpreactionsolution.changeFlowrate(flow_rate_reaction_solution[i])
      sleep(sleep_time_list[i])
   
   Pumpreactionsolution.stop()


# total_volume_reaction_solution = volumecalculation()

# print(f'the total volume of reaction solution needed is {total_volume_reaction_solution} \n'
#       )

# pumpstart()