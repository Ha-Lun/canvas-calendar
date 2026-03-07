import os
import requests
from icalendar import Calendar, Event
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

CANVAS_URL = os.getenv("CANVAS_URL")
CANVAS_TOKEN = os.getenv("CANVAS_TOKEN")

def fetch_canvas_events():
    headers = {"Authorization": f"Bearer {CANVAS_TOKEN}"}
    
    # Use the Planner Items API to look 6 months into the future
    start_date = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d")
    
    url = f"{CANVAS_URL}/api/v1/planner/items?start_date={start_date}&end_date={end_date}&per_page=100"
    
    print(f"Connecting to {url}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Could not fetch data. Status code: {response.status_code}")
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
        # Planner items wrap the details inside a 'plannable' dictionary
        plannable = item.get('plannable', {})
        
        event = Event()
        
        # 1. Add Title
        title = plannable.get('title', 'Untitled Canvas Event')
        
        # Add the course name to the title if Canvas provides it
        course_name = item.get('context_name', '')
        if course_name:
            title = f"[{course_name}] {title}"
            
        event.add('summary', title)
        
        # 2. Add Start Time
        # Planner items use 'plannable_date' for the actual deadline
        event_date = item.get('plannable_date')
        if event_date:
            start_time = datetime.fromisoformat(event_date.replace('Z', '+00:00'))
            event.add('dtstart', start_time)
            # Make the end time the same as the start time (since it's a deadline)
            event.add('dtend', start_time)
            
        # 3. Add the Canvas Link
        html_url = item.get('html_url') or plannable.get('html_url')
        if html_url:
            # Planner URLs are often relative, so we append the base URL
            full_url = f"{CANVAS_URL}{html_url}" if html_url.startswith('/') else html_url
            event.add('description', f"Canvas Link: {full_url}")
        
        cal.add_component(event)

    with open('canvas_events.ics', 'wb') as f:
        f.write(cal.to_ical())
    print(f"Success! Saved {len(events)} events to canvas_events.ics")

if __name__ == "__main__":
    events = fetch_canvas_events()
    create_ics(events)