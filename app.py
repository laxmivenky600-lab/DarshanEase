import sqlite3
from flask import Flask, render_template,request,redirect,session
from flask import send_file
from reportlab.pdfgen import canvas
app = Flask(__name__)
app.secret_key="darshanease123"
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()
        if user:
             session["user"] = email
             return redirect("/dashboard")
        else:
             return "Invalid Email or Password"
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return "Registration Successful!"

    return render_template("register.html")

@app.route("/temples")
def temples():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, temple_name, image
        FROM temples
    """)

    temples = cursor.fetchall()

    conn.close()

    return render_template("temple.html", temples=temples)
@app.route("/book/<int:id>")
def book(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT temple_name FROM temples WHERE id=?", (id,))
    temple = cursor.fetchone()

    conn.close()

    if temple:
        return render_template("booking.html", temple=temple[0])

    return "Temple Not Found"
@app.route('/bookings')
def bookings():
    return render_template("booking.html")

@app.route('/payment', methods=['POST'])
def payment():

    name = request.form['name']
    email = request.form['email']
    mobile = request.form['mobile']
    temple = request.form['temple']
    date = request.form['date']
    tickets = int(request.form['tickets'])

    amount = tickets * 100

    return render_template(
        "payment.html",
        name=name,
        email=email,
        mobile=mobile,
        temple=temple,
        date=date,
        tickets=tickets,
        amount=amount
    )

@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    name = request.form['name']
    email = request.form['email']
    mobile = request.form['mobile']
    temple = request.form['temple']
    booking_date = request.form['date']
    tickets = request.form['tickets']

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO bookings
(name, email, mobile, temple, booking_date, tickets, payment_status)
VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, email, mobile, temple, booking_date, tickets,"paid"))

    conn.commit()
    conn.close()

    return f"""
    <h2>✅ Booking Successful!</h2>
    <hr>
    <p><b>Name:</b> {name}</p>
    <p><b>Email:</b> {email}</p>
    <p><b>Mobile:</b> {mobile}</p>
    <p><b>Temple:</b> {temple}</p>
    <p><b>Date:</b> {booking_date}</p>
    <p><b>Tickets:</b> {tickets}</p>

    <br>
    <a href="/dashboard">Go to Dashboard</a>
    """
@app.route('/dashboard')
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html")
@app.route('/my_bookings')
def my_bookings():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, temple, booking_date, tickets,payment_status
        FROM bookings
    """)

    bookings = cursor.fetchall()

    conn.close()

    return render_template("my_bookings.html", bookings=bookings)
@app.route('/cancel_booking/<int:id>')
def cancel_booking(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM bookings WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/my_bookings")
@app.route('/search', methods=['GET', 'POST'])
def search():
    result = None

    if request.method == 'POST':
        temple = request.form['temple']

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT temple_name, state, city,
                   opening_time, closing_time,
                   description, image
            FROM temples
            WHERE temple_name LIKE ?
        """, ('%' + temple + '%',))

        result = cursor.fetchone()

        conn.close()

    return render_template("search.html", result=result)
@app.route('/download_ticket/<int:id>')
def download_ticket(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, temple, booking_date, tickets, payment_status
        FROM bookings
        WHERE id=?
    """, (id,))

    booking = cursor.fetchone()
    conn.close()

    if booking is None:
        return "Booking not found"

    filename = f"ticket_{id}.pdf"

    pdf = canvas.Canvas(filename)

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(180, 800, "DarshanHub Ticket")

    pdf.setFont("Helvetica", 12)

    pdf.drawString(60, 740, f"Booking ID : {id}")
    pdf.drawString(60, 710, f"Name : {booking[0]}")
    pdf.drawString(60, 680, f"Temple : {booking[1]}")
    pdf.drawString(60, 650, f"Date : {booking[2]}")
    pdf.drawString(60, 620, f"Tickets : {booking[3]}")
    pdf.drawString(60, 590, f"Payment Status : {booking[4]}")

    pdf.save()

    return send_file(filename, as_attachment=True)
@app.route('/profile')
def profile():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, email FROM users LIMIT 1")
    user = cursor.fetchone()

    conn.close()

    return render_template("profile.html", user=user)
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "siri" and password == "siri123":
            return redirect('/admin')
        else:
            return "Invalid Admin Credentials"

    return render_template("admin_login.html")
@app.route("/admin")
def admin():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bookings")
    total_bookings = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bookings WHERE payment_status='Approved'")
    approved = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bookings WHERE payment_status='Rejected'")
    rejected = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "admin.html",
        total_users=total_users,
        total_bookings=total_bookings,
        approved=approved,
        rejected=rejected
    )
@app.route("/admin/users")
def admin_users():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()

    conn.close()

    return render_template("admin_users.html", users=users)
@app.route("/admin/bookings")
def admin_bookings():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, mobile, temple,
               booking_date, tickets, payment_status
        FROM bookings
    """)

    bookings = cursor.fetchall()
    conn.close()

    return render_template("admin_bookings.html", bookings=bookings)
@app.route("/approve/<int:id>")
def approve_booking(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE bookings SET payment_status='Approved' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/admin/bookings")


@app.route("/reject/<int:id>")
def reject_booking(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE bookings SET payment_status='Rejected' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/admin/bookings")
@app.route("/admin/add_temple", methods=["GET","POST"])
def add_temple():

    if request.method=="POST":

        temple_name=request.form["temple_name"]
        state=request.form["state"]
        city=request.form["city"]
        description=request.form["description"]
        opening=request.form["opening_time"]
        closing=request.form["closing_time"]
        image=request.form["image"]
        contact=request.form["contact"]

        conn=sqlite3.connect("database.db")
        cursor=conn.cursor()

        cursor.execute("""
        INSERT INTO temples
        (temple_name,state,city,description,
        opening_time,closing_time,image,contact)

        VALUES(?,?,?,?,?,?,?,?)
        """,(temple_name,state,city,description,
             opening,closing,image,contact))

        conn.commit()
        conn.close()

        return redirect("/admin")

    return render_template("add_temple.html")
@app.route("/admin/view_temples")
def view_temples():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM temples")

    temples = cursor.fetchall()
    print(temples)

    conn.close()

    return render_template(
        "view_temples.html",
        temples=temples
    )
@app.route("/admin/delete_temple/<int:id>")
def delete_temple(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM temples WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/admin/view_temples")
    
@app.route("/admin/edit_temple/<int:id>", methods=["GET","POST"])
def edit_temple(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":

        temple_name = request.form["temple_name"]
        state = request.form["state"]
        city = request.form["city"]
        description = request.form["description"]
        opening = request.form["opening_time"]
        closing = request.form["closing_time"]
        image = request.form["image"]
        contact = request.form["contact"]

        cursor.execute("""
        UPDATE temples
        SET temple_name=?,
            state=?,
            city=?,
            description=?,
            opening_time=?,
            closing_time=?,
            image=?,
            contact=?
        WHERE id=?
        """,(
            temple_name,
            state,
            city,
            description,
            opening,
            closing,
            image,
            contact,
            id
        ))

        conn.commit()
        conn.close()

        return redirect("/admin/view_temples")

    cursor.execute("SELECT * FROM temples WHERE id=?",(id,))
    temple = cursor.fetchone()

    conn.close()

    return render_template(
        "edit_temple.html",
        temple=temple
    )
@app.route("/partner", methods=["GET", "POST"])
def partner():

    if request.method == "POST":

        temple_name = request.form["temple_name"]
        person = request.form["person"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        state = request.form["state"]
        city = request.form["city"]
        address = request.form["address"]
        description = request.form["description"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO partners
        (temple_name, person, email, mobile, state, city, address, description)
        VALUES(?,?,?,?,?,?,?,?)
        """,
        (temple_name, person, email, mobile, state, city, address, description))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("partner.html")
@app.route("/feedback", methods=["GET", "POST"])
def feedback():

    if request.method == "POST":

        username = request.form["username"]
        temple_name = request.form["temple_name"]
        rating = request.form["rating"]
        review = request.form["review"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO feedback(username, temple_name, rating, review)
        VALUES(?,?,?,?)
        """, (username, temple_name, rating, review))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("feedback.html")
@app.route("/admin/view_feedback")
def view_feedback():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM feedback")

    feedbacks = cursor.fetchall()

    conn.close()

    return render_template(
        "view_feedback.html",
        feedbacks=feedbacks
    )
@app.route("/admin/delete_feedback/<int:feedback_id>")
def delete_feedback(feedback_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM feedback WHERE id = ?", (feedback_id,))

    conn.commit()
    conn.close()

    return redirect("/admin/view_feedback")
@app.route("/reviews/<path:temple_name>")
def temple_reviews(temple_name):

    temple_name = temple_name.replace("%20", " ").strip()

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, temple_name, rating, review
        FROM feedback
        WHERE UPPER(TRIM(temple_name)) = UPPER(TRIM(?))
    """, (temple_name,))

    reviews = cursor.fetchall()

    conn.close()
    print("Temple =", temple_name)
    print(images.keys())
    print(images.get(temple_name))
    return render_template(
        "temple_reviews.html",
        reviews=reviews,
        temple_name=temple_name
    )

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/login")
@app.route("/check_feedback")
def check_feedback():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM feedback")
    data = cursor.fetchall()

    conn.close()

    return str(data)
@app.route("/gallery/<path:temple_name>")
def temple_gallery(temple_name):

    temple_name = temple_name.replace("%20", " ").strip().upper()

    gallery_images = []

    if "AINAVILLI" in temple_name:
        gallery_images = [
            "images/ainavilli1.jpg",
            "images/ainavilli2.jpg",
            "images/ainavilli3.jpg",
            "images/ainavilli4.jpg",
            "images/ainavilli5.jpg"
        ]

    elif "SRISAILAM" in temple_name:
        gallery_images = [
            "images/srisailam1.jpg",
            "images/srisailam2.jpg",
            "images/srisailam3.jpg",
            "images/srisailam4.jpg",
            "images/srisailam5.jpg"
        ]

    elif "KANAKADURGA" in temple_name:
        gallery_images = [
            "images/kanaka1.jpg",
            "images/kanaka2.jpg",
            "images/kanaka3.jpg",
            "images/kanaka4.jpg",
            "images/kanaka5.jpg"
        ]

    elif "THIRUMALA" in temple_name or "THIRUMAL" in temple_name or "TIRUMALA" in temple_name:
        gallery_images = [
            "images/tirumala1.jpg",
            "images/tirumala2.jpg",
            "images/tirumala3.jpg",
            "images/tirumala4.jpg",
            "images/tirumala5.jpg"
        ]

    print("Temple Name:", temple_name)
    print("Gallery Images:", gallery_images)

    return render_template(
        "temple_gallery.html",
        temple_name=temple_name,
        gallery_images=gallery_images
    )
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form["email"]
        new_password = request.form["new_password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()

        if user:
            cursor.execute(
                "UPDATE users SET password=? WHERE email=?",
                (new_password, email)
            )
            conn.commit()
            conn.close()

            return """
            <h2>Password Updated Successfully!</h2>
            <br>
            <a href='/login'>Go to Login</a>
            """

        conn.close()

        return "Email not registered."

    return render_template("forgot_password.html")
if __name__ == '__main__':
    app.run(debug=True)