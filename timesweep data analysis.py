from CreateDataFolder import *
import csv
from time import sleep
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy as scipy
import matplotlib.ticker
import matplotlib
matplotlib.use('Agg')
import os
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import matplotlib.ticker
from Functions import *


# Create a experiment file folder to save all the data  
print("Please input the name of you Experiment :>>")
ExperimentName = input(':>>')
print("Please input the name of you FTIR Experiment :>>")
FTIRExperimentName = input(':>>')

# the path where we save the data
ParentFolder = r"S:\Sci-Chem\PRD\IR 112\Bo" 
Experimentfolder_path = CreateDataFolder(ExperimentName,ParentFolder)

# the path of IR rawdata, which will be monitored by watchdog 
IRrawdata_path = r"C:\Users\IR112\Documents\iC IR Experiments\Export folder\{}".format(FTIRExperimentName) 
# the path in the shared drive where the IR raw data will be saved
SavedIRrawdata_path = r'{}\IR_RawData'.format(Experimentfolder_path) 

# create a empty csv file to save all the calsulated data 
with open(r'{}\{}-Data.csv'.format(Experimentfolder_path, ExperimentName), 'a') as f:
    pass 

# Open the reaction parameter file and load the data to data frame
ParameterFile_Path = r'S:\Sci-Chem\PRD\IR 112\Bo\Python_code_Kp\CRSweepExperimentParameter_MA.xlsx'
# copy the experiment parameters file to the experiment folder
shutil.copy(ParameterFile_Path, Experimentfolder_path)
Parameter_df =  pd.read_excel(ParameterFile_Path, index_col=0)
PumpName = Parameter_df.iloc[:,0]; PumpPort = Parameter_df.iloc[:,1]
V_reactor = Parameter_df.iloc[:,2][1]; V_input = Parameter_df.iloc[:,3][1]; V_dead = Parameter_df.iloc[:,4][1]
residence_time = Parameter_df.iloc[:,5]

# Concentration sweep flow rate calculation
flowrate_reactionsolution = []; sleeptime_list = []

# start point flow rate calculation

for i in range (1,len(residence_time)+1):
    flowrate = V_reactor*60/residence_time[i]
    flowrate_reactionsolution.append(flowrate)

sleeptime_zero = residence_time[1]*1.3
sleeptime_list.append(sleeptime_zero)

for i in range (1, len(residence_time)):
    sleeptime = (V_reactor+V_dead)/flowrate_reactionsolution[i]*60
    sleeptime_list.append(sleeptime)



# watchdog class for the data analysis
peak_area_list = []; scan_time_list = []; conversion_list = []; tres_list = []; concentration_list = []

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        file_created = event.src_path
        print(file_created)
        listfile_created = os.listdir(IRrawdata_path)
        
        if len(listfile_created)*5 >= (V_reactor+V_dead)*60/flowrate_reactionsolution[0]:
            try:
                shutil.copy(file_created, SavedIRrawdata_path )
                sleep(1)

                with open(file_created) as csvfile:
                    rawdata = list(csv.reader(csvfile, delimiter = ","))
                
                # set scan time 
                listfile = os.listdir(SavedIRrawdata_path)
                j = len(listfile)
                scantime = j*5/60 
                scan_time_list.append(scantime)
                print(f"{j} scan data collected ")

                IR_rawdata_list = np.array(rawdata[1:],dtype = np.float64) # rawdata[1:], first line is the head, so we start from the second line
                results = background_calculation(IR_rawdata_list,1672,1280,1313)
                peakarea = results[0]
                print(f'peakarea is {peakarea}')
                peak_area_list.append(peakarea)

                # Calculate concentration and conversion
                # value_c = -0.58606 - peakarea
                # con_polynomial = np.poly1d([-0.2104,2.3565, value_c])
                # root_results = con_polynomial.roots
                # concentration = root_results[1]
                
                concentration = (peakarea - 5.9442)/2.5271
                concentration_list.append(concentration)

                conversion = (1- concentration/2.34)*100
                conversion_list.append(conversion)
                print(concentration,conversion)
                        

                # save the calculated data to a new CSV file under ExperimentName folder 
                data_output = {
                    'scantime/minute':scan_time_list,
                    'Peakarea':peak_area_list,
                    'Conversion/%':conversion_list,
                    'concentration/M':concentration_list,
                }
                # print(data_output)
                column_names = ['scantime/minute','Peakarea', 'Conversion/%','concentration/M']
                df = pd.DataFrame(data_output, columns = column_names) #columns = column_names
                df.to_csv(r'{}\{}-Data.csv'.format(Experimentfolder_path,ExperimentName), columns = column_names)

                fig = plt.figure()
                ax = fig.add_subplot(111)
                for axis in ['top', 'bottom', 'left', 'right']:
                    ax.spines[axis].set_linewidth(2) 
                ax.tick_params(axis = 'both', which = 'major', labelsize = 12)
                ax.tick_params(axis = 'both', which = 'minor', labelsize = 12)
                plt.plot(scan_time_list, peak_area_list, color = 'red', linewidth = 4, linestyle = ':')
                plt.xlabel('Scantime/minute',fontsize = 14)
                plt.ylabel('Peakarea',fontsize = 14)
                plt
                plt.savefig(f'{Experimentfolder_path}/RealtimePicture/Scantime_Peakarea')
                plt.clf()
                plt.close()
                
                
                fig = plt.figure()
                ax = fig.add_subplot(111)
                for axis in ['top', 'bottom', 'left', 'right']:
                    ax.spines[axis].set_linewidth(2) 
                ax.tick_params(axis = 'both', which = 'major', labelsize = 12)
                ax.tick_params(axis = 'both', which = 'minor', labelsize = 12)
                plt.plot(scan_time_list, conversion_list, color = 'black', linewidth = 3, linestyle = '-')
                plt.xlabel('Scantime/minute', fontsize = 14)
                plt.ylabel('Conversion', fontsize = 14)
                plt.savefig(f'{Experimentfolder_path}/RealtimePicture/Scantime_Conversion')
                plt.clf()
                plt.close()

            except Exception:
                pass

        else:
            pass

def data_analysis():
    observer = Observer(); event_handler = Handler()
    observer.schedule(event_handler, IRrawdata_path, recursive = True)
    print('Observer start')
    observer.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

data_analysis()


