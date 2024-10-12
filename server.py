# RECO7609 Story Writer Webapp python backend server

#Prompt:

#At a "End Story" button at the bottom to close the python backend server without using threading

#----------------------------------------
#Exception occurred during processing of request from ('127.0.0.1', 58894)
#Traceback (most recent call last):
#  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/socketserver.py", line 316, in _handle_request_noblock
#    self.process_request(request, client_address)
#  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/socketserver.py", line 347, in process_request
#    self.finish_request(request, client_address)
#  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/socketserver.py", line 360, in finish_request
#    self.RequestHandlerClass(request, client_address, self)
#  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/socketserver.py", line 747, in __init__
#    self.handle()
#  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/http/server.py", line 434, in handle
#    self.handle_one_request()
#  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/http/server.py", line 422, in handle_one_request
#    method()
#  File "/Users/tcn/Documents/DMBA/RECO7609/Story writer app/7. WIth End server trial/server.py", line 112, in do_POST
#    data = json.loads(post_data)
#  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/__init__.py", line 346, in loads
#    return _default_decoder.decode(s)
#  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/decoder.py", line 337, in decode
#    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
#  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/decoder.py", line 355, in raw_decode
#    raise JSONDecodeError("Expecting value", s, err.value) from None
#json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

#Shut down port 8080 only and not 8000


#----------------------------------------------------------------------------------------------------------------------------------


from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from collections import defaultdict
import threading

# Sample story data
sample_story = """
Once upon a time in a small village nestled between the mountains, there lived a young girl named Elara. She had a curious spirit and an insatiable desire for adventure. Every morning, she would wander into the lush forests that surrounded her home, dreaming of the magical creatures that might be hiding among the trees.

One sunny day, as Elara explored deeper into the woods than ever before, she stumbled upon a shimmering pond. The water sparkled like diamonds under the sunlight, and as she approached, she noticed a small, iridescent fish swimming gracefully. 

"Hello there," Elara called out, leaning closer. "What are you doing in this pond all alone?"

To her surprise, the fish leaped out of the water and spoke in a melodic voice, "I am not alone, dear girl. I am the guardian of this pond, and I grant wishes to those who are pure of heart."

Elara's eyes widened with wonder. "Really? I’ve always wanted to explore the world beyond my village. Can you help me?"

The fish nodded, its scales glinting. "If your heart is true and your intentions are noble, I will grant you one wish."

Elara thought for a moment, weighing her options. She could wish for riches, fame, or even the ability to fly. But deep down, she knew what she truly desired. 

"I wish to embark on an adventure that will help others," she declared boldly. 

With a flick of its tail, the fish created a burst of sparkling water that enveloped Elara. In an instant, she found herself standing in a bustling marketplace filled with people from all walks of life. 

As she looked around, Elara realized that her adventure had just begun. Each person she encountered had their own story, and she felt a deep urge to listen, to learn, and to lend a hand wherever she could. 

And so, with courage in her heart and a spirit ready for discovery, Elara set forth into the unknown, ready to make a difference in the world.
"""

# Bigram model
class BigramModel:
    def __init__(self, sample_story):
        self.bigrams = defaultdict(list)
        self.words = sample_story.split()
        for i in range(len(self.words) - 1):
            self.bigrams[self.words[i]].append(self.words[i + 1])

    def predict_next_word(self, current_text):
        current_words = current_text.split()
        last_word = current_words[-1] if current_words else ""
        possible_next_words = self.bigrams[last_word]
        if possible_next_words:
            return possible_next_words[0]  # Returns the first possible word
        return ""

    def get_suggestions(self, current_text):
        current_words = current_text.split()
        last_word = current_words[-1] if current_words else ""
        suggestions = [word for word in self.bigrams if word.startswith(last_word)]
        unique_suggestions = list(dict.fromkeys(suggestions))  # Remove duplicates
        return unique_suggestions[:6]  # Limit to six suggestions

# Trigram model
class TrigramModel:
    def __init__(self, sample_story):
        self.trigrams = defaultdict(list)
        self.words = sample_story.split()
        for i in range(len(self.words) - 2):
            key = (self.words[i], self.words[i + 1])
            self.trigrams[key].append(self.words[i + 2])

    def predict_next_word(self, current_text):
        current_words = current_text.split()
        if len(current_words) < 2:
            return ""
        last_two_words = (current_words[-2], current_words[-1])
        possible_next_words = self.trigrams[last_two_words]
        if possible_next_words:
            return possible_next_words[0]  # Returns the first possible word
        return ""

    def get_suggestions(self, current_text):
        current_words = current_text.split()
        last_word = current_words[-1] if current_words else ""
        suggestions = [word for word in self.words if word.startswith(last_word)]
        unique_suggestions = list(dict.fromkeys(suggestions))  # Remove duplicates
        return unique_suggestions[:6]  # Limit to six suggestions

bigram_model = BigramModel(sample_story)
trigram_model = TrigramModel(sample_story)
story = []
model_type = "bigram"  # Default model type

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()
        next_word = bigram_model.predict_next_word(' '.join(story)) if model_type == "bigram" else trigram_model.predict_next_word(' '.join(story))
        response = {
            'story': ' '.join(story),
            'next_word': next_word,
            'button_text': 'Write' if not story or not next_word else 'Use predicted word'
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        global model_type
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        if self.path == '/end':
            response = {'message': 'Server is shutting down...'}
            self._set_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            threading.Thread(target=httpd.shutdown).start()
            return
        
        data = json.loads(post_data)
        next_word = ""
        
        if self.path == '/write':
            word = data.get('word', '').strip()
            if not word:
                if model_type == "bigram":
                    word = bigram_model.predict_next_word(' '.join(story))
                else:
                    word = trigram_model.predict_next_word(' '.join(story))
            story.append(word)
            next_word = bigram_model.predict_next_word(' '.join(story)) if model_type == "bigram" else trigram_model.predict_next_word(' '.join(story))
            response = {
                'story': ' '.join(story),
                'next_word': next_word,
                'button_text': 'Write' if not next_word else 'Use predicted word'
            }
        
        elif self.path == '/switch':
            model_type = data.get('model_type', model_type)
            next_word = bigram_model.predict_next_word(' '.join(story)) if model_type == "bigram" else trigram_model.predict_next_word(' '.join(story))
            response = {
                'next_word': next_word,
                'button_text': 'Write' if not story or not next_word else 'Use predicted word'
            }
        
        elif self.path == '/auto-complete':
            current_text = data.get('text', '').strip()
            if model_type == "bigram":
                suggestions = bigram_model.get_suggestions(current_text)
            else:
                suggestions = trigram_model.get_suggestions(current_text)
            response = {
                'suggestions': suggestions,
                'button_text': 'Write' if current_text else ('Use predicted word' if story and next_word else 'Write')
            }
        
        self._set_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    global httpd
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
