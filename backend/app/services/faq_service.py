import json
from pathlib import Path

FAQ_PATH=Path(__file__).parent/"faq.json"

def look_for_faq(question:str):

    with open(FAQ_PATH,"r", encoding="utf-8") as f:
        faq_data=json.load(f)
    
    for q,ans in faq_data.items():
        if question.lower() in q.lower():
            return ans
    return None
