# import querying framework
from AgentQueryFramework import *

# import the Lyft API
from lyft_rides.client import LyftRidesClient
from lyft_rides.auth import ClientCredentialGrant
from lyft_rides.errors import *

# Turn Sandbox on or off
SANDBOX = False

# OAuth 2.0 credentials
LYFT_CLIENT_ID = "0tpC1zzUT8tI"
LYFT_CLIENT_SECRET = "4aHEKYwthtMJPUNfkvehFVg2710j0Xj-"
LYFT_PERMISSION_SCOPES = "public"


# Main call sequence
def lyft_query(location, dist):
    lyft_session_reg = get_lyft_session()
    lyft_client_reg = LyftRidesClient(lyft_session_reg)

    # retrieve data from the Lyft API
    num_drivers = [get_nearby_lyft_drivers(lyft_client_reg, location)]
    eta = [get_lyft_eta(lyft_client_reg, location)]
    prices = [get_lyft_price_estimates(lyft_client_reg, location, dist)]

    return [eta, prices, num_drivers]


# returns the price estimates for each product at the given location to an endpoint
def get_lyft_price_estimates(client, location, dist):
    end_location = get_end_coordinates(location, dist)

    response = client.get_cost_estimates(
        start_latitude=location[1],
        start_longitude=location[2],
        end_latitude=end_location[0],
        end_longitude=end_location[1]
    )
    price_response = response.json.get('cost_estimates')

    this_location = [location[0]]

    for price in price_response:
        ride_type = json_parse(price, 'display_name')
        ride_price_min = clean(json_parse(price, 'estimated_cost_cents_min'))
        ride_price_max = clean(json_parse(price, 'estimated_cost_cents_max'))
        ride_price_min = float(ride_price_min) / 100
        ride_price_max = float(ride_price_max) / 100

        ride_surge = clean(json_parse(price, 'primetime_percentage'))
        ride_surge = 1 + (int(ride_surge) / 100)

        ride_price = ""
        if ride_price_min == ride_price_max:
            ride_price = "$" + str(ride_price_min)
        else:
            ride_price_avg = (float(ride_price_min) + float(ride_price_max)) / 2
            ride_price = "$" + str(ride_price_avg)

        if ride_type.find("\'Lyft Plus\'") > -1:
            this_location.append(["LyftPlus", ride_price, ride_surge])
        elif ride_type.find("\'Lyft Line\'") > -1:
            this_location.append(["LyftLine", ride_price, ride_surge])
        elif ride_type.find("\'Lyft\'") > -1:
            this_location.append(["LyftReg", ride_price, ride_surge])

    return this_location


# returns the ETA of each product type at each location
def get_lyft_eta(client, location):
    eta_response = []

    try:
        response = client.get_pickup_time_estimates(location[1], location[2])
        eta_response = response.json.get('eta_estimates')
    except (ClientError, ServerError, HTTPError, UnknownHttpError):
        while False:
            response = client.get_pickup_time_estimates(location[1], location[2])
            eta_response = response.json.get('eta_estimates')

    this_location = [location[0]]

    for eta in eta_response:
        ride_type = json_parse(eta, 'display_name')
        ride_eta = clean(json_parse(eta, 'eta_seconds'))

        if ride_type.find("\'Lyft Plus\'") > -1:
            this_location.append(["LyftPlus", ride_eta])
        elif ride_type.find("\'Lyft Line\'") > -1:
            this_location.append(["LyftLine", ride_eta])
        elif ride_type.find("\'Lyft\'") > -1:
            this_location.append(["LyftReg", ride_eta])

    return this_location


# returns the number of drivers for each product at the given location
def get_nearby_lyft_drivers(client, location):
    nearby_drivers = []

    try:
        response = client.get_drivers(location[1], location[2])
        nearby_drivers = response.json.get('nearby_drivers')
    except (ClientError, ServerError, HTTPError, UnknownHttpError):
        while False:
            response = client.get_drivers(location[1], location[2])
            nearby_drivers = response.json.get('nearby_drivers')

    this_location = [location[0]]

    for i in nearby_drivers:
        if str(i).find("\'lyft_plus\'") > -1:
            this_location.append(["LyftPlus", str(i).count("lng")])
        elif str(i).find("\'lyft_line\'") > -1:
            this_location.append(["LyftLine", str(i).count("lng")])
        elif str(i).find("\'lyft\'") > -1:
            this_location.append(["LyftReg", str(i).count("lng")])

    return this_location


# Initiates a Lyft session
def get_lyft_session():
    auth_flow = ClientCredentialGrant(
        client_id=LYFT_CLIENT_ID,
        client_secret=LYFT_CLIENT_SECRET,
        scopes=LYFT_PERMISSION_SCOPES
    )

    session = auth_flow.get_session()

    return session
