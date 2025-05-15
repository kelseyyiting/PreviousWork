"""
Assignment 2
Full Name: Prathyush Bhamidipati
Net ID: pb37
I have completed the Core Goals set for the assignment and attempted the Stretch Goal 1 - Writing Functions Properly
"""
from datetime import datetime

categories = {1: (64, 82),2: (83, 95),3: (96, 112),4: (113, 136),5: (137, 1000)}
def parse_storm_data(filename):
    storm_stats = {}
    annual_counts = {}
    with open(filename, 'r') as file:
        storm_id=None
        storm_name=None
        start_time=None
        end_time=None
        max_wind_speed=0
        min_pressure = 100000
        landfall = 0
        category = 0
        for line in file:
            row = line.strip().split(',')
            if len(row) == 4:
                if storm_id:
                    duration=end_time-start_time
                    storm_stats[storm_id]={
                        "name": storm_name,
                        "duration": f"{duration.days} days {duration.seconds // 3600} hours",
                        "max_wind": max_wind_speed,
                        "min_pressure": min_pressure,
                        "landfalls": landfall,
                        "peak_category": category}
                    update_annual_counts(annual_counts, storm_id, category)
                storm_id = row[0]
                storm_name = row[1].strip() if row[1].strip() != "UNNAMED" else None
                max_wind_speed=0
                min_pressure=100000
                landfall=0
                category=0
                start_time=None
                end_time=None
            elif len(row) > 4:
                date = row[0].strip()
                time = row[1].strip()
                record = row[2].strip()
                wind_speed = int(row[6].strip())
                pressure = int(row[7].strip()) if row[7].strip() else 100000

                timestamp = datetime.strptime(date + time,"%Y%m%d%H%M")
                if start_time is None:
                    start_time = timestamp
                end_time = timestamp
                max_wind_speed = max(max_wind_speed, wind_speed)
                min_pressure = min(min_pressure, pressure)
                for cat, (low, high) in categories.items():
                    if low <= wind_speed <= high:
                        category = max(category, cat)
                if record == "L" and category >= 1:
                    landfall += 1
        if storm_id:
            duration = end_time - start_time
            storm_stats[storm_id] = {
                "name": storm_name,
                "duration": f"{duration.days} days {duration.seconds // 3600} hours",
                "max_wind": max_wind_speed,
                "min_pressure": min_pressure,
                "landfalls": landfall,
                "peak_category": category}
            update_annual_counts(annual_counts, storm_id, category)
    return storm_stats, annual_counts

def update_annual_counts(annual_counts, storm_id, peak_category):
    year = int(storm_id[4:])
    if year not in annual_counts:
        annual_counts[year]={"Storms": 0, "Cat1": 0, "Cat2": 0, "Cat3": 0, "Cat4": 0, "Cat5": 0}

    annual_counts[year]["Storms"] += 1
    if peak_category > 0:
        annual_counts[year][f"Cat{peak_category}"] += 1

def print_results(storm_stats, annual_counts):
    output_file = "hurdat_results.txt"
    with open(output_file, "w") as f:
        for storm_id, details in storm_stats.items():
            f.write(f"Storm: {storm_id} ({details['name'] if details['name'] else 'UNNAMED'})\n")
            f.write(f"  Duration: {details['duration']}\n")
            f.write(f"  Max Wind Speed: {details['max_wind']} knots\n")
            f.write(f"  Min Pressure: {details['min_pressure']} millibars\n")
            f.write(f"  Landfalls at Cat 1+: {details['landfalls']}\n")

        f.write(f"{'Year':<6}{'Storms':>8}{'Cat1':>6}{'Cat2':>6}{'Cat3':>6}{'Cat4':>6}{'Cat5':>6}\n")
        for year,details in sorted(annual_counts.items()):
            f.write(f"{year:<6}{details['Storms']:>8}{details['Cat1']:>6}{details['Cat2']:>6}{details['Cat3']:>6}{details['Cat4']:>6}{details['Cat5']:>6}\n")

def main():
    files = ["hurdat2-1851-2023-051124.txt", "hurdat2-nepac-1949-2023-042624.txt"]
    all_storms = {}
    all_yearly_counts = {}

    for filename in files:
        storm_stats, annual_counts=parse_storm_data(filename)
        all_storms.update(storm_stats)
        for year, counts in annual_counts.items():
            if year not in all_yearly_counts:
                all_yearly_counts[year] = counts
            else:
                for key in counts:
                    all_yearly_counts[year][key] += counts[key]

    print_results(all_storms, all_yearly_counts)

if __name__ == "__main__":
    main()