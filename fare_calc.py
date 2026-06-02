import os

def load_fares(filepath="fare.txt"):
    """
    Reads the text file and returns a dictionary of stations and their values.
    Format expected in txt: 0=25, 1=40, 2=55, etc.
    """
    fares_dict = {}
    
    # Failsafe: Prevent crash if the file is accidentally deleted
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return fares_dict
        
    with open(filepath, 'r') as file:
        for line in file:
            # Clean up any accidental spaces or blank lines
            line = line.strip()
            if '=' in line:
                station_id, station_value = line.split('=')
                # Convert strings to integers so we can do math with them
                fares_dict[int(station_id)] = int(station_value)
                
    return fares_dict

def calculate_fare(start_station, end_station, base_fare=10):
 
    fares = load_fares()
    if start_station not in fares or end_station not in fares:
        return None    
    total_distance_cost = 0 
    first_stop = min(start_station, end_station)
    last_stop = max(start_station, end_station)
    for station in range(first_stop, last_stop):
        total_distance_cost += fares[station]
    total_fare = total_distance_cost + base_fare
    return total_fare


