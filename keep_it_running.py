from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Assalamualikum. I am here!"

def create_app():
   return app
    
