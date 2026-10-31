# Product Requirements Document (PRD)
## Enjoy with R@hul — Hotel & Restaurant Booking Website

---

## 1. Product Overview

| Field | Detail |
|-------|--------|
| **Product Name** | Enjoy with R@hul |
| **Type** | Hotel/Restaurant booking web application |
| **Target Users** | Travelers, diners, families seeking accommodation + meals |
| **Core Value** | Unified platform for room stays + dining reservations with food menu browsing |
| **Current Stage** | MVP / Learning project (personal use, testing) |
| **Tech Stack** | Flask (Python 3), Jinja2 templates, vanilla CSS, gunicorn (prod) |

---

## 2. User Personas

| Persona | Goals | Pain Points |
|---------|-------|-------------|
| **Traveler** | Book a room quickly, see photos, know pricing incl. food options | Fragmented booking (separate calls for room + meals) |
| **Diner** | Reserve a table, browse menu, know prices | No online reservation, menu only on-site |
| **Admin (future)** | View/manage all bookings, update menu/rooms | No dashboard, data lost on refresh |

---

## 3. Functional Requirements

### 3.1 Public Pages

| Page | Route | Key Features |
|------|-------|--------------|
| **Home** | `/` | Hero, 3 feature cards, testimonials, footer with social links |
| **Rooms** | `/rooms` | 4 room cards (Single, Double, Double+Extra, Deluxe) with pricing tiers (Without Food / Veg / Non-Veg), "Book Now" → `/booking` |
| **Food Menu** | `/food` | 4 category cards → sub-pages |
| **Salads** | `/food/salads` | 5 items with name, ingredients, price |
| **Curries** | `/food/curries` | 4 items |
| **Beverages** | `/food/beverages` | 4 items |
| **Desserts** | `/food/desserts` | 4 items |
| **Booking** | `/booking` (GET/POST) | Dual forms: **Dining** (date, guests, food pref) + **Stay** (check-in/out, room type, guests, food pref) |
| **Thank You** | `/booking` → renders `thankyou.html` | Confirms all submitted fields (bug: dining fields missing) |
| **Contact** | `/contact` | Phone (clickable `tel:`), email |

### 3.2 Booking Flow

```
User → /booking → selects Dining OR Stay → fills form → POST → validation → thankyou.html
```

**Dining Fields**: name, email, phone, date, guests, food (veg/non-veg/both)
**Stay Fields**: name, email, phone, check-in, check-out, guests, room type, food

### 3.3 Validation Rules (Current)

- Email: regex format check
- Phone: required (no format enforcement)
- Guests: 1–20
- Dates: not in past; check-out > check-in (server-side only)
- Food: required dropdown
- Room type: required dropdown

---

## 4. Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| **Performance** | Pages load < 2s on 3G; static assets cached |
| **Responsive** | Mobile-first; hamburger nav < 768px; cards stack vertically |
| **Accessibility** | Semantic HTML, labels on inputs, alt text on images |
| **Security** | Input sanitization (`markupsafe.escape`), CSRF protection (planned), no hardcoded secrets |
| **Deployability** | Render Free tier compatible; `gunicorn app:app`; env-based config |

---

## 5. Current Known Issues (Backlog)

| ID | Issue | Severity | Component |
|----|-------|----------|-----------|
| B-01 | Hardcoded `secret_key` in `app.py` | Critical | Security |
| B-02 | No CSRF protection on forms | High | Security |
| B-03 | No database — bookings lost on refresh | High | Backend |
| B-04 | No email confirmations | Medium | Notifications |
| B-05 | `thankyou.html` missing dining fields (date, food) | High | Frontend |
| B-06 | Room images broken (wrong filenames in template) | High | Frontend |
| B-07 | No client-side date validation (min dates) | High | Frontend |
| B-08 | No server-side XSS protection beyond `escape()` | Critical | Security |
| T-01 | Add SQLite/SQLAlchemy persistence | Medium | Backend |
| T-02 | Add Flask-WTF + CSRF | High | Security |
| T-03 | Add Flask-Mail for confirmations | Medium | Notifications |
| T-04 | Fix room image filenames (`bedroom-1.jpg`…) | High | Frontend |
| T-05 | Add `min` attributes + JS date validation | High | Frontend |

> Full ticket list: **SCRUM-10 → SCRUM-23** in Jira (project `SCRUM`)

---

## 6. Data Model (Planned)

```python
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_type = db.Column(db.Enum('dining', 'stay'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    food_preference = db.Column(db.Enum('veg', 'non-veg', 'both'), nullable=False)
    # Dining only
    booking_date = db.Column(db.Date, nullable=True)
    # Stay only
    checkin = db.Column(db.Date, nullable=True)
    checkout = db.Column(db.Date, nullable=True)
    room_type = db.Column(db.String(30), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

---

## 7. UI/UX Specifications

| Element | Spec |
|---------|------|
| **Color Palette** | Earth tones: `#2E7D32` (green), `#F5F5F5` (bg), `#333` (text), `#FF9800` (CTA) |
| **Typography** | System font stack; headings: 2rem/1.5rem/1.25rem |
| **Spacing** | 8px base unit; cards: 16px padding, 24px gap |
| **Buttons** | Primary: green bg, white text, 8px radius; hover: darken 10% |
| **Forms** | Labels above inputs; inline validation messages (red); `tel:` link on contact phone |
| **Images** | Hero: full-width, `object-fit: cover`; Room cards: 300×200, `border-radius: 8px` |

---

## 8. Deployment Configuration

| Item | Value |
|------|-------|
| **Platform** | Render (Free Web Service) |
| **Repo** | `https://github.com/buganiser/enjoy-with-rahul.git` |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Env Vars** | `SECRET_KEY` (auto-generated), `FLASK_DEBUG=false` |
| **Auto-deploy** | On push to `main` |

---

## 9. Future Enhancements (v2+)

| Feature | Description |
|---------|-------------|
| **User Accounts** | Register/login, booking history, profile |
| **Admin Dashboard** | CRUD bookings, rooms, menu items; CSV export |
| **Availability Calendar** | Real-time room availability, prevent double-booking |
| **Payment Integration** | Razorpay/Stripe for deposits |
| **Reviews** | Guest testimonials submission + moderation |
| **Multi-language** | Hindi/English toggle |
| **PWA** | Offline menu browsing, install prompt |

---

## 10. Acceptance Criteria (MVP)

- [x] Home, Rooms, Food, Booking, Contact pages render
- [x] Booking form submits both dining & stay types
- [x] Validation rejects invalid input (server-side)
- [x] Thank you page shows submitted data (fix dining fields)
- [x] Contact phone clickable on mobile
- [x] Deployed on Render with public URL
- [ ] Database persists bookings
- [ ] Email confirmations sent
- [ ] CSRF protection active
- [ ] No hardcoded secrets

---

## 11. Open Questions / Decisions Needed

1. **Room pricing** — Current template shows 3 tiers per room. Confirm final prices?
2. **Food preference options** — Keep `veg` / `non-veg` / `both` or add more (vegan, jain, etc.)?
3. **Image assets** — Use existing `bedroom-1..4.jpg` + food images, or source new ones?
4. **Contact email** — Replace `enjoywithrahul@example.com` with real address?
5. **Analytics** — Add Google Analytics / Plausible for visitor tracking?

---

*Document version: 1.0*  
*Created: 2025-01-15*  
*Author: Auto-generated from codebase analysis*