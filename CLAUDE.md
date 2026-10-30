# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Enjoy with R@hul** - A Flask-based hotel/restaurant booking website with room reservations, dining bookings, and food menu display.

## Development Commands

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run the Flask app (development)
python app.py

# Run on specific port
python app.py --port 5000
```

The app runs on `http://localhost:5000` by default with debug mode enabled.

## Architecture

### Backend (`app.py`)
- Single-file Flask application with 8 routes
- Handles two booking types via POST to `/booking`:
  - **Dining**: name, email, phone, date, guests, food preference
  - **Stay**: name, email, checkin, checkout, guests, room type, food preference
- Food sub-pages serve static menu data (salads, curries, beverages, desserts)
- No database - all data is in-memory/templates

### Frontend (Templates)
- **base.html** - Shared layout with navigation bar
- **home.html** - Hero, features, testimonials, footer
- **rooms.html** - 4 room cards with pricing tiers
- **food.html** - Category cards linking to sub-pages
- **salads.html**, **curries.html**, **beverages.html**, **desserts.html** - Menu item lists
- **booking.html** - Two forms (dining + stay) posting to same endpoint
- **thankyou.html** - Confirmation page (currently only displays stay fields)
- **contact.html** - Simple contact info

### Styling (`static/css/style.css`)
- Single CSS file with all styles
- Hero sections for home/food/rooms
- Card-based layouts with hover effects
- Form styling with date-row for checkin/checkout side-by-side
- Thank you box with success styling

## Key Files to Know

| File | Purpose |
|------|---------|
| `app.py` | All routes and business logic |
| `templates/base.html` | Base layout + navigation |
| `templates/booking.html` | Dual booking forms |
| `templates/thankyou.html` | Confirmation (bug: missing dining fields) |
| `static/css/style.css` | All styling |

## Known Issues

1. **thankyou.html only handles stay bookings** - dining bookings pass different fields (date, food) but template expects checkin, checkout, room
2. **Room images referenced but may not exist** - `single-room.jpg`, `double-room.jpg`, etc. in templates but actual images have different names
3. **No validation/sanitization** on form inputs
4. **No persistence** - bookings only shown on confirmation page

## Adding Features

- **Database**: Add SQLAlchemy or similar to `app.py`
- **Email confirmations**: Integrate Flask-Mail in booking POST handler
- **Admin panel**: Add protected routes for viewing bookings
- **Image management**: Standardize image naming in `static/images/`