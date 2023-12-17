from flask import Flask, render_template, request
import your_email_function_module  # Replace this with the module where your email sending function resides
import sqlite3
from flask import Flask, render_template, request
from flask import Flask, render_template, request, redirect  # Add 'redirect' to the import statement




app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_email = request.form['customer_email']
        email_sent = your_email_function_module.send_email(customer_email, customer_name)

        if email_sent:
            return "Email sent successfully with the unique coupon code!"
        else:
            return "Failed to send the email. Please check your mail configuration."

@app.route('/view_data')
def view_data():
    conn = sqlite3.connect('customer_coupons.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CustomerCoupons")
    data = cursor.fetchall()
    conn.close()
    return render_template('view_data.html', data=data)

@app.route('/get_customer_info', methods=['GET', 'POST'])
def get_customer_info():
    if request.method == 'POST':
        coupon_code = request.form['coupon_code']
        conn = sqlite3.connect('customer_coupons.db')
        cursor = conn.cursor()
        cursor.execute("SELECT CustomerName, Email FROM CustomerCoupons WHERE CouponCode = ?", (coupon_code,))
        customer_data = cursor.fetchone()
        conn.close()
        return render_template('customer_info.html', customer_data=customer_data)
    return render_template('customer_info.html')

@app.route('/delete_customer', methods=['POST'])
def delete_customer():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        
        # Perform deletion operation using customer_id
        
        # For demonstration purposes, assuming deletion is successful
        # Replace this with your actual deletion logic
        deletion_successful = True
        
        if deletion_successful:
            # Redirect to the view_data route after successful deletion
            return redirect('/view_data')  # Use the 'redirect' function to redirect to the view_data route
        else:
            return "Failed to delete the customer."

@app.route('/modify_customer/<int:customer_id>')
def modify_customer(customer_id):
    # Logic to retrieve customer details based on customer_id
    # Render a page/form to modify customer details
    return render_template('modify_customer.html', customer_id=customer_id)

@app.route('/delete_all_customers', methods=['POST'])
def delete_all_customers():
    if request.method == 'POST':
        # Perform deletion of all customer data from the database
        # Replace this with your actual deletion logic
        # For example:
        # conn = sqlite3.connect('customer_coupons.db')
        # cursor = conn.cursor()
        # cursor.execute("DELETE FROM CustomerCoupons")
        # conn.commit()
        # conn.close()

        # For demonstration purposes, assuming deletion is successful
        deletion_successful = True
        
        if deletion_successful:
            # Redirect to the view_data route after successful deletion
            return redirect('/view_data')
        else:
            return "Failed to delete all customers."

if __name__ == '__main__':
    app.run(debug=True)
    

    app = Flask(__name__, template_folder='templates')

