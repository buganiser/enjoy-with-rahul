#!/usr/bin/env python3
"""
Comprehensive Jira Project & Issue Creation Script
Creates "Enjoy with R@hul" (EWR) Scrum project and populates with QA tasks, test scenarios, and bugs
"""

import os
import sys
import json
import requests
from requests.auth import HTTPBasicAuth

# Configuration from environment variables
JIRA_EMAIL = os.environ.get("JIRA_EMAIL")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")
JIRA_BASE_URL = "https://anub131091.atlassian.net"

if not JIRA_EMAIL or not JIRA_API_TOKEN:
    print("❌ Error: JIRA_EMAIL and JIRA_API_TOKEN environment variables must be set")
    sys.exit(1)

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
headers = {"Accept": "application/json", "Content-Type": "application/json"}

# Project configuration
PROJECT_KEY = "EWR"
PROJECT_NAME = "Enjoy with R@hul"
PROJECT_TEMPLATE = "com.pyxis.greenhopper.jira:gh-scrum-template"

def api_get(endpoint, params=None):
    """GET request to Jira API"""
    url = f"{JIRA_BASE_URL}{endpoint}"
    response = requests.get(url, headers=headers, auth=auth, params=params)
    return response

def api_post(endpoint, payload):
    """POST request to Jira API"""
    url = f"{JIRA_BASE_URL}{endpoint}"
    response = requests.post(url, headers=headers, auth=auth, json=payload)
    return response

def check_connection():
    """Step 1: Check Jira API connection and permissions"""
    print("🔍 Step 1: Checking Jira API connection and permissions...")
    response = api_get("/rest/api/3/myself")
    if response.status_code == 200:
        user = response.json()
        print(f"   ✅ Connected as: {user.get('displayName', user.get('emailAddress', 'Unknown'))}")
        print(f"   ✅ Account ID: {user.get('accountId')}")
        return True
    else:
        print(f"   ❌ Connection failed: {response.status_code} - {response.text}")
        return False

def check_permissions():
    """Check if user has admin/project creation permissions"""
    print("\n🔍 Checking permissions...")
    response = api_get("/rest/api/3/mypermissions", params={"permissions": "CREATE_PROJECTS,ADMINISTER_PROJECTS"})
    if response.status_code == 200:
        perms = response.json().get("permissions", {})
        can_create = perms.get("CREATE_PROJECTS", {}).get("havePermission", False)
        can_admin = perms.get("ADMINISTER_PROJECTS", {}).get("havePermission", False)
        print(f"   CREATE_PROJECTS permission: {'✅ Yes' if can_create else '❌ No'}")
        print(f"   ADMINISTER_PROJECTS permission: {'✅ Yes' if can_admin else '❌ No'}")
        return can_create
    else:
        print(f"   ⚠️ Could not check permissions: {response.status_code}")
        return False

def find_existing_project():
    """Step 2: Check if project already exists"""
    print(f"\n🔍 Step 2: Searching for existing project '{PROJECT_NAME}' (key: {PROJECT_KEY})...")
    response = api_get("/rest/api/3/project/search", params={"query": PROJECT_NAME, "maxResults": 50})
    if response.status_code == 200:
        data = response.json()
        for project in data.get("values", []):
            if project.get("key") == PROJECT_KEY or project.get("name") == PROJECT_NAME:
                print(f"   ✅ Found existing project: {project['key']} - {project['name']}")
                return project
        print(f"   ℹ️ No existing project found with key '{PROJECT_KEY}' or name '{PROJECT_NAME}'")
        return None
    else:
        print(f"   ❌ Search failed: {response.status_code} - {response.text}")
        return None

def create_project():
    """Step 3: Create the Scrum project via API"""
    print(f"\n🔨 Step 3: Creating Scrum project '{PROJECT_NAME}' (key: {PROJECT_KEY})...")

    # Jira Cloud project creation payload
    payload = {
        "key": PROJECT_KEY,
        "name": PROJECT_NAME,
        "projectTypeKey": "software",
        "projectTemplateKey": PROJECT_TEMPLATE,
        "description": "Jira project for 'Enjoy with R@hul' - Hotel/Restaurant booking website QA and development tracking",
        "leadAccountId": None,  # Will use current user
        "assigneeType": "PROJECT_LEAD",
        "url": "https://github.com/your-repo/enjoy-with-rahul",
        "avatarId": 10400  # Software project avatar
    }

    response = api_post("/rest/api/3/project", payload)

    if response.status_code == 201:
        project = response.json()
        print(f"   ✅ Project created successfully!")
        print(f"      Key: {project.get('key')}")
        print(f"      ID: {project.get('id')}")
        print(f"      Self: {project.get('self')}")
        return project
    elif response.status_code == 400:
        error = response.json()
        if "errors" in error and "key" in error["errors"]:
            if "already exists" in error["errors"]["key"].lower():
                print(f"   ℹ️ Project key '{PROJECT_KEY}' already exists, searching...")
                return find_existing_project()
        print(f"   ❌ Project creation failed (400): {json.dumps(error, indent=2)}")
        return None
    elif response.status_code == 403:
        print(f"   ❌ Permission denied (403): You may not have permission to create projects")
        print(f"      Response: {response.text}")
        return None
    else:
        print(f"   ❌ Project creation failed: {response.status_code} - {response.text}")
        return None

def verify_project(project_key):
    """Step 4: Verify project was created and get details"""
    print(f"\n✅ Step 4: Verifying project '{project_key}'...")
    response = api_get(f"/rest/api/3/project/{project_key}")
    if response.status_code == 200:
        project = response.json()
        print(f"   ✅ Project verified:")
        print(f"      Key: {project.get('key')}")
        print(f"      Name: {project.get('name')}")
        print(f"      Type: {project.get('projectTypeKey')}")
        print(f"      URL: {JIRA_BASE_URL}/browse/{project_key}")
        return project
    else:
        print(f"   ❌ Verification failed: {response.status_code} - {response.text}")
        return None

def get_issue_types(project_key):
    """Get available issue types for the project"""
    print(f"\n🔍 Getting issue types for project '{project_key}'...")
    response = api_get(f"/rest/api/3/issuetype/project", params={"projectKey": project_key})
    if response.status_code == 200:
        issue_types = response.json()
        type_map = {}
        for it in issue_types:
            type_map[it["name"].lower()] = it["id"]
            print(f"   - {it['name']}: {it['id']}")
        return type_map
    else:
        print(f"   ❌ Failed to get issue types: {response.status_code} - {response.text}")
        return {}

def create_issue(project_key, summary, description, issue_type_name, issue_type_map, priority="Medium", labels=None, components=None):
    """Create a single issue"""
    issue_type_id = issue_type_map.get(issue_type_name.lower())
    if not issue_type_id:
        # Try to find by partial match
        for name, id in issue_type_map.items():
            if issue_type_name.lower() in name or name in issue_type_name.lower():
                issue_type_id = id
                break

    if not issue_type_id:
        print(f"   ❌ Issue type '{issue_type_name}' not found in project")
        return None

    fields = {
        "project": {"key": project_key},
        "summary": summary,
        "description": {
            "type": "doc",
            "version": 1,
            "content": [{
                "type": "paragraph",
                "content": [{"type": "text", "text": description}]
            }]
        },
        "issuetype": {"id": issue_type_id},
        "priority": {"name": priority},
    }

    if labels:
        fields["labels"] = labels
    if components:
        fields["components"] = [{"name": c} for c in components]

    response = api_post("/rest/api/3/issue", {"fields": fields})

    if response.status_code == 201:
        issue = response.json()
        print(f"   ✅ Created {issue_type_name}: {issue['key']} - {summary}")
        return issue
    elif response.status_code == 400:
        error = response.json()
        if "errors" in error and "summary" in error["errors"]:
            if "already exists" in error["errors"]["summary"].lower():
                print(f"   ⏭️ Skipping duplicate: {summary}")
                return None
        print(f"   ❌ Failed to create '{summary}': {json.dumps(error, indent=2)}")
        return None
    else:
        print(f"   ❌ Failed to create '{summary}': {response.status_code} - {response.text}")
        return None

def create_issues(project_key, issue_type_map):
    """Step 5: Create QA tasks, login test scenarios, and bug tickets"""
    print(f"\n📝 Step 5: Creating issues in project '{project_key}'...")

    all_issues = []

    # ============================================================
    # QA TASKS
    # ============================================================
    qa_tasks = [
        ("QA Task: Test Dining Reservation Flow",
         "Test the complete dining reservation flow:\n1. Navigate to /booking\n2. Fill dining form (name, email, phone, date, guests, food preference)\n3. Submit form\n4. Verify thank you page shows all fields correctly\n5. Verify data validation works",
         "Task", "Medium", ["qa", "booking", "dining"], ["Booking"]),

        ("QA Task: Test Stay/Room Booking Flow",
         "Test the complete stay booking flow:\n1. Navigate to /booking\n2. Fill stay form (name, email, phone, check-in, check-out, guests, room type, food preference)\n3. Submit form\n4. Verify thank you page shows all fields correctly\n5. Verify date validation (check-out > check-in, no past dates)",
         "Task", "Medium", ["qa", "booking", "stay"], ["Booking"]),

        ("QA Task: Test Food Menu Navigation",
         "Test food menu navigation and display:\n1. Navigate to /food\n2. Click each category card (Salads, Curries, Beverages, Desserts)\n3. Verify each category page loads correctly\n4. Verify item details (name, ingredients, price) display properly",
         "Task", "Medium", ["qa", "food", "menu"], ["Food Menu"]),

        ("QA Task: Test Room Listings Display",
         "Test room listings page:\n1. Navigate to /rooms\n2. Verify all 4 room types display (Single, Double, Double+Extra Bed, Deluxe)\n3. Verify pricing tiers show (Without Food, Veg, Non-Veg)\n4. Verify room images load correctly\n5. Verify 'Book Now' buttons link to booking form",
         "Task", "Medium", ["qa", "rooms", "images"], ["Rooms"]),

        ("QA Task: Test Responsive Design",
         "Test responsive design across devices:\n1. Test navigation bar on mobile (hamburger menu)\n2. Test hero sections on mobile/desktop\n3. Test form usability on mobile\n4. Test card layouts wrap correctly",
         "Task", "Medium", ["qa", "ui", "responsive"], ["UI/UX"]),

        ("QA Task: Cross-Browser Testing",
         "Test on multiple browsers:\n1. Chrome (latest)\n2. Firefox (latest)\n3. Safari (latest)\n4. Edge (latest)\nVerify all functionality works consistently",
         "Task", "Low", ["qa", "browser", "compatibility"], ["UI/UX"]),
    ]

    # ============================================================
    # LOGIN TEST SCENARIOS (if auth is added later)
    # ============================================================
    login_tests = [
        ("Test Scenario: User Registration",
         "Test user registration flow:\n1. Navigate to registration page\n2. Fill valid registration data\n3. Submit form\n4. Verify email verification sent\n5. Verify account activation\n5. Test duplicate email handling\n6. Test password strength validation",
         "Test", "Medium", ["test", "auth", "registration"], ["Authentication"]),

        ("Test Scenario: User Login",
         "Test user login flow:\n1. Navigate to login page\n2. Test valid credentials\n3. Test invalid credentials\n4. Test 'Remember me' functionality\n5. Test password reset flow\n6. Test session persistence",
         "Test", "Medium", ["test", "auth", "login"], ["Authentication"]),

        ("Test Scenario: Admin Login & Dashboard",
         "Test admin access:\n1. Login with admin credentials\n2. Verify admin dashboard loads\n3. Verify booking management visible\n4. Verify user management visible\n5. Test role-based access control",
         "Test", "Medium", ["test", "auth", "admin"], ["Authentication"]),

        ("Test Scenario: Session Management",
         "Test session handling:\n1. Login and verify session cookie\n2. Test session timeout\n3. Test concurrent session limit\n4. Test logout clears session\n5. Test CSRF token validation",
         "Test", "Low", ["test", "auth", "session"], ["Authentication"]),
    ]

    # ============================================================
    # BUG TICKETS
    # ============================================================
    bugs = [
        ("Bug: Thank you page missing dining booking fields",
         "Dining booking confirmation doesn't show date and food preference fields.\n\nSteps to Reproduce:\n1. Go to /booking\n2. Fill dining form (name, email, phone, date, guests, food)\n3. Submit\n4. Observe thank you page\n\nExpected: Page shows name, email, phone, date, guests, food preference\nActual: Only shows name, email, phone, guests (missing date, food)",
         "Bug", "High", ["bug", "booking", "dining", "frontend"], ["Booking"]),

        ("Bug: Room images broken - wrong filenames",
         "Room cards show broken image icons due to incorrect image filenames in template.\n\nSteps to Reproduce:\n1. Go to /rooms\n2. Observe room cards\n\nExpected: All 4 room cards display correct images\nActual: Images reference single-room.jpg, double-room.jpg, etc. but actual files are bedroom-1.jpg through bedroom-4.jpg",
         "Bug", "High", ["bug", "rooms", "images", "frontend"], ["Rooms"]),

        ("Bug: No server-side form validation - XSS risk",
         "Forms accept empty/invalid data and have XSS vulnerability via unsanitized inputs.\n\nSteps to Reproduce:\n1. Submit empty booking form\n2. Submit with <script>alert(1)</script> in name field\n3. Observe data accepted\n\nExpected: Server rejects invalid data; all outputs escaped\nActual: No validation; raw input rendered in thank you page",
         "Bug", "Critical", ["bug", "security", "validation", "xss", "backend"], ["Booking", "Security"]),

        ("Bug: No client-side date validation",
         "Users can select past dates for check-in; check-out before check-in allowed.\n\nSteps to Reproduce:\n1. Go to booking form\n2. Select past date for check-in\n3. Select check-out before check-in\n\nExpected: Date pickers restrict to today+; check-out min = check-in + 1 day\nActual: No date restrictions enforced",
         "Bug", "High", ["bug", "validation", "dates", "frontend"], ["Booking"]),

        ("Bug: No database persistence for bookings",
         "Bookings only shown on confirmation page; lost on refresh - no storage.\n\nSteps to Reproduce:\n1. Submit booking\n2. Refresh thank you page\n3. No record exists\n\nExpected: Bookings stored in database; admin can view all\nActual: No database; data only in memory during request",
         "Bug", "High", ["bug", "backend", "database", "persistence"], ["Booking", "Backend"]),

        ("Bug: No email confirmations sent",
         "Customers don't receive email receipt of booking.\n\nSteps to Reproduce:\n1. Complete booking\n2. Check email\n\nExpected: Confirmation email sent to customer email\nActual: No email functionality implemented",
         "Bug", "Medium", ["bug", "email", "notifications"], ["Booking", "Notifications"]),

        ("Bug: Hardcoded secret key in app.py",
         "Flask secret key hardcoded in source code.\n\nSteps to Reproduce:\n1. View app.py\n2. See: app.secret_key = 'your-secret-key-change-in-production'\n\nExpected: Secret key from environment variable\nActual: Hardcoded placeholder in source",
         "Bug", "Medium", ["bug", "security", "config", "backend"], ["Security", "Backend"]),

        ("Bug: No CSRF protection on forms",
         "Forms vulnerable to CSRF attacks - no CSRF tokens.\n\nSteps to Reproduce:\n1. Craft malicious form submission\n2. Submit to booking endpoint\n\nExpected: CSRF tokens on all forms\nActual: No CSRF protection implemented",
         "Bug", "Medium", ["bug", "security", "csrf", "backend"], ["Security", "Backend"]),
    ]

    # Create all issues
    for summary, desc, issue_type, priority, labels, components in qa_tasks + login_tests + bugs:
        issue = create_issue(project_key, summary, desc, issue_type, issue_type_map, priority, labels, components)
        if issue:
            all_issues.append(issue)

    return all_issues

def main():
    print("=" * 60)
    print("JIRA PROJECT & ISSUE CREATION")
    print("=" * 60)
    print(f"Target: {JIRA_BASE_URL}")
    print(f"Project: {PROJECT_NAME} ({PROJECT_KEY})")
    print(f"Template: Scrum")
    print("=" * 60)

    # Step 1: Check connection
    if not check_connection():
        print("\n❌ Cannot proceed - connection failed")
        sys.exit(1)

    # Check permissions
    can_create_project = check_permissions()

    # Step 2: Check existing project
    existing_project = find_existing_project()

    project = existing_project

    # Step 3: Create project if needed
    if not project:
        if not can_create_project:
            print("\n⚠️ You don't have CREATE_PROJECTS permission.")
            print("   Please create the project manually in Jira UI:")
            print("   1. Go to https://anub131091.atlassian.net")
            print("   2. Projects → Create project")
            print("   3. Choose 'Scrum' template")
            print(f"   4. Name: '{PROJECT_NAME}', Key: '{PROJECT_KEY}'")
            print("   Then re-run this script.")
            sys.exit(1)

        project = create_project()
        if not project:
            print("\n❌ Project creation failed. Cannot proceed.")
            sys.exit(1)
    else:
        print(f"\n✅ Using existing project: {project['key']} - {project['name']}")

    project_key = project.get("key", PROJECT_KEY)

    # Step 4: Verify project
    project = verify_project(project_key)
    if not project:
        print("\n❌ Project verification failed")
        sys.exit(1)

    # Get issue types
    issue_type_map = get_issue_types(project_key)
    if not issue_type_map:
        print("\n❌ Could not get issue types. Cannot create issues.")
        sys.exit(1)

    # Step 5: Create issues
    all_issues = create_issues(project_key, issue_type_map)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Project: {project_key} - {PROJECT_NAME}")
    print(f"Project URL: {JIRA_BASE_URL}/browse/{project_key}")
    print(f"Board URL: {JIRA_BASE_URL}/jira/software/projects/{project_key}/boards/1")
    print(f"Issues created: {len(all_issues)}")
    print("=" * 60)

    if all_issues:
        print("\nCreated Issues:")
        for issue in all_issues:
            print(f"  - {issue['key']}: {issue['fields']['summary']}")

if __name__ == "__main__":
    main()