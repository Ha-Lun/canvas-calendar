# Canvas Calendar Auto-Sync 📅

An automated Python script that fetches upcoming deadlines and events from the Canvas LMS API and generates a subscribe-able `.ics` calendar feed. 

This project uses GitHub Actions to run automatically, ensuring your personal Apple/Google Calendar stays perfectly in sync with your university assignments without requiring any manual updates or local hosting.

## Features
* **Automated Syncing:** Runs on a schedule every 6 hours via GitHub Actions.
* **Direct Calendar Integration:** Generates a standard `canvas_events.ics` file that can be plugged directly into Google Calendar, Apple Calendar, or Outlook.
* **Secure:** Uses environment variables and GitHub Secrets so your personal Canvas API token is never exposed to the public.
