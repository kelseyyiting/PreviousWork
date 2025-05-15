'''
I completed Core goals 1,2,3
'''
from copy import deepcopy

from sympy import false

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def _top_20(info):
    import heapq
    top20=heapq.nlargest(20,info.items(),key=lambda x:x[1][6])
    # top20 = sorted(info.items(), key=lambda x: x[1][-1], reverse=True)[:20]
    print(top20)
    return top20

def output_for_top_20(info) :
    top20=_top_20(info)
    new_dic_top20=[]

    for storm in top20:
        '''
        top20 is a list: [('ID',[name,year,time,maxwind,minpressure,landfall,distance]),...]
        storm is a tuple: ('ID',[name,year,time,maxwind,minpressure,landfall,distance])
        '''
        storm_info = []  # this is a new list [name,distance]
        name=storm[1][0]
        id=storm[0]
        distance=storm[1][6]

        storm_info.append(name)
        storm_info.append(id)
        storm_info.append(distance)

        new_dic_top20.append(storm_info)
    return new_dic_top20

def select_cities(file_path, mode='r', encoding='utf-8',verbose=False):
    selected_cities= {}     # "city","lat","lng", "country","iso2""admin_name",  "population", & “id”
    with open(file_path, mode, encoding=encoding) as file:
        for line in file:   #"city","city_ascii","lat","lng","country","iso2","iso3","admin_name","capital","population","id"
            line=line.split(',')
            line = [item.strip('"') for item in line]
            lat=line[2]
            lng=line[3]
            population=line[-2]

            if is_number(lat):
                lat=float(lat)
                lng=float(lng)
                try:
                    population=int(population)
                except ValueError:
                    break
                if population>=500000 and lat>=0 and lat<=90 and lng<=0 and lng>=-180 :
                    new_city_value={}
                    new_city_key=(line[0],line[-1].strip('\"\n'))   #city and id

                    new_city_value['lat']=lat   #lat
                    new_city_value['lng']=lng  #lng
                    new_city_value['country']=line[4]    #country
                    new_city_value['iso2']=line[5]    #iso2
                    new_city_value['admin_name']=line[7]   #adminname
                    new_city_value['pop']=population   #population

                    selected_cities[new_city_key]=new_city_value
                else: continue
            else:
                continue
    return selected_cities
def print_cities(selected_cities):
    for city in selected_cities:
        print(" ".join("{:<30}".format(item) for item in city))
    return 0

# def _hit_city(citypath,storm_location,storm_name,verbose=False) :
#     '''
#     :param cities: cities: the list of cities which might hit by storms
#           e.g  "Tokyo","Tokyo","35.6897","139.6922","Japan","JP","JPN","Tōkyō","primary","37732000","1392685764"
#     :param storm_location: the location of the storm, a dictionary: {lat:123,long:123}
#
#     :return: return a list or dict contains id(which is unique as a key),name, country, capital
#     '''
#     city_hit=None
#     storm_range=_nm_near(20,storm_location,verbose)
#     with open(citypath, mode='r', encoding='utf-8') as file:
#         for line in file:
#             line=line.split(',')
#             if is_number(line[-1]):
#                 city_name=line[0]
#                 city_id=line[-1]
#                 city_country=line[4]
#                 city_capital=line[-3]
#
#                 city_lat=line[2]
#                 city_lng=line[3]
#                 city_loc={'lat':city_lat,'lng':city_lng}
#                 if verbose:
#                     if city_name=='Hamilton' and storm_name=='EMILY':
#                         print(city_name,storm_name)
#                 if _if_near(city_loc,storm_range) :
#                     distance_storm_city = calculate_distance(city_loc['lat'], city_loc['lng'], storm_location['lat'],
#                                                              storm_location['lng'])
#                     if distance_storm_city>20:
#                         city_hit=[city_id,city_name,city_country,city_capital]
#
#             else:continue
#     # for city,city_info in cities.items():
#     #     city_name=city[0]
#     #     city_loc={'lat':city_info['lat'],'lng':city_info['lng']}
#     #     if verbose:
#     #         if city_name=='Hamilton' and storm_name=='EMILY':
#     #             print(city_name,storm_name)
#     #     if _if_near(city_loc,storm_range) :
#     #         distance_storm_city=calculate_distance(city_loc['lat'],city_loc['lng'],storm_location['lat'],storm_location['lng'])
#     #         if verbose:print(city_name)
#     #         if distance_storm_city>20 :
#     #             city_hit=city_name
#     #             break
#     #     else:continue
#     return city_hit
def _if_near(city_spot,storm_location) :
    # this function is designed to roughly calculate if the storm near the city
    if abs(city_spot['lat']-storm_location['lat']) < 2 and abs(city_spot['lng']-storm_location['lng']) < 2:return True
    return False
def _if_near_precise(city_spot,location_range):
    '''
    this function is designed to check if a spot's location is within a certain range
    :param city_spot: location is a dic: {lat:123,long:123}, means a spot
    :param location_range: location range is a dictionary: {'lat':[N,S],"lng":[E,W]}, means a spot
    :return: return a boolean
    '''
    city_spot['lat']=float(city_spot['lat'])
    city_spot['lng']=float(city_spot['lng'])
    if location_range['lat'][1] <= city_spot['lat'] <= location_range['lat'][0] and location_range['lng'][1] <= city_spot['lng'] <= location_range['lng'][0]:
        return True
    return False
def _calculative_loc(spot):
    if not is_number(spot['lat'][-1]):
        if spot['lat'][-1] == 'S':
            spot['lat']=-float(spot['lat'][:-1])
        else:
            spot['lat']=float(spot['lat'][:-1])

        if spot['lng'][-1] == 'W':
            spot['lng'] = -float(spot['lng'][:-1])
        else:
            spot['lng']=float(spot['lng'][:-1])

    else:
        spot['lat'] = float(spot['lat'])
        spot['lng'] = float(spot['lng'])
    return spot
def _nm_near (nm:float,storm_location,verbose=False):#tested
    storm_location_range={}
    '''
    :param nm: nm is a float or an integer, it means how many nautical meters away from the location
    :param location: location is a dictionary: {lat:123,long:123}
    :return: return a dictionary:{'lat':[North,south],'lng':[East,West]}
    '''
    from geographiclib.geodesic import Geodesic
    geod = Geodesic.WGS84
    lat=storm_location['lat']
    lng=storm_location['lng']
    distance_m=nm*1852

    North=geod.Direct(lat,lng,0,distance_m)
    South=geod.Direct(lat,lng,180,distance_m)
    East=geod.Direct(lat,lng,90,distance_m)
    West=geod.Direct(lat,lng,270,distance_m)

    storm_location_range['lat']=[North['lat2'], South['lat2']]
    storm_location_range['lng']= [East['lon2'], West['lon2']]
    if verbose:print(storm_location_range)
    return storm_location_range

def cities_hit(storm_path:list,citypath:str,mode='r', encoding='utf-8',verbose=False)->dict:
    '''
    :param storm_path: the list contains two file path of storms
    :param cities: city path is a file path recording information for cities
    :return: return a dictionary of cities and the count they get hit in a descending way
    '''
    cities_with_storms={}
    last_storm=''
    last_hit_location=None
    is_landfall=False
    storm_date=None
    line_now=0
    for file_path in storm_path:
        with open(file_path, mode='r', encoding='utf-8') as file:
            for line in file:
                line = line.split(',')#18521009, 2100, L, HU, 29.9N,  84.4W,  90, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999
                if 0<line_now<=line_count:  #could be optimize by count the number of title line[-1]
                    line_now+=1
                    if line[2] == ' L':
                        is_landfall=True
                    if is_landfall == False: continue
                    speed=float(line[6])
                    if speed>=63 :
                        storm_location = {'lat': line[4], 'lng': line[5]}
                        storm_location = _calculative_loc(storm_location)
                        if verbose:
                            storm_date=line[0]
                            if storm_date=='19870923':print()
                        with open(citypath, mode, encoding=encoding) as cities:
                            for city in cities:     #"Tokyo","Tokyo","35.6897","139.6922","Japan","JP","JPN","Tōkyō","primary","37732000","1392685764"
                                city = city.split(',')
                                city = [item.strip('"') for item in city]
                                city[-1] = city[-1].replace('\"\n', '')
                                if is_number(city[-1]):
                                    city_id = city[-1]
                                    city_name = city[0]
                                    if verbose and storm_ID == 'AL121987' and city_id == '1060000000':
                                        print(storm_name,city_name)
                                    if verbose and storm_ID == 'AL082014' and city_id == '1060000000':
                                        print()
                                    if last_storm == storm_ID and last_city == city_id:  # means this city is already hit by this storm
                                        continue

                                    city_loc = {'lat': city[2], 'lng': city[3]}
                                    city_loc=_calculative_loc(city_loc)

                                    if not _if_near(city_loc,storm_location):
                                        is_landfall=False
                                        continue
                                    else: is_landfall=True
                                    storm_range = _nm_near(20, storm_location, verbose=False)
                                    if _if_near_precise(city_loc,storm_range):
                                        last_storm = storm_ID
                                        last_city = city_id
                                        city_country = city[4]
                                        city_capital = city[-3]

                                        last_hit_location=deepcopy(storm_location)
                                        if cities_with_storms.get(city_id) is None:
                                            newlist = [city_name, city_country, city_capital, 1]
                                            cities_with_storms[city_id] = newlist
                                        else:
                                            cities_with_storms[city_id][-1] += 1
                                            if verbose: print(cities_with_storms[city_id])
                                        break
                                else:continue   #process this line:"city","city_ascii","lat","lng","country","iso2","iso3","admin_name","capital","population","id"
                    else:continue
                else:       #AL121987,              EMILY,     30,

                    storm_name=line[1].replace(' ','')
                    storm_ID=line[0]
                    is_landfall=False
                    line_count=int(line[2])
                    line_now=1
                    continue
    return cities_with_storms
# def cities_hit_2 (citypath,landfall_storms,verbose=False):
#     '''
#     :param citypath:city path is a file path recording information for cities
#     :param landfall_storms: landfall storms is a list, [name,loc_range] which location is a dictionary{lat:123,lng:123}
#     :return:
#     '''
#     cities_with_storms={}
#     with open(citypath, 'r', encoding='utf-8') as file:
#         for line in file:
#             line = line.split(',')
#             line = [item.strip('"') for item in line]
#             line[-1]=line[-1].replace('\"\n','')
#             if is_number(line[-1]):
#                 city_name = line[0]
#                 city_lat = line[2]
#                 city_lng = line[3]
#                 city_loc = {'lat': city_lat, 'lng': city_lng}
#                 i=0
#                 while i < len(landfall_storms):
#                     #[name,location] which location is a dictionary{lat:123,lng:123}
#                     storm=landfall_storms[i]
#                     storm_name = storm[0]
#                     storm_id = storm[1]
#                     if verbose:
#                         if storm_id == 'AL121987' and city_name=='Hamilton':
#                             print(storm_name,city_name)
#                     # storm_location = storm[1]
#                     storm_range=landfall_storms[i][-1]
#                     if _if_near(city_loc, storm_range):
#                         # distance_storm_city = calculate_distance(city_loc['lat'], city_loc['lng'], storm_location['lat'],storm_location['lng'])
#                         city_id = line[-1]
#                         city_country = line[4]
#                         city_capital = line[-3]
#                         # if distance_storm_city > 20:
#                         if cities_with_storms.get(city_id) is None:
#                             newlist=[city_name, city_country, city_capital,1]
#                             cities_with_storms[city_id] = newlist
#                         else:
#                             cities_with_storms[city_id][-1]+=1
#                             if verbose: print(cities_with_storms[city_id])
#                         del landfall_storms[i]
#                     else:
#                         i+=1
#     return cities_with_storms
def sorted_city (cities):
    sorted_cities = dict(sorted(cities.items(), key=lambda item: item[1][3], reverse=True))
    return sorted_cities
def print_with_format(cities,key_width,value_width,file=None):
    format={'City_ID':['City_Name','Country','Capital']}
    print("{:<{}}{}".format('City_ID',key_width," ".join("{:<{}}".format(v,value_width) for v in format['City_ID'])),file=file)
    for city_ID in cities:
        print("{:<{}}{}".format(city_ID,key_width," ".join("{:<{}}".format(v,value_width) for v in cities[city_ID])),file=file)
    return 0

def landfall_filter(file_path,verbose=False):
    '''

    :param file_path: the path of the storms file
    :param verbose:
    :return: filtered_storms is a list including, [[name,ID,location_range],[name,ID,location_range],...]
    '''
    filtered_storms=[]
    i=0
    for file in file_path:
        with open(file, mode='r', encoding='utf-8') as file:
            for line in file:
                line = line.split(',')
                if is_number(line[0]):  # 18521009, 2100, L, HU, 29.9N,  84.4W,  90, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999
                    speed = float(line[6])
                    if line[2] == ' L' and speed > 63:
                        location = {'lat': line[4], 'lng': line[5]}
                        loc_range=_nm_near(20,location,)
                        new_storm=[storm_name,storm_ID,loc_range]
                        if verbose and storm_name == 'EMILY':
                            print(new_storm)
                        i+=1
                        filtered_storms.append(new_storm)
                else:
                    storm_name=line[1].replace(' ','')
                    storm_ID=line[0]
                    continue
    if verbose:print(i)
    return filtered_storms


if __name__ == '__main__':
    # hurdat_path = ['hurdat2-1851-2023-051124.txt', 'hurdat2-nepac-1949-2023-042624.txt']
    # # hurdat_path=['Hurdat-testing.txt']
    # # citypath = 'wordcities-testing.csv'
    # citypath='worldcities.csv'
    # # print(cities_hit(hurdat_path,citypath))
    # print_with_format(cities_hit(hurdat_path,citypath), 13, 30)

    with open('A3Result.txt', 'w', encoding='utf-8') as f:
        #Core Goal 1
        print('----------------------------------------------------', file=f)
        print('Core Goal 1',file=f)
        import A2
        general_output_atlantic=A2.output_general_infos('hurdat2-1851-2023-051124.txt')
        general_output_nepac=A2.output_general_infos('hurdat2-nepac-1949-2023-042624.txt')
        merge_storms = {**general_output_atlantic, **general_output_nepac} # system ID : [name,year,time,max_wind,min_pressure,landfall,distance]
        for storm in output_for_top_20(merge_storms):
            print("{:<12} {:<12} {}".format(storm[0], storm[1], storm[2]),file=f)

        #Core Goal 2
        print('----------------------------------------------------', file=f)
        print('Core Goal 2', file=f)
        selected_cities= select_cities('worldcities.csv')
        for city_id in selected_cities:
            print(f"{city_id} {selected_cities[city_id]}", file=f)

        #Core Goal 3
        print('----------------------------------------------------', file=f)
        print('Core Goal 3', file=f)
        hurdat_path=['hurdat2-1851-2023-051124.txt','hurdat2-nepac-1949-2023-042624.txt']
        citypath='worldcities.csv'
        sorted_cities = sorted_city(cities_hit(hurdat_path, citypath))
        print_with_format(sorted_cities, 13, 30,file=f)


