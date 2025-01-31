import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Load marks data
with open("q-vercel-python.json", "r") as file:
    marks_data = {entry["name"]: entry["marks"] for entry in json.load(file)}

# Print the first few entries to check if data is loaded correctly
print("Marks Data Sample:", list(marks_data.items())[:5])  # Debugging log

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Received GET request")  # Debugging log

        # Parse query parameters
        query_components = parse_qs(urlparse(self.path).query)
        names = query_components.get("name", [])
        
        print("Query Params:", query_components)  # Debugging log
        print("Names received:", names)  # Debugging log

        # Ensure names are stripped of extra spaces and case-matched
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

        
        self.wfile.write(json.dumps({"marks": marks}).encode('utf-8'))
        return

    def do_OPTIONS(self):  # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return

