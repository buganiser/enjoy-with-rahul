from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime
from markupsafe import escape
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-change-in-prod')

def validate_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_date(date_str, field_name):
    """Validate date format and return datetime object"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError(f"Invalid {field_name} format. Use YYYY-MM-DD.")

def validate_guests(guests_str):
    """Validate guest count"""
    try:
        guests = int(guests_str)
        if guests < 1:
            raise ValueError("Number of guests must be at least 1.")
        if guests > 20:
            raise ValueError("Number of guests cannot exceed 20.")
        return guests
    except ValueError as e:
        if "guests" in str(e).lower():
            raise
        raise ValueError("Invalid number of guests.")

def sanitize_input(value):
    """Sanitize input to prevent XSS"""
    return escape(value.strip()) if value else ''

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Rooms page
@app.route('/rooms')
def rooms():
    return render_template('rooms.html')

# Food page
@app.route('/food')
def food():
    return render_template('food.html')

# Booking page (GET & POST)
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        booking_type = request.form.get('booking_type', '')

        # Common validation
        errors = []

        # Sanitize and validate common fields
        name = sanitize_input(request.form.get('name', ''))
        email = sanitize_input(request.form.get('email', ''))
        phone = sanitize_input(request.form.get('phone', ''))
        guests_str = request.form.get('guests', '')

        if not name:
            errors.append("Name is required.")
        if not email:
            errors.append("Email is required.")
        elif not validate_email(email):
            errors.append("Invalid email format.")
        if not phone:
            errors.append("Phone is required.")
        try:
            guests = validate_guests(guests_str)
        except ValueError as e:
            errors.append(str(e))

        if booking_type == "dining":
            date_str = request.form.get('date', '')
            food = sanitize_input(request.form.get('food', ''))

            if not date_str:
                errors.append("Date is required.")
            else:
                try:
                    booking_date = validate_date(date_str, 'date')
                    if booking_date < datetime.now().date():
                        errors.append("Booking date cannot be in the past.")
                except ValueError as e:
                    errors.append(str(e))

            if not food:
                errors.append("Food option is required.")

            if errors:
                for error in errors:
                    flash(error, 'error')
                return render_template('booking.html'), 400

            return render_template(
                "thankyou.html",
                booking_type="Dining",
                name=name,
                email=email,
                phone=phone,
                date=date_str,
                guests=guests,
                food=food
            )

        elif booking_type == "stay":
            checkin_str = request.form.get('checkin', '')
            checkout_str = request.form.get('checkout', '')
            room = sanitize_input(request.form.get('room', ''))
            food = sanitize_input(request.form.get('food', ''))

            if not checkin_str:
                errors.append("Check-in date is required.")
            if not checkout_str:
                errors.append("Check-out date is required.")

            checkin_date = None
            checkout_date = None
            if checkin_str:
                try:
                    checkin_date = validate_date(checkin_str, 'check-in')
                    if checkin_date < datetime.now().date():
                        errors.append("Check-in date cannot be in the past.")
                except ValueError as e:
                    errors.append(str(e))

            if checkout_str:
                try:
                    checkout_date = validate_date(checkout_str, 'check-out')
                except ValueError as e:
                    errors.append(str(e))

            if checkin_date and checkout_date and checkin_date >= checkout_date:
                errors.append("Check-out date must be after check-in date.")

            if not room:
                errors.append("Room type is required.")
            if not food:
                errors.append("Food option is required.")

            if errors:
                for error in errors:
                    flash(error, 'error')
                return render_template('booking.html'), 400

            return render_template(
                "thankyou.html",
                booking_type="Stay",
                name=name,
                email=email,
                phone=phone,
                checkin=checkin_str,
                checkout=checkout_str,
                guests=guests,
                room=room,
                food=food
            )

    return render_template('booking.html')



# Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Salads page
@app.route('/food/salads')
def salads_page():
    salads = [
        {"name": "Lime & Blistered Peanut Coleslaw", "ingredients": "Mayo-free, with peanuts, cherry tomatoes & lime vinaigrette.", "price": 250},
        {"name": "Caesar Salad", "ingredients": "Crisp lettuce, creamy Caesar dressing, parmesan & croutons.", "price": 300},
        {"name": "Fruit Salad", "ingredients": "Fresh seasonal fruits with a honey-lime drizzle.", "price": 200},
        {"name": "Sprout Salad", "ingredients": "Protein-packed sprouts with onion, tomato & lemon.", "price": 180},
        {"name": "Pasta Salad", "ingredients": "Pasta tossed with veggies & light dressing.", "price": 280}
    ]
    return render_template("salads.html", salads=salads)

@app.route('/food/curries')
def curries_page():
    curries = [
        {
            "name": "Butter Chicken",
            "ingredients": "Tender chicken in creamy tomato-based gravy with butter and spices.",
            "price": 350
        },
        {
            "name": "Mutton Rogan Josh",
            "ingredients": "Juicy lamb pieces slow cooked with Kashmiri spices.",
            "price": 420
        },
        {
            "name": "Fish Curry",
            "ingredients": "Fresh fish cooked with coconut milk and South Indian spices.",
            "price": 300
        },
        {
            "name": "Paneer Tikka Masala",
            "ingredients": "Grilled paneer cubes in spicy and tangy tomato gravy.",
            "price": 280
        }
    ]
    return render_template("curries.html", curries=curries)

@app.route('/food/beverages')
def beverages_page():
    beverages = [
        {
            "name": "Mango Lassi",
            "ingredients": "Sweet mango pulp blended with yogurt, milk, and sugar.",
            "price": 120
        },
        {
            "name": "Masala Chai",
            "ingredients": "Traditional Indian tea brewed with milk, spices, and herbs.",
            "price": 80
        },
        {
            "name": "Cold Coffee",
            "ingredients": "Chilled coffee with milk, sugar, and ice cream topping.",
            "price": 150
        },
        {
            "name": "Fresh Lime Soda",
            "ingredients": "Refreshing lemon soda served sweet or salty.",
            "price": 90
        }
    ]
    return render_template("beverages.html", beverages=beverages)


@app.route('/food/desserts')
def desserts_page():
    desserts = [
        {
            "name": "Gulab Jamun",
            "ingredients": "Soft fried dough balls soaked in sugar syrup.",
            "price": 100
        },
        {
            "name": "Rasgulla",
            "ingredients": "Bengali sweet made with cottage cheese balls in sugar syrup.",
            "price": 120
        },
        {
            "name": "Chocolate Brownie",
            "ingredients": "Rich chocolate cake topped with walnuts and chocolate sauce.",
            "price": 180
        },
        {
            "name": "Ice Cream Sundae",
            "ingredients": "Two scoops of ice cream with chocolate syrup and nuts.",
            "price": 150
        }
    ]
    return render_template("desserts.html", desserts=desserts)



if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug_mode)
