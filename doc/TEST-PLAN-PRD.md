# Test Plan — Enjoy with R@hul (PRD-Based)

**Document Version:** 1.0  
**Date:** 2026-10-30  
**Author:** Generated from PRD.md  
**Status:** Draft

---

## 1. Objective

Validate the **Enjoy with R@hul** hotel/restaurant booking website against the Product Requirements Document (PRD v1.0). Ensure all MVP acceptance criteria are met, known bugs are fixed, and the application is ready for Render deployment.

**Primary Goals:**
- Verify all public pages render correctly (Home, Rooms, Food, Booking, Contact, Thank You)
- Confirm dual booking flows (Dining + Stay) submit and display correctly
- Validate server-side and client-side validation rules
- Confirm security fixes: no hardcoded secrets, CSRF protection, XSS prevention
- Verify deployment configuration works on Render Free tier

---

## 2. Scope

### In Scope (MVP per PRD §10)
| Area | PRD Reference |
|------|---------------|
| Public page rendering (Home, Rooms, Food, sub-pages, Booking, Contact, Thank You) | §3.1, §10 |
| Dining reservation form (name, email, phone, date, guests, food preference) | §3.2, §3.3 |
| Stay/room booking form (name, email, phone, check-in, check-out, guests, room type, food preference) | §3.2, §3.3 |
| Server-side validation (email regex, phone required, guests 1–20, dates not past, check-out > check-in, food required, room type required) | §3.3 |
| Thank you page displays all submitted fields for both booking types | §3.1, §10 (B-05) |
| Contact page with clickable `tel:` phone link | §3.1, §10 |
| Render deployment with gunicorn, env-based config | §8, §10 |
| Responsive design (mobile-first, hamburger nav < 768px) | §4, §7 |
| Security: input sanitization (`markupsafe.escape`), no hardcoded secrets | §4, §5 (B-01, B-08) |
| Room image fixes (correct filenames: `bedroom-1.jpg`…`bedroom-4.jpg`) | §5 (B-06, T-04) |
| Client-side date validation (min dates, check-out ≥ check-in + 1) | §5 (B-07, T-05) |

### Out of Scope (Post-MVP / v2+ per PRD §9)
- User accounts, login, booking history
- Admin dashboard (CRUD bookings, rooms, menu, CSV export)
- Real-time availability calendar / double-booking prevention
- Payment integration (Razorpay/Stripe)
- Reviews/testimonials submission & moderation
- Multi-language (Hindi/English)
- PWA features (offline, install prompt)
- Database persistence (T-01) — tracked but not blocking MVP deploy
- Email confirmations (T-03) — tracked but not blocking MVP deploy

---

## 3. Inclusions (Test Coverage)

### 3.1 Functional Test Cases

| ID | Feature | Test Scenario | Expected Result |
|----|---------|---------------|-----------------|
| TC-01 | Home Page | Load `/` | Hero, 3 feature cards, testimonials, footer with social links render |
| TC-02 | Rooms Page | Load `/rooms` | 4 room cards (Single, Double, Double+Extra, Deluxe) with 3 pricing tiers each; "Book Now" links to `/booking` |
| TC-03 | Room Images | Inspect room card images | All 4 cards display `bedroom-1.jpg` through `bedroom-4.jpg` (no broken images) |
| TC-04 | Food Menu Index | Load `/food` | 4 category cards (Salads, Curries, Beverages, Desserts) link to sub-pages |
| TC-05 | Salads Page | Load `/food/salads` | 5 items with name, ingredients, price |
| TC-06 | Curries Page | Load `/food/curries` | 4 items with name, ingredients, price |
| TC-07 | Beverages Page | Load `/food/beverages` | 4 items with name, ingredients, price |
| TC-08 | Desserts Page | Load `/food/desserts` | 4 items with name, ingredients, price |
| TC-09 | Contact Page | Load `/contact` | Phone number as clickable `tel:` link; email displayed |
| TC-10 | Booking Page - Dining Form | Load `/booking`, fill dining form, submit valid data | Redirects to `thankyou.html` showing: name, email, phone, date, guests, food preference |
| TC-11 | Booking Page - Stay Form | Load `/booking`, fill stay form, submit valid data | Redirects to `thankyou.html` showing: name, email, phone, check-in, check-out, guests, room type, food preference |
| TC-12 | Dining Validation - Email | Submit dining form with invalid email | Server rejects with validation error |
| TC-13 | Dining Validation - Phone | Submit dining form with empty phone | Server rejects with validation error |
| TC-14 | Dining Validation - Guests | Submit dining form with guests=0 or >20 | Server rejects with validation error |
| TC-15 | Dining Validation - Past Date | Submit dining form with date in past | Server rejects with validation error |
| TC-16 | Dining Validation - Food Required | Submit dining form without food preference | Server rejects with validation error |
| TC-17 | Stay Validation - Check-in Past | Submit stay form with check-in in past | Server rejects with validation error |
| TC-18 | Stay Validation - Check-out ≤ Check-in | Submit stay form with check-out ≤ check-in | Server rejects with validation error |
| TC-19 | Stay Validation - Room Type Required | Submit stay form without room type | Server rejects with validation error |
| TC-20 | Stay Validation - Food Required | Submit stay form without food preference | Server rejects with validation error |
| TC-21 | XSS Protection | Submit `<script>alert(1)</script>` in name field | Output escaped on thank you page; no script execution |
| TC-22 | CSRF Protection | Submit form without CSRF token (if implemented) | Request rejected |
| TC-23 | Client-side Date Validation - Dining | Open dining form, try select past date | Date picker restricts to today or future |
| TC-24 | Client-side Date Validation - Stay | Open stay form, try select past check-in | Date picker restricts to today or future |
| TC-25 | Client-side Date Validation - Stay | Select check-in, try select check-out ≤ check-in | Check-out picker min = check-in + 1 day |
| TC-26 | Responsive - Mobile Nav | View Home page at < 768px width | Hamburger menu appears; all nav links accessible |
| TC-27 | Responsive - Card Stacking | View Rooms/Food pages at < 768px | Cards stack vertically |
| TC-28 | Responsive - Form Layout | View Booking page at < 768px | Forms stack; date fields stack (not side-by-side) |

### 3.2 Non-Functional Test Cases

| ID | Category | Test Scenario | Expected Result |
|----|----------|---------------|-----------------|
| NF-01 | Performance | Load each page on simulated 3G | Page load < 2s |
| NF-02 | Caching | Reload page, check headers | Static assets have cache headers |
| NF-03 | Accessibility | Run axe-core / Lighthouse | No critical a11y violations; semantic HTML, labels, alt text present |
| NF-04 | Security - Secrets | Inspect `app.py` and env | No hardcoded `secret_key`; reads from `SECRET_KEY` env var |
| NF-05 | Security - Debug | Deploy to Render, check `FLASK_DEBUG` | `FLASK_DEBUG=false` in production |
| NF-06 | Deployment | Push to `main`, verify Render build | Build passes; `gunicorn app:app` starts; public URL accessible |

---

## 4. Test Environments

| Environment | URL / Access | Purpose |
|-------------|--------------|---------|
| **Local Dev** | `http://localhost:5000` (Flask debug) | Developer testing, rapid iteration |
| **Local Prod Sim** | `http://localhost:8000` (gunicorn) | Validate production server behavior |
| **Render Staging** | `https://<app>.onrender.com` (auto-deploy from `main`) | Pre-production validation |
| **Render Production** | `https://<app>.onrender.com` (after manual promote) | Final sign-off |

**Test Data:**
- Valid dining booking: Name "Test User", Email "test@example.com", Phone "9876543210", Date tomorrow, Guests 2, Food "veg"
- Valid stay booking: Name "Test User", Email "test@example.com", Phone "9876543210", Check-in tomorrow, Check-out day after, Guests 2, Room "Double", Food "non-veg"
- Invalid data sets per validation rules in §3.3

---

## 5. Defect Reporting

**Tool:** Jira (Project: `SCRUM`)  
**Labels:** `test-failure`, `mvp-blocker`, `security`, `ui`, `validation`, `deployment`  
**Priority Mapping:**
| Severity | Jira Priority | SLA |
|----------|---------------|-----|
| Critical (security, data loss, deploy block) | Critical | Fix before deploy |
| High (functional break, missing MVP AC) | High | Fix in current sprint |
| Medium (cosmetic, non-blocking) | Medium | Next sprint |
| Low (enhancement, tech debt) | Low | Backlog |

**Defect Template:**
```
Summary: [Component] Brief description
Description: Steps to reproduce, expected vs actual, environment
Labels: [component], [severity], test-failure
Attachments: Screenshot, HAR file, logs
```

---

## 6. Test Strategy

### 6.1 Test Types & Approach

| Test Type | Approach | Coverage Target |
|-----------|----------|-----------------|
| **Smoke** | Run on every deploy (local + Render) | 100% critical paths (TC-01, TC-10, TC-11, TC-28) |
| **Functional** | Manual + automated (pytest + Playwright) | All TC-01 to TC-28 |
| **Validation** | Boundary value + negative testing | All validation rules (§3.3) |
| **Security** | Static analysis (bandit), manual XSS/CSRF probes | NF-04, TC-21, TC-22 |
| **Responsive** | Chrome DevTools device toolbar + real mobile | TC-26, TC-27, TC-28 |
| **Performance** | Lighthouse CI in pipeline | NF-01, NF-02 |
| **Accessibility** | axe-core in CI + manual keyboard nav | NF-03 |
| **Deployment** | Render preview deploy on PR + main branch | NF-06 |

### 6.2 Automation Stack
- **Unit/Integration:** `pytest` + `Flask.test_client` (validation logic, route responses)
- **E2E:** `Playwright` (full booking flows, responsive checks)
- **Static Analysis:** `bandit` (security), `flake8` (lint)
- **CI:** GitHub Actions (run on PR + push to main)

### 6.3 Test Data Management
- No database in MVP → test data ephemeral (in-memory only)
- Each test run uses fresh Flask app instance
- Playwright tests clean up via browser context isolation

---

## 7. Test Schedule

| Phase | Timeline | Activities | Exit Criteria |
|-------|----------|------------|---------------|
| **Sprint 1 (Week 1-2)** | Days 1-14 | - Fix critical bugs (B-01, B-02, B-03, B-05, B-06, B-07, B-08)<br>- Implement CSRF (T-02)<br>- Fix room images (T-04)<br>- Add client-side date validation (T-05)<br>- Write unit/E2E tests | All B-01..B-08 resolved; TC-01..TC-28 pass locally |
| **Sprint 2 (Week 3)** | Days 15-21 | - Render deployment validation (NF-06)<br>- Performance & accessibility audit (NF-01..NF-03)<br>- Security review (NF-04, NF-05)<br>- Regression testing | Zero Critical/High defects; all MVP AC (§10) ✅ |
| **Release** | Day 22 | - Production deploy<br>- Post-deploy smoke test | Public URL live; smoke passes |

---

## 8. Tools

| Category | Tool | Version / Config |
|----------|------|------------------|
| **Test Management** | Jira (Zephyr/Excel export) | Project `SCRUM` |
| **API Testing** | Postman / `requests` | Collection: `enjoy-with-rahul.postman_collection.json` |
| **E2E Automation** | Playwright (Python) | `playwright==1.40+`, Chromium/Firefox/WebKit |
| **Unit Testing** | pytest + Flask test client | `pytest==7.4+`, `pytest-cov` |
| **Static Analysis** | bandit, flake8 | `bandit==1.7+`, `flake8==6.0+` |
| **Performance** | Lighthouse CI | `@lhci/cli` in GitHub Actions |
| **Accessibility** | axe-core / Lighthouse | Integrated in Playwright + CI |
| **Deployment** | Render (Free Web Service) | Auto-deploy on `main` push |
| **Version Control** | Git + GitHub | Branch: `main`, PR-based workflow |

---

## 9. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Hardcoded secret deployed** | High | Critical | Pre-commit hook + CI check for `secret_key` in code; Render env var mandatory |
| **CSRF vulnerability** | High | Critical | Implement Flask-WTF + CSRF before deploy; test TC-22 |
| **XSS via unsanitized output** | Medium | Critical | Enforce `markupsafe.escape` on all template vars; bandit scan in CI |
| **Render Free tier limits (spin-down, no DB)** | High | Medium | Accept cold-start latency; plan SQLite persistence (T-01) post-MVP |
| **Mobile layout regressions** | Medium | High | Visual regression tests (Playwright screenshots) in CI |
| **Date validation bypass (JS disabled)** | Medium | High | Server-side validation is source of truth; client-side is UX only |
| **Image 404s on Render** | Medium | Medium | Verify `static/images/` committed; test NF-06 includes image loads |
| **Missing email confirmations** | Low (deferred) | Medium | Documented as known gap (B-04, T-03); not blocking MVP |

---

## 10. Approvals

| Role | Name | Sign-off | Date |
|------|------|----------|------|
| **Product Owner** | — | ☐ | — |
| **Lead Developer** | — | ☐ | — |
| **QA Lead** | — | ☐ | — |
| **DevOps / Deploy** | — | ☐ | — |

> **Note:** This test plan covers MVP scope only. Post-MVP features (database, email, admin dashboard) require separate test plans.

---

## Appendix A: Traceability Matrix (PRD §10 AC → Test Cases)

| Acceptance Criterion (PRD §10) | Test Case(s) |
|--------------------------------|--------------|
| Home, Rooms, Food, Booking, Contact pages render | TC-01, TC-02, TC-04, TC-09, TC-10 |
| Booking form submits both dining & stay types | TC-10, TC-11 |
| Validation rejects invalid input (server-side) | TC-12 through TC-20 |
| Thank you page shows submitted data (fix dining fields) | TC-10, TC-11 |
| Contact phone clickable on mobile | TC-09 |
| Deployed on Render with public URL | NF-06 |
| Database persists bookings | Out of scope (T-01) |
| Email confirmations sent | Out of scope (T-03) |
| CSRF protection active | TC-22, NF-04 |
| No hardcoded secrets | NF-04 |

---

## Appendix B: Test Data Sets

### Valid Dining Booking
```json
{
  "booking_type": "dining",
  "name": "Rahul Sharma",
  "email": "rahul@example.com",
  "phone": "9161728664",
  "date": "2026-11-01",
  "guests": "4",
  "food": "veg"
}
```

### Valid Stay Booking
```json
{
  "booking_type": "stay",
  "name": "Priya Patel",
  "email": "priya@example.com",
  "phone": "9876543210",
  "checkin": "2026-11-05",
  "checkout": "2026-11-07",
  "guests": "2",
  "room_type": "Deluxe",
  "food": "both"
}
```

### Invalid Data Samples
| Field | Invalid Value | Expected Error |
|-------|---------------|----------------|
| email | "not-an-email" | "Invalid email format" |
| phone | "" | "Phone is required" |
| guests | "0" | "Guests must be 1-20" |
| guests | "25" | "Guests must be 1-20" |
| date (dining) | "2026-01-01" (past) | "Date cannot be in the past" |
| checkin (stay) | "2026-01-01" (past) | "Check-in cannot be in the past" |
| checkout (stay) | same as checkin | "Check-out must be after check-in" |
| food | "" | "Food preference is required" |
| room_type | "" | "Room type is required" |

---

*End of Test Plan*