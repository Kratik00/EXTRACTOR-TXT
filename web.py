from flask import Flask

web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running by lucifer"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
  
