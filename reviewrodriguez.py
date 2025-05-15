import os
from datetime import datetime
from collections import defaultdict

outfile = open('cyclones.txt', 'w')

def read_write_hurdat(file_path, storm_by_year, tropic_storms):
    """
        Parses a HURDAT2 dataset file and extracts storm information, writing summaries to an output file.

        Each storm's data is aggregated, including:
        - Storm ID
        - Name (if available)
        - Duration (in days and hours)
        - Maximum sustained wind (in knots)
        - Minimum central pressure (in millibars)
        - Number of landfalls while at category 1

        The function writes the extracted storm summaries to 'cyclones2.txt' and updates storm_by_year and tropic_storms.

        :param: file_path (str): Path to the HURDAT2 dataset.
        :param: storm_by_year(dict):A defaultdict(list) mapping years to a list of maximum wind speeds for storms
        in that year.This dictionary is updated in-place.
        :param: tropic_storms (list): A list tracking storm statistics in the format:
        [total storms, storms originating in tropics, storms staying in tropics].
        This list is updated in-place.
        :return: None
    """
    if os.path.splitext(file_path)[1].lower() != ".txt":
        raise ValueError(f"Error: The file '{file_path}' is not a .txt file.")

    storm = [None] * 7 # [ stormid, name, start, max_wind, min_pressure, landfall, remain_tropic ]
    row_count = None

    with open(file_path, 'r') as f:
        for line in f:
            line = line.replace('\n', '')
            line = line.split(',')

        # check line is not empty and first 2 characters of first column are alphanumeric
            if line != "" and line[0][:1].isalpha():
                storm[0] = line[0]
                storm[1] = line[1].strip()
                row_count = int(line[2])
                tropic_storms[0] += 1
                continue

            timestamp = datetime.strptime(line[0].strip()+line[1].strip(), '%Y%m%d%H%M')
            if storm[2] is None:
                storm[2] = timestamp   # record date and time of first row

            max_wind = int(line[6])
            if storm[3] is None or max_wind > storm[3]:
                storm[3] = max_wind

            min_pressure = int(line[7])
            # missing central pressure values are denoted as pp
            if min_pressure != -999 and (storm[4] is None or min_pressure < storm[4]):
                    storm[4] = min_pressure

            # keep count of landfall events for storm while cat 1 or higher (max sustained winds > 64 kt)
            if line[2].strip() == 'L' and max_wind > 64:
                    storm[5] = (storm[5] or 0) + 1

            latitude = float(line[4].strip()[:-1])
            if storm[6] is None and latitude <= 23.436:
                tropic_storms[1] += 1
                storm[6] = True

            if latitude > 23.436:
                storm[6] = False

            if row_count == 1: # during the last row of data for the storm
                duration = timestamp - storm[2]
                days = duration.days
                hours = duration.seconds / 3600

                row = str(f'Storm ID: {storm[0]} {"Name: " + storm[1] if storm[1] != 'UNNAMED' else '' } '
                          f'Duration: {days} day(s) {hours} hour(s) Max Wind Speed: {storm[3]} '
                          f'Minimum Central Pressure: {storm[4]} Landfall Count: {storm[5]}')
                print(row, file = outfile)

                storm_by_year[storm[2].year].append(storm[3])

                if storm[6]:
                    tropic_storms[2] += 1

                storm = [None] * 7

            row_count -= 1

storm_by_year = defaultdict(list)
tropic_storms = [0,0,0]  # [ # storms, # origin @ tropic, # remain in tropic ]

read_write_hurdat('hurdat2-nepac-1949-2023-042624.txt',storm_by_year,tropic_storms)
read_write_hurdat('hurdat2-1851-2023-051124.txt',storm_by_year,tropic_storms)


print(f'{'Year':>5}{'Storms':>7}{'Cat1':>5}{'Cat2':>5}{'Cat3':>5}{'Cat4':>5}{'Cat5':>5}', file = outfile)
first_year = min(storm_by_year.keys())
last_year = max(storm_by_year.keys())
all_years = range(first_year, last_year + 1) # complete list of years spanned by the data

for year in all_years:
    storm_max_ws = storm_by_year.get(year, []) # if year is not in the files it will be empty list
    cat_1 = len([x for x in storm_max_ws if 63 < x < 83])
    cat_2 = len([x for x in storm_max_ws if 82 < x < 96])
    cat_3 = len([x for x in storm_max_ws if 95 < x < 113])
    cat_4 = len([x for x in storm_max_ws if 112 < x < 137])
    cat_5 = len([x for x in storm_max_ws if x > 136])
    print(f'{year:5}{len(storm_max_ws):>7}{cat_1:>5}{cat_2:>5}{cat_3:>5}{cat_4:>5}{cat_5:>5}', file = outfile)

origin_percent = round((tropic_storms[1]/tropic_storms[0])*100,2) if tropic_storms[0] > 0 else 0
stay_percent = round((tropic_storms[2]/tropic_storms[0])*100,2) if tropic_storms[0] > 0 else 0
print(f'{origin_percent}% of all storms originated within the tropics', file = outfile)
print(f'{stay_percent}% of all storms stayed within the tropics', file = outfile)
