# Jira Tickets for "Enjoy with R@hul" Project

**Project Key:** SCRUM  
**Board:** https://anub131091.atlassian.net/jira/software/projects/SCRUM/boards/1

---

## Epics

| Epic Key | Summary | Description |
|----------|---------|-------------|
| SCRUM-1 | **Booking System** | Core booking functionality for dining reservations and room stays |
| SCRUM-2 | **Food Menu Display** | Display food categories and items with details |
| SCRUM-3 | **Room Management** | Room listings with pricing, images, and booking integration |
| SCRUM-4 | **UI/UX Improvements** | Navigation, responsiveness, hero sections, user experience |
| SCRUM-5 | **Technical Debt & Bugs** | Fix existing bugs, add validation, database persistence |

---

## User Stories

### Epic: Booking System (SCRUM-1)

| Story Key | Summary | Description | Acceptance Criteria | Story Points |
|-----------|---------|-------------|---------------------|--------------|
| SCRUM-101 | **Dining Reservation** | As a customer, I can book a dining reservation so that I can reserve a table | • Form accepts name, email, phone, date, guests, food preference<br>• Validation on all fields<br>• Confirmation page shows all details | 3 |
| SCRUM-102 | **Stay/Room Booking** | As a customer, I can book a room stay so that I can reserve accommodation | • Form accepts name, email, phone, check-in, check-out, guests, room type, food preference<br>• Date validation (check-out > check-in, no past dates)<br>• Confirmation page shows all details | 3 |
| SCRUM-103 | **Booking Confirmation** | As a customer, I receive confirmation details after booking so that I have a record | • Thank you page displays all submitted fields correctly for both booking types<br>• Email confirmation sent (future) | 2 |
| SCRUM-104 | **Admin Booking View** | As an admin, I can view all bookings so that I can manage reservations | • Admin dashboard lists all bookings<br>• Filter by type (dining/stay), date, status<br>• Export to CSV | 5 |

### Epic: Food Menu Display (SCRUM-2)

| Story Key | Summary | Description | Acceptance Criteria | Story Points |
|-----------|---------|-------------|---------------------|--------------|
| SCRUM-201 | **Food Categories** | As a customer, I can view food categories so that I can browse the menu | • Categories: Salads, Curries, Beverages, Desserts<br>• Clickable cards navigate to category pages | 2 |
| SCRUM-202 | **Menu Item Details** | As a customer, I can see item details so that I can make informed choices | • Each item shows name, ingredients, price<br>• Consistent layout across categories | 2 |
| SCRUM-203 | **Dynamic Menu Data** | As an admin, I can manage menu items so that I can update offerings | • CRUD for menu items in admin panel<br>• Categories managed separately | 5 |

### Epic: Room Management (SCRUM-3)

| Story Key | Summary | Description | Acceptance Criteria | Story Points |
|-----------|---------|-------------|---------------------|--------------|
| SCRUM-301 | **Room Listings** | As a customer, I can view room types with pricing so that I can choose the best option | • 4 room types: Single, Double, Double+Extra Bed, Deluxe<br>• Each shows pricing tiers (Without Food, Veg, Non-Veg)<br>• Book Now button links to booking form | 2 |
| SCRUM-302 | **Room Images** | As a customer, I can see room images so that I know what to expect | • Each room card displays relevant image<br>• Images load correctly (fixed from bug) | 1 |
| SCRUM-303 | **Room Availability** | As a customer, I can see room availability so that I don't book unavailable rooms | • Calendar integration showing booked dates<br>• Real-time availability check | 8 |

### Epic: UI/UX Improvements (SCRUM-4)

| Story Key | Summary | Description | Acceptance Criteria | Story Points |
|-----------|---------|-------------|---------------------|--------------|
| SCRUM-401 | **Responsive Navigation** | As a user, I see a responsive navigation bar so that I can navigate easily on mobile/desktop | • Hamburger menu on mobile<br>• All links work on all screen sizes | 2 |
| SCRUM-402 | **Hero Section with CTA** | As a user, I see a hero section with CTA so that I'm guided to book | • Home page hero with "Book Your Stay" button<br>• Food page hero with "Book a Table" button<br>• Rooms page hero | 2 |
| SCRUM-403 | **Footer & Social Links** | As a user, I see footer with contact/social info so that I can reach out | • Contact info displayed<br>• Social media links (FB, Instagram, Twitter) | 1 |
| SCRUM-404 | **Testimonials Section** | As a user, I see guest testimonials so that I trust the service | • Carousel or grid of testimonials<br>• Admin can add/edit testimonials | 3 |

---

## Bug Tickets

| Bug Key | Summary | Description | Steps to Reproduce | Expected Behavior | Priority | Severity |
|---------|---------|-------------|-------------------|-------------------|----------|----------|
| SCRUM-501 | **Thank you page missing dining fields** | Dining booking confirmation doesn't show date and food preference | 1. Go to /booking<br>2. Fill dining form<br>3. Submit<br>4. Observe thank you page | Thank you page shows: name, email, phone, date, guests, food preference | High | Major |
| SCRUM-502 | **Room images broken** | Room cards show broken image icons due to wrong filenames | 1. Go to /rooms<br>2. Observe room cards | All 4 room cards display correct images (bedroom-1.jpg through bedroom-4.jpg) | High | Major |
| SCRUM-503 | **No server-side form validation** | Forms accept empty/invalid data; XSS risk via unsanitized inputs | 1. Submit empty booking form<br>2. Submit with `<script>alert(1)</script>` in name field | Server rejects invalid data; all outputs escaped | Critical | Critical |
| SCRUM-504 | **No client-side date validation** | Users can select past dates; check-out before check-in | 1. Go to booking form<br>2. Select past date for check-in<br>3. Select check-out before check-in | Date pickers restrict to today+; check-out min = check-in + 1 day | High | Major |
| SCRUM-505 | **No database persistence** | Bookings only shown on confirmation page; lost on refresh | 1. Submit booking<br>2. Refresh thank you page<br>3. No record exists | Bookings stored in database; admin can view all | High | Major |
| SCRUM-506 | **No email confirmations** | Customers don't receive email receipt of booking | 1. Complete booking<br>2. Check email | Confirmation email sent to customer email | Medium | Normal |
| SCRUM-507 | **Hardcoded secret key** | Flask secret key hardcoded in app.py | 1. View app.py<br>2. See `app.secret_key = 'your-secret-key...'` | Secret key from environment variable | Medium | Normal |
| SCRUM-508 | **No CSRF protection** | Forms vulnerable to CSRF attacks | 1. Craft malicious form submission | CSRF tokens on all forms | Medium | Normal |

---

## CSV Import Format

Copy the below into a CSV file and use Jira's **Bulk Import** (Issues → Import Issues from CSV):

```csv
Summary,Description,Issue Type,Project Key,Priority,Labels,Story Points,Epic Link
"Dining Reservation","As a customer, I can book a dining reservation so that I can reserve a table",Story,SCRUM,Medium,booking,3,SCRUM-1
"Stay/Room Booking","As a customer, I can book a room stay so that I can reserve accommodation",Story,SCRUM,Medium,booking,3,SCRUM-1
"Booking Confirmation","As a customer, I receive confirmation details after booking so that I have a record",Story,SCRUM,Medium,booking,2,SCRUM-1
"Admin Booking View","As an admin, I can view all bookings so that I can manage reservations",Story,SCRUM,Low,admin,5,SCRUM-1
"Food Categories","As a customer, I can view food categories so that I can browse the menu",Story,SCRUM,Medium,food,2,SCRUM-2
"Menu Item Details","As a customer, I can see item details so that I can make informed choices",Story,SCRUM,Medium,food,2,SCRUM-2
"Dynamic Menu Data","As an admin, I can manage menu items so that I can update offerings",Story,SCRUM,Low,admin,5,SCRUM-2
"Room Listings","As a customer, I can view room types with pricing so that I can choose the best option",Story,SCRUM,Medium,rooms,2,SCRUM-3
"Room Images","As a customer, I can see room images so that I know what to expect",Story,SCRUM,High,rooms,1,SCRUM-3
"Room Availability","As a customer, I can see room availability so that I don't book unavailable rooms",Story,SCRUM,Low,rooms,8,SCRUM-3
"Responsive Navigation","As a user, I see a responsive navigation bar so that I can navigate easily on mobile/desktop",Story,SCRUM,Medium,ui,2,SCRUM-4
"Hero Section with CTA","As a user, I see a hero section with CTA so that I'm guided to book",Story,SCRUM,Medium,ui,2,SCRUM-4
"Footer & Social Links","As a user, I see footer with contact/social info so that I can reach out",Story,SCRUM,Low,ui,1,SCRUM-4
"Testimonials Section","As a user, I see guest testimonials so that I trust the service",Story,SCRUM,Low,ui,3,SCRUM-4
"Thank you page missing dining fields","Dining booking confirmation doesn't show date and food preference",Bug,SCRUM,High,bug,critical,SCRUM-5
"Room images broken","Room cards show broken image icons due to wrong filenames",Bug,SCRUM,High,bug,critical,SCRUM-5
"No server-side form validation","Forms accept empty/invalid data; XSS risk via unsanitized inputs",Bug,SCRUM,Critical,security,critical,SCRUM-5
"No client-side date validation","Users can select past dates; check-out before check-in",Bug,SCRUM,High,validation,major,SCRUM-5
"No database persistence","Bookings only shown on confirmation page; lost on refresh",Bug,SCRUM,High,backend,major,SCRUM-5
"No email confirmations","Customers don't receive email receipt of booking",Bug,SCRUM,Medium,email,normal,SCRUM-5
"Hardcoded secret key","Flask secret key hardcoded in app.py",Bug,SCRUM,Medium,security,normal,SCRUM-5
"No CSRF protection","Forms vulnerable to CSRF attacks",Bug,SCRUM,Medium,security,normal,SCRUM-5
```

---

## JSON for Jira REST API

If you have API access, use this JSON structure:

```json
{
  "fields": {
    "project": { "key": "SCRUM" },
    "summary": "Dining Reservation",
    "description": "As a customer, I can book a dining reservation so that I can reserve a table",
    "issuetype": { "name": "Story" },
    "priority": { "name": "Medium" },
    "labels": ["booking"],
    "customfield_10016": 3,
    "customfield_10014": "SCRUM-1"
  }
}
```

---

## Sprint 1 Plan (Recommended)

| Ticket | Type | Points | Notes |
|--------|------|--------|-------|
| SCRUM-501 | Bug | - | Critical - affects dining bookings |
| SCRUM-502 | Bug | - | Critical - broken images |
| SCRUM-503 | Bug | - | Critical - security |
| SCRUM-507 | Bug | - | Security - move secret to env |
| SCRUM-101 | Story | 3 | After bugs fixed |
| SCRUM-102 | Story | 3 | After bugs fixed |

**Total: ~6 story points + critical bugs**

---

## How to Import

### Option 1: CSV Import (Easiest)
1. Copy CSV section above → save as `jira-import.csv`
2. In Jira: **Issues** → **Import Issues from CSV**
3. Map fields: Summary, Description, Issue Type, Project Key, Priority, Labels, Story Points, Epic Link
4. Create Epics first, then import stories/bugs linking to Epics

### Option 2: Manual Creation
1. Go to your board: https://anub131091.atlassian.net/jira/software/projects/SCRUM/boards/1
2. Click **Create** → Select Issue Type (Story/Bug)
3. Fill in fields from tables above
4. Set Epic Link after creating Epics

### Option 3: REST API (If you have token)
```bash
curl -X POST -u email:api_token \
  -H "Content-Type: application/json" \
  -d @ticket.json \
  https://anub131091.atlassian.net/rest/api/3/issue
```

---

## Board Column Setup (Recommended)

**Kanban Columns:**
1. **Backlog** - New issues, not yet prioritized
2. **To Do** - Prioritized, ready for work
3. **In Progress** - Currently being worked on
4. **In Review** - Code review / testing
5. **Done** - Completed and deployed

**Swimlanes:** By Issue Type (Stories, Bugs, Tasks)

**Quick Filters:**
- `type = Story` (label: Stories)
- `type = Bug` (label: Bugs)
- `priority = Critical` (label: Critical)
- `component = booking` (label: Booking)
- `component = security` (label: Security)