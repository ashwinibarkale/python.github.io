from flask import Flask, render_template, request, redirect, url_for
import re
app = Flask(__name__)

def validate_form(name, email, phone, password, confirm_password):
    errors = {}

    if not name or not all(char.isalpha() or char.isspace() for char in name):
        errors['name'] = "Name should not be empty and should contain only alphabets and spaces."

    if not phone.isdigit() or len(phone) != 10 or not (phone.startswith('7') or phone.startswith('8') or phone.startswith('9')):
        errors['phone'] = "Phone should be a 10-digit number starting with 7, 8, or 9."

    if not email or '@' not in email or '.' not in email:
        errors['email'] = "Invalid email format."

    if not password or len(password) < 8 or len(password) > 12 or not re.match("^[a-zA-Z0-9!@#$%^&*()_-]+$", password):
        errors['password'] = "Password should be 8 to 12 characters long and contain only alphanumeric and special characters (!@#$%^&*()_-)."

    if password != confirm_password:
        errors['confirm_password'] = "Passwords do not match."

    return errors  # Dictionary of errors, empty if validation is successful

@app.route('/')
def index():
    return render_template('index.html', validation_message={})

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    validation_errors = validate_form(name, email, phone, password, confirm_password)

    if validation_errors:
        return render_template('index.html', validation_message=validation_errors)

    # Clear validation messages after successful submission
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return "Form submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)
