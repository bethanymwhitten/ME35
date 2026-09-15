#importing the libraries
import network
import urequests
import time
 
#setting up SSID and password 
SSID = "tufts_eecs" #use tufts_eecs
PASSWORD = "foundedin1883" #foundedin1883

#function definition 
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
    print("Connected! IP address:", wlan.ifconfig()[0])
    return wlan
 
#function call
connect_wifi()

URL = "https://api-v3.mbta.com/predictions";
MBTA_API_KEY = "a0900ee8c0364a38a1c7a3aeafbd312f"
STOP_ID = "5035"; # 55 George St opp Wedgemere Rd
ROUTE_ID = "96";
DIRECTION_ID = "1"; # inbound: Medford Square -> Harvard

MBTA_URL = (
    URL
    + "?filter[stop]=" + STOP_ID
    + "&filter[route]=" + ROUTE_ID
    + "&filter[direction_id]=" + DIRECTION_ID
    + "&api_key=" + MBTA_API_KEY)
            
print(MBTA_URL)

response = urequests.get(MBTA_URL)
data = response.json()
response.close()


# ISS_URL = "http://api.open-notify.org/iss-now.json"
# response = urequests.get(ISS_URL)
# data = response.json()
# response.close()

print(data)