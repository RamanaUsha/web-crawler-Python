from flask import Flask, render_template, flash
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your_app_password'     # Replace with your App Password
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'

mail = Mail(app)

# Test Email Route
@app.route('/send_test_email')
def send_test_email():
    try:
        msg = Message('Test Email', recipients=['recipient@example.com'])
        msg.body = 'This is a test email sent from your Flask app!'
        mail.send(msg)
        return 'Test email sent successfully!'
    except Exception as e:
        return f'Error sending email: {e}'

if __name__ == '__main__':
    app.run(debug=True)
