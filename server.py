from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime, date

def downloadData():
    f = open('source.json')
    data = json.load(f)
    f.close()
    return data

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        # self.wfile.write(b'Hello, world!')
        dcurrPos = getCurrentPosition()
        jsonCurrPos = json.dumps(dcurrPos, indent = 4)
        self.wfile.write(bytes(jsonCurrPos, 'utf-8'))

def getCurrentPosition():
    data = downloadData()
    #let's get the current time, but make it simple.
    currTime = datetime.now().hour * 100 + datetime.now().minute
    for x in data['destinations']:
        depart = datetime.utcfromtimestamp(int(x['departure'])/1000) #we gotta convert the strings to date objects so we can work with them
        depart = depart.replace(hour = (depart.hour + 14) % 24) #the datasource timestamps are 10 hours off (my tz plus origin tz not mapped properly) so we'll advance them 24 hours, back them up by 10, and mod 24 to get it between 0..23
        depart = depart.hour * 100 + depart.minute #let's convert the times into a simple number to make it really easy to compare
        if currTime <= depart: #let's see if we know his current position
            return x

print("Connecting to Santa Actual Nighttime Telemetry and Altimiter (SANTA) satellite network...")
print("If you experience errors connecting to Santa Actual Nighttime Telemetry and Altimiter (SANTA) satellite network. See https://www.youtube.com/watch?v=6-HUgzYPm9g for assistance.")
print("Preparing to host services on port 8000")
httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
print("Ready.")
httpd.serve_forever()
