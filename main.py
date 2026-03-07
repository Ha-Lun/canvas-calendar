import os
import requests
from icalendar import Calendar, Event
from datetime import datetime
from dotenv import load_dotenv

# Load variables from the .env file for local testing
load_dotenv()

CANVAS_URL = os.getenv("CANVAS_URL")
CANVAS_TOKEN = os.getenv("CANVAS_TOKEN")

def fetch_canvas_events():
    headers = {"Authorization": f"Bearer {CANVAS_TOKEN}"}
    # The endpoint for upcoming assignments and events
    url = f"{CANVAS_URL}/api/v1/users/self/upcoming_events"
    
    print(f"Connecting to {url}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Could not fetch data. Status code: {response.status_code}")
        print(response.text)
        return []
        
    return response.json()

def create_ics(events):
    if not events:
        print("No events found to add to the calendar.")
        return

    cal = Calendar()
    cal.add('prodid', '-//My Canvas Calendar//')
    cal.add('version', '2.0')

    for item in events:
        event = Event()
        
        # 1. Add Title
        event.add('summary', item.get('title', 'Untitled Canvas Event')) 
        
        # 2. Add Start Time
        if item.get('start_at'):
            start_time = datetime.fromisoformat(item['start_at'].replace('Z', '+00:00'))
            event.add('dtstart', start_time)
        
        # 3. Add End Time
        if item.get('end_at'):
            end_time = datetime.fromisoformat(item['end_at'].replace('Z', '+00:00'))
            event.add('dtend', end_time)
            
        # 4. Add the Canvas Link to the description
        event.add('description', f"Canvas Link: {item.get('html_url', 'No link available')}")
        
        cal.add_component(event)

    # Save the file locally
    with open('canvas_events.ics', 'wb') as f:
        f.write(cal.to_ical())
    print(f"Success! Saved {len(events)} events to canvas_events.ics")

if __name__ == "__main__":
    events = fetch_canvas_events()
    create_ics(events)