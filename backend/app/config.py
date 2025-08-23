from dotenv import load_dotenv
import os 

load_dotenv()

GEMINI_API_KEY=os.getenv("GOOGLE_API_KEY")
PORT=os.getenv("PORT")