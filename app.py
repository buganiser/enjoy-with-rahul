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
        name = request.form['name']
        email = request.form['email']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        guests = request.form['guests']
        room = request.form['room']

        return render_template(
            'thankyou.html',
            name=name,
            email=email,
            checkin=checkin,
            checkout=checkout,
            guests=guests,
            room=room
        )
    return render_template('booking.html')

# Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
