import subprocess
import shlex
import random
import shutil
import math
import sys
import datetime
import time
import os

#Set the path of 64 bit NetSim Binaries to be used for simulation. 
NETSIM_PATH="C:\\Users\\Navya\\Documents\\NetSim\\Workspaces\\Performance-Analysis-Wireless-Adhoc-Network\\bin_x64"
NUMBER_OF_NODES=7

#Set NETSIM_AUTO environment variable to avoid keyboard interrupt at the end of each simulation
os.environ['NETSIM_AUTO'] = '1'

#Create IOPath directory to store the input Configuration.netsim file and the simulation output files during each iteration
if not os.path.exists('IOPath'):
    os.makedirs('IOPath')

#Create Data directory to store the Configuration.netsim and the Metrics.xml files associated with each iteration
#if not os.path.exists('Data'):
   # os.makedirs('Data')

#Clear the IOPath folder if it has any files created during previous multi-parameter sweep runs
for root, dirs, files in os.walk('IOPath'):
    for file in files:
        os.remove(os.path.join(root, file))

IAT= [160000,80000,53333,40000,32000,26666,22857,20000,17777,16000,15686,15384,15094,14814,14545,14285,14035,13793,13559,13333,12307,11428,10666,10000,9411,8888,8421,8000]

#Delete result.csv file if it already exists
if(os.path.isfile("result.csv")):
    os.remove("result.csv")

#create a csv file to log the output metrics for analysis
csvfile = open("result.csv", 'w')

#Add headings to the CSV file
csvfile.write('INTER_ARRIVAL_TIME(micro sec),THROUGHPUT(Mbps),')
csvfile.close()

#create a folder with name as year-month-day-hour.minute.seconds inside the data folder
today=time.strftime('%d-%b-%Y-%H.%M.%S')
foldername= 'Wireless-Adhoc-Network-Cases'

#Iterate based on the number of time simulation needs to be run and the input parameter range
for i in IAT:
      Soure_rate=(1000*8)/i
      Soure_rate=(round(Soure_rate, 2))
    
      if(os.path.isfile("Configuration.netsim")):
       os.remove("Configuration.netsim")

      if(os.path.isfile("IOPath\Configuration.netsim")):
        os.remove("IOPath\Configuration.netsim")

      if(os.path.isfile("IOPath\Metrics.xml")):
        os.remove("IOPath\Metrics.xml")

      #Call ConfigWriter.exe with arguments as per the number of variable parameters in the input.xml file
      cmd='ConfigWriter.exe '+str(i)
      print(cmd)
      os.system(cmd)

      #Copy the Configuration.netsim file generated by ConfigWriter.exe to IOPath directory 
      if(os.path.isfile("Configuration.netsim")):
        shutil.copy("Configuration.netsim","IOPath\Configuration.netsim")
      for x in range(1,NUMBER_OF_NODES):
      	static_file='StaticIPConfigure'+str(x)+'.txt'
      	if(os.path.isfile(static_file)):
      		shutil.copy(str(static_file),"IOPath\\"+str(static_file))
      	strIOPATH=os.getcwd()+"\IOPath"
    
      #Run NetSim via CLI mode by passing the apppath iopath and license information to the NetSimCore.exe
      cmd="start \"NetSim_Multi_Parameter_Sweeper\" /wait /min /d "+ "\""+NETSIM_PATH+ "\" "\
      +"NetSimcore.exe -apppath \""+NETSIM_PATH+"\" -iopath \""+strIOPATH+\
      "\" -license 5053@192.168.0.9"

    
      #print(cmd)
      os.system(cmd)


      #Create a copy of the output Metrics.xml file for writing the result log
      if(os.path.isfile("IOPath\Metrics.xml")):
        shutil.copy("IOPath\Metrics.xml","Metrics.xml")

      cmd="MetricsCsv.exe IOPath"
      os.system(cmd)
    
      #Number of Script files i.e Number of Output parameters to be read from Metrics.xml
      #If only one output parameter is to be read only one Script text file with name Script.txt to be provided
      #If more than one output parameter is to be read, multiple Script text file with name Script1.txt, Script2.txt,...
      #...,Scriptn.txt to be provided
      OUTPUT_PARAM_COUNT=1;
    
      if(os.path.isfile("Metrics.xml")):
        #Write the value of the variable parameters in the current iteration to the result log
        csvfile = open("result.csv", 'a')
        csvfile.write('\n'+str(i)+',')    
        csvfile.close()
        
        if(OUTPUT_PARAM_COUNT==1):
            #Call the MetricsReader.exe passing the name of the output log file for updating the log based on script.txt
            os.system("MetricsReader.exe result.csv")                
        else:
            for n in range(1,OUTPUT_PARAM_COUNT+1,1):
                os.rename("Script"+str(n)+".txt","Script.txt");
                os.system("MetricsReader.exe result.csv")
                csvfile = open("result.csv", 'a')
                csvfile.write(',')
                csvfile.close()
                os.rename("Script.txt","Script"+str(n)+".txt");          

      else:
        #Update the output Metric as crash if Metrics.xml file is missing
        csvfile = open("result.csv", 'a')
        csvfile.write('\n'+str(i)+','+'crash'+',')
        csvfile.close()

      #Name of the Output folder to which the results will be saved
      OUTPUT_PATH='Performance-Analysis-Wireless-Adhoc-Network\\'+str(foldername)+'\\6-Hop-Network'+'-'+ str(today)+'\\6-Hop_'+'Source rate'+'-'+str(Soure_rate)+'Mbps';
    
      if not os.path.exists(OUTPUT_PATH):
       os.makedirs(OUTPUT_PATH)

       #create a copy of result.csv file present in sweep folder to date-time folder
       if(os.path.isfile('result.csv')):
         shutil.copy(os.path.join('result.csv'),'Performance-Analysis-Wireless-Adhoc-Network\\'+str(foldername)+'\\6-Hop-Network'+'-'+ str(today))

       #Create a copy of all files that is present in IOPATH to the desired output location
       files_names = os.listdir('IOPATH')
       for file_name in files_names:
          shutil.move(os.path.join('IOPATH', file_name),OUTPUT_PATH)

       #Delete Configuration.netsim file created during the last iteration
       if(os.path.isfile("Configuration.netsim")):
         os.remove("Configuration.netsim")

       #Delete Metrics.xml file created during the last iteration
       if(os.path.isfile("Metrics.xml")):
         os.remove("Metrics.xml")
