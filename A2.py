'''
I have attempted the stretch goals 1 & 2.
'''
import sys

from sympy import false
from sympy.abc import lamda

from review1 import update_annual_counts


'''
This dataset (known as NE/NC Pacific HURDAT2) has a comma-delimited,
text format with six-hourly information on the location,
maximum winds, central pressure, and (beginning in 2004) size of
all known tropical cyclones and subtropical cyclones.
'''
from copy import deepcopy
'''
system ID              Name        
AL011851,            UNNAMED,     14,

Date y/m/d,Time  , L                ,Max w,P   ,  
18510625, 0000,  , HU, 28.0N,  94.8W,  80, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999
'''

'''
goals: print out the following data for EACH STORM
a.	Storm system ID (e.g. ‘AL011851’). Also show its name if not ‘UNNAMED’
b.	The duration of time the storm was tracked, as days + hours. (datetime library is helpful).
c.	The highest Maximum sustained wind (in knots).
d.	The lowest Minimum in central pressure (in millibars).
e.	How many landfalls, if any, did it have while at Category 1 or higher? (see below for Categories)
'''
from datetime import datetime

def calculate_time(time_start, time_end):
    time_format = "%Y%m%d %H%M"  # calculate the time
    dt_start = datetime.strptime(time_start, time_format)
    dt_end = datetime.strptime(time_end, time_format)
    time_diff = dt_end - dt_start
    days = time_diff.days
    hours = time_diff.seconds // 3600
    time = str(days) + 'd' + str(hours) + 'h'
    return time

def insert_infos(system_ID,output,info_line,time,max_wind,min_pressure,landfall,distance=0):
    output[system_ID].append(info_line[0][0:4])  # insert the year of the storm
    output[system_ID].append(time)  # insert the time of the storm

    output[system_ID].append(max_wind)  # insert the min pressure of the storm
    output[system_ID].append(min_pressure)  # insert the max wind of the storm
    output[system_ID].append(landfall)      #insert the number of landfall
    output[system_ID].append(distance)      #insert the distance of storm
    return


def output_general_infos(file_path, mode='r', encoding='utf-8',verbose=False):
    output={}   #using dictionaries to record system id and other infos
    number_of_lines = 0
    with open(file_path, mode, encoding=encoding) as file:  #open the file
        for line in file:
            if line[0].isdigit(): #processing the information lines

                now_line += 1
                info_line=line.split(',')    #18510625, 0000,  , HU, 28.0N,  94.8W,  80, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999
                if info_line[2] ==' L':     #calculating landfall
                    if float(info_line[6])>=64 : landfall+=1

                if number_of_lines == 1:    #if there is only one line record for a storm
                    insert_infos(system_ID,output,info_line,'NA',info_line[6],info_line[7],landfall)
                    continue

                wind.append(float(info_line[6]))    #using a list to record the wind in a storm
                pressure.append(float(info_line[7]))

                if now_line == 1:
                    time_start = info_line[0]+info_line[1]
                    lon_start = info_line[5]
                    lat_start = info_line[4]
                    distance=0
                elif now_line == number_of_lines:
                    time_end = info_line[0]+info_line[1]

                    time=calculate_time(time_start, time_end) #calculate the time
                    max_wind = max(wind)        #calculate the max wind
                    min_pressure = min(pressure)        #calculate the min pressure


                    insert_infos(system_ID,output, info_line, time, max_wind, min_pressure ,landfall,distance)   #insert infos
                    #system ID : [name,year,time,max_wind,min_pressure,landfall,distance]
                else:
                    lon_end = info_line[5]
                    lat_end = info_line[4]
                    distance +=calculate_distance(lat_start, lon_start, lat_end, lon_end)

                    lon_start = lon_end
                    lat_start = lat_end

            else: #processing the title lines
                line=line.replace(' ','')   #eliminate all the blank space
                title_line=line.split(',')    #AL011851,            UNNAMED,     14,
                system_ID=title_line[0]      #record the key as system id
                output[system_ID]=[]     #key = title_line[0]
                output[system_ID].append(title_line[1])
                number_of_lines=int(title_line[2])
                now_line=0
                # output={system ID :[name]}
                if verbose:
                    print('the ID{} line has created'.format(system_ID))

                wind=[]     #create a list to record wind
                pressure=[]     #create a list to record pressure
                landfall=0      #initialize the number of landfall occurs

    return output
def calculate_distance(lat1,lon1,lat2,lon2) :
    from geographiclib.geodesic import Geodesic
    f1 = lambda geo_info: float(geo_info[:-1])

    lat1=f1(lat1)
    lon1=f1(lon1)
    lat2=f1(lat2)
    lon2=f1(lon2)

    geod = Geodesic.WGS84
    result=geod.Inverse(lat1,lon1,lat2,lon2)

    distance_meters=result['s12']
    distance_nm=distance_meters/1852
    return distance_nm

def output_for_each_id(general) :
    info=deepcopy(general)
    for system_ID in info:
        del info[system_ID][1]
    return info

def output_for_each_year(info) :
    '''
    :param general: general is a dictionary{system_ID:[name,year,time,max_wind,min_pressure,landfall],...}
    '''
    output_year={}
    for system_ID in info:
        year=info[system_ID][1]
        if year not in output_year: #create a new key-value if there's no record for this year
            output_year[year]=[0,0,0,0,0,0]     #initialize a new dictionary for goal 5

        output_year[year][0]+=1     #calculate how many storms appear in one year
        max_wind=float(info[system_ID][3])

        if max_wind>=137:       #calculate cat appears how many times
            output_year[year][5]+=1
        elif max_wind >= 113:
            output_year[year][4] += 1
        elif max_wind>=96:
            output_year[year][3]+=1
        elif max_wind >= 83:
            output_year[year][2] += 1
        elif max_wind>=64:
            output_year[year][1]+=1
    return output_year

def print_each_ID (general_output,district,file=None) :
    output_id = output_for_each_id(general_output)  # print infos for goal4
    id_format={'ID':['Name','Time','Max_wind','Min_pressure','Landfall','distance']}
    sorted_print(output_id, 12, 12,id_format,district,file)
    return output_id

def print_each_year(general_output,district,file=None) :   # print infos for goal5
    output_year = output_for_each_year(general_output)
    year_format={'Year':['Storm','Cat1','Cat2','Cat3','Cat4','Cat5']}
    sorted_print(output_year,6,5,year_format,district,file)
    return output_year

def sorted_print(info,key_width,value_width,which_format,district,file=None):
    print(district)
    for key in which_format:
        print("{:<{}}{}".format(key, key_width, " ".join("{:<{}}".format(v, value_width) for v in which_format[key])))
    for system_ID in info:
        print("{:<{}}{}".format(system_ID,key_width," ".join("{:<{}}".format(v,value_width) for v in info[system_ID])))
    print('--------------------------------------------------')
    print('')
    if file:
        print(district,file=file)
        for key in which_format:
            print("{:<{}}{}".format(key, key_width, " ".join("{:<{}}".format(v, value_width) for v in which_format[key])),file=file)
        for system_ID in info:
            print("{:<{}}{}".format(system_ID, key_width,
                                    " ".join("{:<{}}".format(v, value_width) for v in info[system_ID])),file=file)
        print('--------------------------------------------------',file=file)
        print('',file=file)
    return



def cities_hit(selected_cities,):
    for city in selected_cities:
        return 0

# def filter_landfall(storms): #storms: {system ID : [name,year,time,max_wind,min_pressure,landfall,distance]}
#     landed_storms={}
#     for system_ID in storms:
#         if storms[system_ID][5]<=0 or storms[system_ID][3]<=63:
#             continue

    return 0
import A3
if True:
    general_output_atlantic=output_general_infos('hurdat2-1851-2023-051124.txt')
    general_output_nepac=output_general_infos('hurdat2-nepac-1949-2023-042624.txt')

    output_id_atlantic = output_for_each_id(general_output_atlantic)
    output_id_nepac = output_for_each_id(general_output_nepac)

    merge_storms = {**general_output_atlantic, **general_output_nepac} # system ID : [name,year,time,max_wind,min_pressure,landfall,distance]
    A3.output_for_top_20(merge_storms)       #top 20 storms distance in two district - core goal 1

    selected_cities= A3.select_cities('worldcities.csv')     #core goal 2

'''
20250209: core goal 1 &2 completed
incompleted part : core goal 3

draft: 
#1 process the hurdat file again, recording each line which have a 'L' symbol and max wind >63, 
including location infos and wind speed.
#2then use a loop to compare each city's location.
'''