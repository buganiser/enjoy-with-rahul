#!/usr/bin/env python3
"""
Create Jira tickets for "Enjoy with R@hul" project
"""

import os
import json
import requests
from requests.auth import HTTPBasicAuth

# Jira credentials from environment variables
JIRA_EMAIL = os.environ.get("JIRA_EMAIL")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")
JIRA_BASE_URL = "https://anub131091.atlassian.net"
PROJECT_KEY = "SCRUM"

if not JIRA_EMAIL or not JIRA_API_TOKEN:
    print("Error: JIRA_EMAIL and JIRA_API_TOKEN environment variables must be set")
    exit(1)

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
headers = {"Accept": "application/json", "Content-Type": "application/json"}

def create_issue(fields):
    """Create a Jira issue"""
    url = f"{JIRA_BASE_URL}/rest/api/3/issue"
    payload = {"fields": fields}
    response = requests.post(url, json=payload, headers=headers, auth=auth)
    if response.status_code == 201:
        return response.json()
    else:
        print(f"Error creating issue: {response.status_code}")
        print(response.text)
        return None

def create_epic(summary, description):
    """Create an Epic"""
    fields = {
        "project": {"key": PROJECT_KEY},
        "summary": summary,
        "description": {
            "type": "doc",
            "version": 1,
            "content": [{
                "type": "paragraph",
                "content": [{"type": "text", "text": description}]
            }]
        },
        "issuetype": {"name": "Epic"},
    }
    return create_issue(fields)

def create_story(summary, description, epic_key, story_points, labels=None):
    """Create a Story linked to an Epic"""
    fields = {
        "project": {"key": PROJECT_KEY},
        "summary": summary,
        "description": {
            "type": "doc",
            "version": 1,
            "content": [{
                "type": "paragraph",
                "content": [{"type": "text", "text": description}]
            }]
        },
        "issuetype": {"name": "Story"},
        "priority": {"name": "Medium"},
        "labels": labels or [],
    }
    if story_points:
        fields["customfield_10016"] = story_points  # Story Points field
    if epic_key:
        fields["customfield_10014"] = epic_key  # Epic Link field
    return create_issue(fields)

def create_bug(summary, description, epic_key, priority, labels=None):
    """Create a Bug linked to an Epic"""
    fields = {
        "project": {"key": PROJECT_KEY},
        "summary": summary,
        "description": {
            "type": "doc",
            "version": 1,
            "content": [{
                "type": "paragraph",
                "content": [{"type": "text", "text": description}]
            }]
        },
        "issuetype": {"name": "Bug"},
        "priority": {"name": priority},
        "labels": labels or [],
    }
    if epic_key:
        fields["customfield_10014"] = epic_key  # Epic Link field
    return create_issue(fields)

# ============================================================
# EPICS
# ============================================================
epics = [
    ("SCRUM-1", "Booking System", "Core booking functionality for dining reservations and room stays"),
    ("SCRUM-2", "Food Menu Display", "Display food categories and items with details"),
    ("SCRUM-3", "Room Management", "Room listings with pricing, images, and booking integration"),
    ("SCRUM-4", "UI/UX Improvements", "Navigation, responsiveness, hero sections, user experience"),
    ("SCRUM-5", "Technical Debt & Bugs", "Fix existing bugs, add validation, database persistence"),
]

epic_keys = {}
print("Creating Epics...")
for key, summary, desc in epics:
    result = create_epic(summary, desc)
    if result:
        epic_keys[key] = result["key"]
        print(f"  Created {result['key']}: {summary}")
    else:
        print(f"  FAILED to create Epic: {summary}")

print(f"\nEpic keys: {epic_keys}")

# ============================================================
# STORIES
# ============================================================
stories = [
    # Booking System (SCRUM-1)
    ("Dining Reservation", "As a customer, I can book a dining reservation so that I can reserve a table. Form accepts name, email, phone, date, guests, food preference. Validation on all fields. Confirmation page shows all details.", "SCRUM-1", 3, ["booking"]),
    ("Stay/Room Booking", "As a customer, I can book a room stay so that I can reserve accommodation. Form accepts name, email, phone, check-in, check-out, guests, room type, food preference. Date validation (check-out > check-in, no past dates). Confirmation page shows all details.", "SCRUM-1", 3, ["booking"]),
    ("Booking Confirmation", "As a customer, I receive confirmation details after booking so that I have a record. Thank you page displays all submitted fields correctly for both booking types. Email confirmation sent (future).", "SCRUM-1", 2, ["booking"]),
    ("Admin Booking View", "As an admin, I can view all bookings so that I can manage reservations. Admin dashboard lists all bookings. Filter by type (dining/stay), date, status. Export to CSV.", "SCRUM-1", 5, ["admin"]),

    # Food Menu Display (SCRUM-2)
    ("Food Categories", "As a customer, I can view food categories so that I can browse the menu. Categories: Salads, Curries, Beverages, Desserts. Clickable cards navigate to category pages.", "SCRUM-2", 2, ["food"]),
    ("Menu Item Details", "As a customer, I can see item details so that I can make informed choices. Each item shows name, ingredients, price. Consistent layout across categories.", "SCRUM-2", 2, ["food"]),
    ("Dynamic Menu Data", "As an admin, I can manage menu items so that I can update offerings. CRUD for menu items in admin panel. Categories managed separately.", "SCRUM-2", 5, ["admin"]),

    # Room Management (SCRUM-3)
    ("Room Listings", "As a customer, I can view room types with pricing so that I can choose the best option. 4 room types: Single, Double, Double+Extra Bed, Deluxe. Each shows pricing tiers (Without Food, Veg, Non-Veg). Book Now button links to booking form.", "SCRUM-3", 2, ["rooms"]),
    ("Room Images", "As a customer, I can see room images so that I know what to expect. Each room card displays relevant image. Images load correctly (fixed from bug).", "SCRUM-3", 1, ["rooms"]),
    ("Room Availability", "As a customer, I can see room availability so that I don't book unavailable rooms. Calendar integration showing booked dates. Real-time availability check.", "SCRUM-3", 8, ["rooms"]),

    # UI/UX Improvements (SCRUM-4)
    ("Responsive Navigation", "As a user, I see a responsive navigation bar so that I can navigate easily on mobile/desktop. Hamburger menu on mobile. All links work on all screen sizes.", "SCRUM-4", 2, ["ui"]),
    ("Hero Section with CTA", "As a user, I see a hero section with CTA so that I'm guided to book. Home page hero with 'Book Your Stay' button. Food page hero with 'Book a Table' button. Rooms page hero.", "SCRUM-4", 2, ["ui"]),
    ("Footer & Social Links", "As a user, I see footer with contact/social info so that I can reach out. Contact info displayed. Social media links (FB, Instagram, Twitter).", "SCRUM-4", 1, ["ui"]),
    ("Testimonials Section", "As a user, I see guest testimonials so that I trust the service. Carousel or grid of testimonials. Admin can add/edit testimonials.", "SCRUM-4", 3, ["ui"]),
]

print("\nCreating Stories...")
for summary, desc, epic, points, labels in stories:
    epic_key = epic_keys.get(epic)
    result = create_story(summary, desc, epic_key, points, labels)
    if result:
        print(f"  Created {result['key']}: {summary}")
    else:
        print(f"  FAILED to create Story: {summary}")

# ============================================================
# BUGS
# ============================================================
bugs = [
    ("Thank you page missing dining fields", "Dining booking confirmation doesn't show date and food preference. Steps: 1. Go to /booking 2. Fill dining form 3. Submit 4. Observe thank you page. Expected: Thank you page shows name, email, phone, date, guests, food preference.", "SCRUM-5", "High", ["bug", "critical"]),
    ("Room images broken", "Room cards show broken image icons due to wrong filenames. Steps: 1. Go to /rooms 2. Observe room cards. Expected: All 4 room cards display correct images (bedroom-1.jpg through bedroom-4.jpg).", "SCRUM-5", "High", ["bug", "critical"]),
    ("No server-side form validation", "Forms accept empty/invalid data; XSS risk via unsanitized inputs. Steps: 1. Submit empty booking form 2. Submit with <script>alert(1)</script> in name field. Expected: Server rejects invalid data; all outputs escaped.", "SCRUM-5", "Critical", ["security", "critical"]),
    ("No client-side date validation", "Users can select past dates; check-out before check-in. Steps: 1. Go to booking form 2. Select past date for check-in 3. Select check-out before check-in. Expected: Date pickers restrict to today+; check-out min = check-in + 1 day.", "SCRUM-5", "High", ["validation", "major"]),
    ("No database persistence", "Bookings only shown on confirmation page; lost on refresh. Steps: 1. Submit booking 2. Refresh thank you page 3. No record exists. Expected: Bookings stored in database; admin can view all.", "SCRUM-5", "High", ["backend", "major"]),
    ("No email confirmations", "Customers don't receive email receipt of booking. Steps: 1. Complete booking 2. Check email. Expected: Confirmation email sent to customer email.", "SCRUM-5", "Medium", ["email", "normal"]),
    ("Hardcoded secret key", "Flask secret key hardcoded in app.py. Steps: 1. View app.py 2. See app.secret_key = 'your-secret-key...'. Expected: Secret key from environment variable.", "SCRUM-5", "Medium", ["security", "normal"]),
    ("No CSRF protection", "Forms vulnerable to CSRF attacks. Steps: 1. Craft malicious form submission. Expected: CSRF tokens on all forms.", "SCRUM-5", "Medium", ["security", "normal"]),
]

print("\nCreating Bugs...")
for summary, desc, epic, priority, labels in bugs:
    epic_key = epic_keys.get(epic)
    result = create_bug(summary, desc, epic_key, priority, labels)
    if result:
        print(f"  Created {result['key']}: {summary}")
    else:
        print(f"  FAILED to create Bug: {summary}")

print("\n✅ Done! Check your Jira board: https://anub131091.atlassian.net/jira/software/projects/SCRUM/boards/1")