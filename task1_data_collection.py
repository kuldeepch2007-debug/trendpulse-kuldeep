import requests
import json
import time 
import os
from datetime import datetime

#Headers is used for introduction of ourself to the server

headers = {"User-Agent": "TrendPulse/1.0"}

KEYWORDS = {
    "technology": ["AI", "software","tech", "code","computer","data","cloud","API","GPU","LLM"],
    "worldnews": ["war","government","country","president","election","climate","attack","global"],
    "sports": ["NFL","NBA","FIFA","sport","game","team","player","league","championship"],
    "science": ["research","study","space","physics","biology","discovery","NASA","genome"],
    "entertainment": ["movie","film","music","Netflix","game","book","show","award","streaming"],
}

#fetching the list of ids from Hackernews

url = "https://hacker-news.firebaseio.com/v0/topstories.json"
response = requests.get(url, headers=headers)
story_ids = response.json()[:500]

session = requests.Session()

'''this function is used to fetch the story id 
we used try and except to avoid crashing'''

def fetch_story(story_id):
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    try:
        response = session.get(url,headers=headers)
        return response.json()
    except Exception as e:
        print(f"Failed to fetch {story_id}: {e}")
        return None

'''this function checks every word and if that word matches with a keyword of any category that is categorised 
example : the openai launches an offer for students
the function checks ai in the sentence and categorizes it  into technology '''

def categorize(title):
    title_lower = title.lower()
    for category,keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category
    return None        

all_stories = []

#for each category,we check the story ids and fetch the story details

for category in KEYWORDS:
    print(f"collecting {category}....")
    collected = []
    
    for story_id in story_ids:
        if len(collected) >= 25:
            break         #for each category 25 stories are enough so we used break when 25 stories collected
        
        story = fetch_story(story_id)
        if story is None:
            continue      #we skipped on none because the story is not getting, and we used continue, so we can get the next story
        
        title = story.get("title")
        if not title:
            continue
        
        story_category = categorize(title)
        if story_category != category:
            continue
        
        story_data = {
           "post_id" : story.get("id"),
           "title" : title,
           "category" : category,
           "score": story.get("score"),
           "num_comments": story.get("descendants"),
           "author":story.get("by"),
           "collected_at": datetime.now().isoformat()
        }
        collected.append(story_data)
    time.sleep(2)
    all_stories.extend(collected)
    print(f"   -> {category}: {len(collected)} collected")
print(f"Total collected: {len(all_stories)}")   

#creates a folder named data and if it is already created it ignores it
#creates filename example data/trends_20260824.json
#open the created file and adds the information in json format


os.makedirs("data", exist_ok=True)
filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"
with open(filename, "w") as f:
    json.dump(all_stories, f, indent=2)

print(f"Collected {len(all_stories)} stories. Saved to {filename}")    
