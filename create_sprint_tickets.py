#!/usr/bin/env python3
"""
Create Jira tickets for bugs/modifications found in code review.
Targets existing SCRUM project using working Basic Auth via Atlassian Gateway.
"""

import os
import sys
import requests
from requests.auth import HTTPBasicAuth

# Load from environment
JIRA_EMAIL = os.environ.get("JIRA_EMAIL")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")
JIRA_CLOUD_ID = os.environ.get("JIRA_CLOUD_ID")
PROJECT_KEY = "SCRUM"

if not all([JIRA_EMAIL, JIRA_API_TOKEN, JIRA_CLOUD_ID]):
    print("❌ Missing required env vars: JIRA_EMAIL, JIRA_API_TOKEN, JIRA_CLOUD_ID")
    sys.exit(1)

# Use Atlassian API Gateway with Basic Auth (proven working)
API_BASE = f"https://api.atlassian.com/ex/jira/{JIRA_CLOUD_ID}/rest/api/3"
auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
headers = {"Accept": "application/json", "Content-Type": "application/json"}

def api_post(endpoint, payload):
    url = f"{API_BASE}{endpoint}"
    r = requests.post(url, headers=headers, auth=auth, json=payload)
    return r

def api_get(endpoint, params=None):
    url = f"{API_BASE}{endpoint}"
    r = requests.get(url, headers=headers, auth=auth, params=params)
    return r

def get_project_id():
    """Get project ID from project key"""
    r = api_get(f"/project/{PROJECT_KEY}")
    if r.status_code == 200:
        return r.json().get("id")
    print(f"❌ Failed to get project: {r.status_code} - {r.text}")
    return None

def get_issue_types():
    """Get issue type IDs for the project"""
    project_id = get_project_id()
    if not project_id:
        return {}
    r = api_get("/issuetype/project", params={"projectId": project_id})
    if r.status_code == 200:
        return {it["name"].lower(): it["id"] for it in r.json()}
    print(f"❌ Failed to get issue types: {r.status_code} - {r.text}")
    return {}

def get_valid_priorities():
    """Get valid priority names"""
    r = api_get("/priority")
    if r.status_code == 200:
        return [p["name"] for p in r.json()]
    return ["Highest", "High", "Medium", "Low", "Lowest"]

def create_issue(summary, description, issue_type, priority="Medium", labels=None, components=None):
    """Create a single issue"""
    issue_types = get_issue_types()
    type_id = issue_types.get(issue_type.lower())

    if not type_id:
        print(f"   ❌ Issue type '{issue_type}' not found. Available: {list(issue_types.keys())}")
        return None

    fields = {
        "project": {"key": PROJECT_KEY},
        "summary": summary,
        "description": {
            "type": "doc",
            "version": 1,
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": description}]}]
        },
        "issuetype": {"id": type_id},
        "priority": {"name": priority},
    }
    if labels:
        fields["labels"] = labels
    if components:
        fields["components"] = [{"name": c} for c in components]

    r = api_post("/issue", {"fields": fields})
    if r.status_code == 201:
        issue = r.json()
        print(f"   ✅ {issue['key']}: {summary}")
        return issue
    else:
        print(f"   ❌ Failed: {r.status_code} - {r.text}")
        return None

# ============================================================
# TICKETS TO CREATE (from code review)
# ============================================================

BUGS = [
    {
        "summary": "Bug: Hardcoded secret key in app.py",
        "description": "Flask secret_key is hardcoded in app.py line 6:\napp.secret_key = 'your-secret-key-change-in-production'\n\nRisk: Session hijacking, CSRF bypass if deployed.\nFix: Move to environment variable: app.secret_key = os.environ.get('SECRET_KEY')",
        "issue_type": "Bug",
        "priority": "Critical",
        "labels": ["security", "config", "backend"],
        "components": ["Security", "Backend"]
    },
    {
        "summary": "Bug: No server-side form validation - XSS risk",
        "description": "Booking forms accept empty/invalid data. User input rendered unsanitized in thankyou.html.\n\nSteps to reproduce:\n1. Submit booking with <script>alert(1)</script> in name field\n2. Observe script executes in confirmation page\n\nFix: Add server-side validation + ensure all outputs escaped via markupsafe.escape()",
        "issue_type": "Bug",
        "priority": "Critical",
        "labels": ["security", "xss", "validation", "backend"],
        "components": ["Security", "Booking", "Backend"]
    },
    {
        "summary": "Bug: No CSRF protection on forms",
        "description": "All POST forms (booking, contact) lack CSRF tokens.\n\nRisk: Cross-site request forgery attacks.\nFix: Add Flask-WTF, include {{ form.csrf_token }} in all forms, validate on POST.",
        "issue_type": "Bug",
        "priority": "High",
        "labels": ["security", "csrf", "backend"],
        "components": ["Security", "Backend", "Booking"]
    },
    {
        "summary": "Bug: No database persistence for bookings",
        "description": "Bookings only shown on thankyou.html confirmation page. Data lost on refresh - no storage.\n\nExpected: Bookings stored in database; admin can view/manage.\nActual: No database; data only in memory during request.\nFix: Add SQLAlchemy + SQLite/PostgreSQL, create Booking model, persist on submit.",
        "issue_type": "Bug",
        "priority": "High",
        "labels": ["backend", "database", "persistence", "booking"],
        "components": ["Backend", "Booking", "Database"]
    },
    {
        "summary": "Bug: Thank you page missing dining booking fields",
        "description": "Dining booking confirmation doesn't show 'date' and 'food preference' fields.\n\nSteps:\n1. Go to /booking\n2. Fill dining form (name, email, phone, date, guests, food)\n3. Submit\n4. Observe thankyou.html\n\nExpected: Shows name, email, phone, date, guests, food preference\nActual: Only shows name, email, phone, guests (missing date, food)\nFix: Update thankyou.html template to conditionally render dining vs stay fields.",
        "issue_type": "Bug",
        "priority": "High",
        "labels": ["bug", "booking", "dining", "frontend"],
        "components": ["Booking", "Frontend"]
    },
    {
        "summary": "Bug: Room images broken - wrong filenames in template",
        "description": "Room cards show broken image icons due to incorrect filenames in rooms.html.\n\nTemplate references: single-room.jpg, double-room.jpg, double-extra-bed.jpg, deluxe-room.jpg\nActual files in static/images/: bedroom-1.jpg through bedroom-4.jpg\n\nFix: Update template src paths to match actual filenames.",
        "issue_type": "Bug",
        "priority": "High",
        "labels": ["bug", "rooms", "images", "frontend"],
        "components": ["Rooms", "Frontend"]
    },
    {
        "summary": "Bug: No client-side date validation",
        "description": "Date pickers allow past dates for check-in; check-out before check-in allowed.\n\nSteps:\n1. Go to booking form\n2. Select past date for check-in\n3. Select check-out before check-in\n\nExpected: Date pickers restrict min=today; check-out min=check-in+1 day\nActual: No date restrictions enforced client-side.\nFix: Add min attribute to date inputs, JS validation for check-out > check-in.",
        "issue_type": "Bug",
        "priority": "High",
        "labels": ["bug", "validation", "dates", "frontend"],
        "components": ["Booking", "Frontend"]
    },
    {
        "summary": "Bug: No email confirmations sent",
        "description": "Customers don't receive email receipt after booking.\n\nSteps:\n1. Complete booking\n2. Check email\n\nExpected: Confirmation email sent to customer email\nActual: No email functionality implemented.\nFix: Integrate Flask-Mail, send confirmation on successful booking.",
        "issue_type": "Bug",
        "priority": "Medium",
        "labels": ["bug", "email", "notifications", "booking"],
        "components": ["Booking", "Notifications"]
    },
]

TASKS = [
    {
        "summary": "Task: Move secret key to environment variable",
        "description": "Replace hardcoded secret_key in app.py with environment variable.\n\nCode change:\n- app.py: app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-change-in-prod')\n- Add SECRET_KEY to .env / deployment config",
        "issue_type": "Task",
        "priority": "Critical",
        "labels": ["security", "config", "backend"],
        "components": ["Security", "Backend", "Config"]
    },
    {
        "summary": "Task: Add Flask-WTF for CSRF protection",
        "description": "Implement CSRF protection on all forms.\n\nSteps:\n1. pip install Flask-WTF\n2. Initialize CSRFProtect(app) in app.py\n3. Update all forms in templates to include {{ form.csrf_token }}\n4. Convert form handling to use FlaskForm classes",
        "issue_type": "Task",
        "priority": "High",
        "labels": ["security", "csrf", "backend", "forms"],
        "components": ["Security", "Backend", "Booking"]
    },
    {
        "summary": "Task: Add SQLite/SQLAlchemy for booking persistence",
        "description": "Add database layer to persist bookings.\n\nSteps:\n1. pip install Flask-SQLAlchemy\n2. Create Booking model (id, type, name, email, phone, dates, guests, room, food, created_at)\n3. Initialize db in app.py\n4. On booking POST: create Booking record, commit\n5. Add admin route to view bookings",
        "issue_type": "Task",
        "priority": "Medium",
        "labels": ["backend", "database", "persistence", "booking"],
        "components": ["Backend", "Booking", "Database"]
    },
    {
        "summary": "Task: Add email confirmation system (Flask-Mail)",
        "description": "Send booking confirmation emails to customers.\n\nSteps:\n1. pip install Flask-Mail\n2. Configure MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD in env\n3. Create email templates (text + HTML)\n4. Send async email on successful booking\n5. Add admin notification option",
        "issue_type": "Task",
        "priority": "Medium",
        "labels": ["email", "notifications", "booking", "backend"],
        "components": ["Booking", "Notifications", "Backend"]
    },
    {
        "summary": "Task: Fix room image filenames in template",
        "description": "Update rooms.html to use correct image filenames.\n\nCurrent (broken): single-room.jpg, double-room.jpg, double-extra-bed.jpg, deluxe-room.jpg\nActual files: bedroom-1.jpg, bedroom-2.jpg, bedroom-3.jpg, bedroom-4.jpg\n\nMap each room type to correct bedroom-N.jpg",
        "issue_type": "Task",
        "priority": "High",
        "labels": ["frontend", "rooms", "images", "bugfix"],
        "components": ["Rooms", "Frontend"]
    },
    {
        "summary": "Task: Add client-side date validation",
        "description": "Add date picker restrictions and validation.\n\nChanges:\n- checkin input: min=\"{{ today }}\"\n- checkout input: min=\"{{ checkin + 1 day }}\" (JS)\n- Add JS to enforce checkout > checkin\n- Show validation message if violated",
        "issue_type": "Task",
        "priority": "High",
        "labels": ["frontend", "validation", "dates", "booking"],
        "components": ["Booking", "Frontend"]
    },
]

def main():
    print("=" * 60)
    print(f"CREATING TICKETS IN PROJECT: {PROJECT_KEY}")
    print("=" * 60)

    # Test connection first
    r = api_get("/myself")
    if r.status_code != 200:
        print(f"❌ Auth failed: {r.status_code} - {r.text}")
        sys.exit(1)
    user = r.json()
    print(f"✅ Connected as: {user.get('displayName')}")
    print(f"✅ Target project: {PROJECT_KEY}")
    print()

    # Check issue types
    issue_types = get_issue_types()
    print(f"Available issue types: {list(issue_types.keys())}")

    # Check priorities
    priorities = get_valid_priorities()
    print(f"Valid priorities: {priorities}")
    print()

    # Map issue types to available ones
    # Use 'Task' for bugs since 'Bug' not available
    for bug in BUGS:
        bug["issue_type"] = "Task"
        # Map invalid priorities
        if bug["priority"] not in priorities:
            bug["priority"] = "High" if bug["priority"] in ["Critical", "High"] else "Medium"

    for task in TASKS:
        if task["priority"] not in priorities:
            task["priority"] = "High" if task["priority"] in ["Critical", "High"] else "Medium"

    all_created = []

    # Create bugs (as Tasks)
    print("🐛 Creating BUGS (as Tasks)...")
    for bug in BUGS:
        issue = create_issue(**bug)
        if issue:
            all_created.append(issue)

    print()

    # Create tasks
    print("📋 Creating TASKS...")
    for task in TASKS:
        issue = create_issue(**task)
        if issue:
            all_created.append(issue)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total created: {len(all_created)}")
    for issue in all_created:
        key = issue.get('key', 'unknown')
        summary = issue.get('fields', {}).get('summary', issue.get('summary', 'unknown'))
        print(f"  - {key}: {summary}")
    print(f"\nView board: https://anub131091.atlassian.net/jira/software/projects/{PROJECT_KEY}/boards/1")
    print("=" * 60)

if __name__ == "__main__":
    main()