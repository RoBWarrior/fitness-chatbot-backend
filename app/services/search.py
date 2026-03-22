import os
import requests
from app.core.config import SERPAI_API_KEY

def search_serpai(query: str, num_results: int=5):
    url="https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERPAI_API_KEY,
        "engine": "google",
        "num": num_results
    }
    try:
        res=requests.get(url, params=params)
        data=res.json()
        results=[]
        
        for item in data.get("organic_results", []):
            results.append(f"{item.get('title')}: {item.get('snippet')}")
            
        return results
       
    except Exception as e:
        print(f"An error occured while searching about the topic {e}")