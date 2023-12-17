import smtplib
import random
import string
from email.message import EmailMessage
import sqlite3

# Function to generate a random coupon code
def generate_coupon():
    coupon_length = 8
    characters = string.ascii_letters + string.digits
    coupon = ''.join(random.choice(characters) for i in range(coupon_length))
    return coupon

# Function to check if email exists in the database
def check_existing_email(customer_email):
    conn = sqlite3.connect('customer_coupons.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Email FROM CustomerCoupons WHERE Email = ?", (customer_email,))
    result = cursor.fetchone()
    conn.close()
    return bool(result)

# Function to create the table if it doesn't exist
def create_table():
    conn = sqlite3.connect('customer_coupons.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CustomerCoupons (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerName TEXT,
            Email TEXT,
            CouponCode TEXT
        )
    ''')

    conn.commit()
    conn.close()


# Function to save customer details and coupon code to a SQLite database
def save_to_database(customer_email, customer_name, coupon_code):
    conn = sqlite3.connect('customer_coupons.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CustomerCoupons (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerName TEXT,
            Email TEXT,
            CouponCode TEXT
        )
    ''')

    cursor.execute('''
        INSERT INTO CustomerCoupons (CustomerName, Email, CouponCode)
        VALUES (?, ?, ?)
    ''', (customer_name, customer_email, coupon_code))

    conn.commit()
    conn.close()

# Function to send email
def send_email(customer_email, customer_name):
    sender_email = 'akram@elegode.space'
    sender_password = '5YbqYX9iJP9'

    coupon_code = generate_coupon()  # Generate a unique coupon for each customer

    if check_existing_email(customer_email):
        print("Email already exists in the records. No email sent.")
        return False

    # Save customer details and coupon to the SQLite database
    save_to_database(customer_email, customer_name, coupon_code)

    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = customer_email
    msg['Subject'] = 'Your Exclusive Coupon Code'
    msg.set_content(f"Hi {customer_name},\n\nHere is your unique coupon code: {coupon_code}")

    try:
        with smtplib.SMTP_SSL('mail.elegode.space', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send the email. Error: {str(e)}")
        return False

# Create the table if it doesn't exist
create_table()

# Input customer name and email after running the code
customer_name = input("Enter customer's name: ")
customer_email = input("Enter customer's email address: ")

# Send the email with the unique coupon code for this customer if email doesn't exist already
email_sent = send_email(customer_email, customer_name)

if email_sent:
    print("Email sent successfully with the unique coupon code!")
else:
    print("Failed to send the email. Please check your mail configuration.")