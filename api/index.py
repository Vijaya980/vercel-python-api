import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Load marks data
with open("q-vercel-python.json", "r") as file:
    marks_data = {entry["name"]: entry["marks"] for entry in json.load(file)}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        query_components = parse_qs(urlparse(self.path).query)
        names = query_components.get("name", [])

        # Fetch marks for the provided names
        marks = [marks_data.get(name, 0) for name in names]

        # Send response with CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow all origins
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')  # Allow GET requests
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')  # Allow content-type header
        self.end_headers()
        
        self.wfile.write(json.dumps({"marks": marks}).encode('utf-8'))

    def do_OPTIONS(self):  # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
