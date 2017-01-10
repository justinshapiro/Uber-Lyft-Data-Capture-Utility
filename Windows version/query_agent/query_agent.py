# import querying framework
from AgentQueryFramework import *

# import helper libraries
import time
import sys
import os.path
import queue

# import querying routines that use the APIs
from UberQuery import uber_query
from LyftQuery import lyft_query
from WeatherQuery import weather_query

SOURCE_FILE = sys.argv[1]
UBER_REQUEST_LIMIT = 2000
STATS_FILE_LOCATION = "resources\\status.txt"


# Main routine
def main():
    # Set distance of Uber trip for the run
    trip_distance = 5

    # Get latitude, longitude, and location identifier from CSV
    location_data = get_location_data(SOURCE_FILE)

    # Create output CSV to store results
    if not os.path.isfile(sys.argv[2]):
        make_CSV()
    else:
        CSV = open(OUTPUT_FILE_NAME, "a")
        CSV.write("\n\n")
        CSV.close()

    count = 0
    run = 0
    total_locations = 0
    total_hr_requests = 0
    num_locations = len(location_data)
    num_uber_requests = 2
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        STATUS_OUT = open(STATS_FILE_LOCATION, "w")
        STATUS_OUT.write("\n------Round #" + str(run + 1) + "------\n")
        print("\n------Round #" + str(run + 1) + "------\n", end="")
        STATUS_OUT.close()
        time.sleep(3)

        for location in location_data:
            if total_hr_requests < UBER_REQUEST_LIMIT - 1 and elapsed_time < 3590:
                # Run routines from the Uber and Lyft APIs that get the desired data
                try:
                    data = [location, trip_distance, uber_query(location, trip_distance),
                            lyft_query(location, trip_distance), weather_query(location)]
                except IndexError:
                    while False:
                        data = [location, trip_distance, uber_query(location, trip_distance),
                                lyft_query(location, trip_distance), weather_query(location)]

                STATUS_OUT = open(STATS_FILE_LOCATION, "w")
                STATUS_OUT.write("Elapsed Time: " + str(elapsed_time) + " s | ")
                print("Elapsed Time: " + str(elapsed_time) + " s | ", end="")
                STATUS_OUT.write("Querying: " + str(location[0]) + " | ")
                print("Querying: " + str(location[0]) + " | ", end="")
                STATUS_OUT.write("Total locations queried: " + str(total_locations) + " | ")
                print("Total locations queried: " + str(total_locations) + " | ", end="")
                STATUS_OUT.write("Uber requests made: " + str(total_hr_requests))
                print("Uber requests made: " + str(total_hr_requests) + "\n", end="")
                STATUS_OUT.close()

                count += 1
                total_locations += 1
                total_hr_requests += num_uber_requests

                if count < num_locations:
                    CSV_write(data, False)
                else:
                    CSV_write(data, True)
                    count = 0
                    run += 1

                elapsed_time = time.time() - start_time
            else:
                while elapsed_time < 3600:
                    STATUS_OUT = open(STATS_FILE_LOCATION, "w")
                    STATUS_OUT.write("Starting new run in " + str(3600 - elapsed_time) + " seconds\n")
                    print("Starting new run in " + str(3600 - elapsed_time) + " seconds\n", end="")
                    STATUS_OUT.close()
                    elapsed_time = time.time() - start_time

                STATUS_OUT = open(STATS_FILE_LOCATION, "w")
                STATUS_OUT.write("New hour, resuming data collection\n")
                # print("New hour, resuming data collection\n", end="")
                STATUS_OUT.close()
                count = 0
                run = 0
                total_locations = 0
                total_hr_requests = 0
                start_time = time.time()


# Program start point
main()