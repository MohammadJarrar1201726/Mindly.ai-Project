from app import app
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    app.run(debug=os.getenv('DEBUG') == 'True')
