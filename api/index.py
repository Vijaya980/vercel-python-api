import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Load marks data
with open("q-vercel-python.json", "r") as file:
    marks_data = {entry["name"].strip(): entry["marks"] for entry in json.load(file)}

# Print the first few names for debugging
print("Sample Data:", list(marks_data.keys())[:10])  # Print some names from JSON

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Received GET request")  # Debugging log

        # Parse query parameters
        query_components = parse_qs(urlparse(self.path).query)
        names = query_components.get("name", [])
        
        print("Query Params:", query_components)  # Debugging log
        print("Names received:", names)  # Debugging log

        # Ensure names are stripped of spaces and matched in lowercase
        names = [name.strip() for name in names]

        # Fetch marks
        marks = [marks_data.get(name, "Not Found") for name in names]
        
        print("Marks found:", marks)  # Debugging log

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = json.dumps({"marks": marks})
        print("Response:", response)  # Debugging log

        self.wfile.write(response.encode('utf-8'))