# RECO7609 Story Writer Webapp python backend server

#Prompt:

#Please generate a story writer webapp with html as the frontend and python as the backend without the use of external libraries in any part of the code.

#The webapp should have:
#1. Input box for user to input words
#2. have a write button for user to confirm input the word
#3. have a box above the input box to show the story inputed by the user
#4. have another thin box between the box and the input box labelled "Next Word"
#5. Have a box under the input box labelled "Auto  Complete"


from http.server import BaseHTTPRequestHandler, HTTPServer
import json

story = []

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(json.dumps({'story': ' '.join(story)}).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        word = json.loads(post_data)['word']
        story.append(word)
        self._set_headers()
        self.wfile.write(json.dumps({'story': ' '.join(story)}).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()

