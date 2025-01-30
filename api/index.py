import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Load marks data from the uploaded file
with open("q-vercel-python.json", "r") as file:
    marks_data = {entry["name"]: entry["marks"] for entry in json.load(file)}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        query_components = parse_qs(urlparse(self.path).query)
        names = query_components.get("name", [])

        # Fetch marks for the provided names
        marks = [marks_data.get(name, 0) for name in names]

        # Prepare the response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Enable CORS
        self.end_headers()
        
        self.wfile.write(json.dumps({"marks": marks}).encode('utf-8'))
