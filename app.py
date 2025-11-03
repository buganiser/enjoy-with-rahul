from flask import Flask, render_template, request

app = Flask(__name__)

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
        booking_type = request.form['booking_type']

        if booking_type == "dining":
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            date = request.form['date']
            guests = request.form['guests']
            food = request.form['food']

            return render_template(
                "thankyou.html",
                booking_type="Dining",
                name=name,
                email=email,
                phone=phone,
                date=date,
                guests=guests,
                food=food
            )

        elif booking_type == "stay":
            name = request.form['name']
            email = request.form['email']
            checkin = request.form['checkin']
            checkout = request.form['checkout']
            guests = request.form['guests']
            room = request.form['room']
            food = request.form['food']

            return render_template(
                "thankyou.html",
                booking_type="Stay",
                name=name,
                email=email,
                checkin=checkin,
                checkout=checkout,
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
    app.run(debug=True)
