import sys
import math
from datetime import datetime

CENSUS_FILE = 0
SAMPLE_FILE = 1
FILE_TYPE = SAMPLE_FILE
CENSUS_FILE_LID = 4
CENSUS_FILE_LAT = 62
CENSUS_FILE_LON = 61
SAMPLE_FILE_LID = 0
SAMPLE_FILE_LAT = 1
SAMPLE_FILE_LON = 2

OUTPUT_FILE_NAME = sys.argv[2]


# Extract data marked by the parse_key from the JSON
def json_parse(json_list, parse_key):
    data = str(json_list).split(",")
    for d in data:
        if d.find(parse_key) > -1:
            return str(d.split(":", 1)[-1])


# Remove unwanted characters from parsed JSON data
def clean(obj):
    obj = obj.replace(" ", "")
    obj = obj.replace("}", "")
    obj = obj.replace("\'", "")
    obj = obj.replace("%", "")
    obj = obj.replace("$", "")
    return obj


# Calculate the GPS coordinate that is a given distance away from another one
def get_end_coordinates(start_location, dist):
    earth_radius = 6378.1
    bearing = 1.57

    lat = math.radians(start_location[1])
    lon = math.radians(start_location[2])

    end_lat = math.asin(math.sin(lat) * math.cos(dist / earth_radius) +
                        math.cos(lat) * math.sin(dist / earth_radius) * math.cos(bearing))

    end_lon = lon + math.atan2(math.sin(bearing) * math.sin(dist / earth_radius) * math.cos(lat),
                               math.cos(dist / earth_radius) - math.sin(lat) * math.sin(end_lat))

    end_lat = math.degrees(end_lat)
    end_lon = math.degrees(end_lon)

    return [end_lat, end_lon]


# Read latitude, longitude and location from a CSV file
def get_location_data(filename):
    raw_location_data = []
    csv = open(filename, "r")
    for line in csv:
        raw_location_data.append(line.split(","))
    raw_location_data.pop(0)

    location_data = []
    for element in raw_location_data:
        location_id = element[SAMPLE_FILE_LID]
        longitude = element[SAMPLE_FILE_LON]
        latitude = element[SAMPLE_FILE_LAT]

        if FILE_TYPE == CENSUS_FILE:
            latitude = str(latitude).replace("\n", "")
        else:
            longitude = str(longitude).replace("\n", "")

        latitude = float(latitude)
        longitude = float(longitude)

        location = [location_id, latitude, longitude]
        location_data.append(location)

    return location_data


# Create output CSV to store results
def make_CSV():
    CSV = open(OUTPUT_FILE_NAME, "w")

    header = ("Date/Time,"
              "Location_Name,"
              "Y,"
              "X,"
              "sample_trip_dist,"
              "uberPOOL_ETA,"
              "uberX_ETA,"
              "uberSELECT_ETA,"
              "uberBLACK_ETA,"
              "uberXL_ETA,"
              "uberSUV_ETA,"
              "uberPOOL_price,"
              "uberX_price,"
              "uberSELECT_price,"
              "uberBLACK_price,"
              "uberXL_price,"
              "uberSUV_price,"
              "uberPOOL_surge,"
              "uberX_surge,"
              "uberSELECT_surge,"
              "uberBLACK_surge,"
              "uberXL_surge,"
              "uberSUV_surge,"
              "lyftREG_ETA,"
              "lyftLine_ETA,"
              "lyftPlus_ETA,"
              "lyftREG_price,"
              "lyftLine_price,"
              "lyftPlus_price,"
              "lyftREG_surge,"
              "lyftLine_surge,"
              "lyftPlus_surge,"
              "lyftREG_drivers,"
              "lyftLine_drivers,"
              "lyftPlus_drivers,"
              "temperature (F),"
              "rain-last3hr (mm) %,"
              "snow-last3hr (mm) %\n")

    CSV.write(header)
    CSV.close()


# Write data to CSV (one line only)
def CSV_write(data, EOR):
    CSV = open(OUTPUT_FILE_NAME, "a")

    section_header = str(datetime.now().strftime('%Y-%m-%d:%H:%M:%S.%f')) + ","
    section_header += str(data[0][0]) + "," + str(data[0][1]) + "," + str(data[0][2])
    CSV.write(section_header + "," + str(data[1]) + ",")

    uber_eta = ["", "", "", "", "", ""]

    for obj in data[2][0]:
        this_obj = obj
        this_obj.pop(0)
        for product in this_obj:
            if product[0] == 'UberPOOL':
                uber_eta[0] = product[1]
            elif product[0] == 'UberX':
                uber_eta[1] = product[1]
            elif product[0] == 'UberSELECT':
                uber_eta[2] = product[1]
            elif product[0] == 'UberBLACK':
                uber_eta[3] = product[1]
            elif product[0] == 'UberXL':
                uber_eta[4] = product[1]
            elif product[0] == 'UberSUV':
                uber_eta[5] = product[1]

    for eta in uber_eta:
        CSV.write(eta + ",")

    uber_price = ["", "", "", "", "", ""]
    uber_surge = ["", "", "", "", "", ""]

    for obj in data[2][1]:
        this_obj = obj
        this_obj.pop(0)
        for product in this_obj:
            if product[0] == 'UberPOOL':
                uber_price[0] = product[1]
                uber_surge[0] = product[2]
            elif product[0] == 'UberX':
                uber_price[1] = product[1]
                uber_surge[1] = product[2]
            elif product[0] == 'UberSELECT':
                uber_price[2] = product[1]
                uber_surge[2] = product[2]
            elif product[0] == 'UberBLACK':
                uber_price[3] = product[1]
                uber_surge[3] = product[2]
            elif product[0] == 'UberXL':
                uber_price[4] = product[1]
                uber_surge[4] = product[2]
            elif product[0] == 'UberSUV':
                uber_price[5] = product[1]
                uber_surge[5] = product[2]

    for price in uber_price:
        CSV.write(price + ",")

    for surge in uber_surge:
        CSV.write(surge + ",")

    lyft_eta = ["", "", ""]

    for obj in data[3][0]:
        this_obj = obj
        this_obj.pop(0)
        for product in this_obj:
            if product[0] == 'LyftReg':
                lyft_eta[0] = product[1]
            elif product[0] == 'LyftLine':
                lyft_eta[1] = product[1]
            elif product[0] == 'LyftPlus':
                lyft_eta[2] = product[1]

    for eta in lyft_eta:
        CSV.write(eta + ",")

    lyft_price = ["", "", ""]
    lyft_surge = ["", "", ""]

    for obj in data[3][1]:
        this_obj = obj
        this_obj.pop(0)
        for product in this_obj:
            if product[0] == 'LyftReg':
                lyft_price[0] = product[1]
                lyft_surge[0] = product[2]
            elif product[0] == 'LyftLine':
                lyft_price[1] = product[1]
                lyft_surge[1] = product[2]
            elif product[0] == 'LyftPlus':
                lyft_price[2] = product[1]
                lyft_surge[2] = product[2]

    for price in lyft_price:
        CSV.write(price + ",")

    for surge in lyft_surge:
        CSV.write(str(surge) + ",")

    lyft_drivers = ["", "", ""]

    for obj in data[3][2]:
        this_obj = obj
        this_obj.pop(0)
        for product in this_obj:
            if product[0] == 'LyftReg':
                lyft_drivers[0] = product[1]
            elif product[0] == 'LyftLine':
                lyft_drivers[1] = product[1]
            elif product[0] == 'LyftPlus':
                lyft_drivers[2] = product[1]

    for driver in lyft_drivers:
        CSV.write(str(driver) + ",")

    for obj in data[4]:
        CSV.write(obj + ",")

    CSV.write("\n")

    if EOR:
        CSV.write("\n")

    CSV.close()
