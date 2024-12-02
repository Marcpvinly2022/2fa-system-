import tkinter as tk
from tkinter import messagebox, colorchooser
import smtplib
import random
import string
from email.message import EmailMessage

# Replace with your email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "smayowa689@gmail.com"      # Sender email
EMAIL_PASSWORD = "Kgqaizzngrcgtnjm"        # Email app password

# Sample user data
users = {
    "user1": {"password": "mypassword", "email": "user1@example.com", "security_answer": "Group14"},
    "Oladele": {"password": "2022004802", "email": "nehemiaholadele", "security_answer": "Group14"},
    "Lawanson": {"password": "2022003832", "email": "lawansonolalekan@gmail.com", "security_answer": "Group14"},
    "James": {"password": "2022008748", "email": "Jamesolah892@gmail.com", "security_answer": "Group14"},
    "Rohim": {"password": "2022003100", "email": "jubrilrohim2005@gmail.com", "security_answer": "Group14"},
    "Marcpvinly": {"password": "1234", "email": "mayoe751@gmail.com", "security_answer": "Group14"},
    "Olasiji": {"password": "2022011759", "email": "olasijiphilip@gmail.com", "security_answer": "Group14"},
    "Adelasoye": {"password": "2022005248", "email": "adelasoyeadedamola8@gmail.com", "security_answer": "Group14"},
    "Oluwafemi": {"password": "2022005933", "email": "aolufemi605@gmail.com", "security_answer": "Group14"},
    "Oyedare": {"password": "2022005268", "email": "mercyoyedare2525@gmail.com", "security_answer": "Group14"},
    "Ajamu": {"password": "2022004647", "email": "judahadepoju2@gmail.com", "security_answer": "Group14"},
    "Swep Group14": {"password": "Group_14", "email": "judahadepoju2@gmail.com", "security_answer": "Group14"},
    "alice_smith": {"password": "password123", "email": "alicesmith@example.com", "security_answer": "Group14"}
}

# Global variables
current_user = None
otp_code = None
selected_color = "#ffffff"  # Default background color

# Function to generate random OTP
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

# Function to send OTP to user's email
def send_otp_email(email, otp_code):
    msg = EmailMessage()
    msg['Subject'] = 'Your OTP Code'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg.set_content(f"Your OTP code is: {otp_code}")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        messagebox.showinfo("OTP Sent", f"An OTP has been sent to {email}.")
    except Exception as e:
        messagebox.showerror("Email Error", f"Failed to send OTP email. Error: {e}")

# Function to validate OTP and show security question
def validate_otp(entered_otp):
    if entered_otp == otp_code:
        otp_window.destroy()
        show_security_question()
    else:
        messagebox.showerror("Invalid OTP", "The OTP you entered is incorrect.")

# Function to validate the security answer
def validate_security_answer(answer):
    if answer.lower() == users[current_user]["security_answer"].lower():
        security_window.destroy()
        show_welcome_screen()
    else:
        messagebox.showerror("Invalid Answer", "Incorrect answer to the security question.")

# Function to show the OTP entry screen
def show_otp_screen():
    global otp_code, otp_window
    otp_code = generate_otp()
    user_email = users[current_user]["email"]
    send_otp_email(user_email, otp_code)

    otp_window = tk.Toplevel()
    otp_window.title("Enter OTP")
    otp_window.config(bg=selected_color)
    otp_window.geometry("300x300")
    tk.Label(otp_window, text="Enter OTP sent to your email:", bg=selected_color).pack(pady=10)
    otp_entry = tk.Entry(otp_window)
    otp_entry.pack(pady=5)

    def submit_otp():
        validate_otp(otp_entry.get().strip())

    tk.Button(otp_window, text="Submit", command=submit_otp).pack(pady=10)

# Function to show security question
def show_security_question():
    global security_window
    security_window = tk.Toplevel()
    security_window.title("Security Question")
    security_window.geometry("400x400")
    security_window.config(bg=selected_color)

    tk.Label(security_window, text="What is the name of Your swep group?", bg=selected_color).pack(pady=10)
    answer_entry = tk.Entry(security_window)
    answer_entry.pack(pady=10)

    def submit_answer():
        validate_security_answer(answer_entry.get().strip())

    tk.Button(security_window, text="Submit", command=submit_answer).pack(pady=10)

# Function to show welcome screen
def show_welcome_screen():
    welcome_window = tk.Toplevel()
    welcome_window.title("Welcome")
    welcome_window.geometry("400x400")
    welcome_window.config(bg=selected_color)

    tk.Label(welcome_window, text="Welcome to the platform!", font=("Helvetica", 16), bg=selected_color).pack(pady=20)

    # Logout button that returns to the login window
    tk.Button(welcome_window, text="Logout", command= create_login_window).pack(pady=90)

# Function to handle login
def login():
    global current_user
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if username in users and users[username]["password"] == password:
        current_user = username
        login_window.destroy()
        show_otp_screen()
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password.")

# Function to choose background color
def choose_color():
    global selected_color
    color_code = colorchooser.askcolor(title="Choose Background Color")
    if color_code[1]:
        selected_color = color_code[1]
        login_window.config(bg=selected_color)

# Logout function that returns to the login page
def logout():
    global login_window
    current_user = None  # Reset the current user
    for widget in login_window.winfo_children():
        widget.destroy()  # Destroy all widgets from the current window
    login_window.deiconify()  # Show the login window again

# Tkinter login window
def create_login_window():
    global login_window, username_entry, password_entry
    login_window = tk.Tk()
    login_window.title("2FA Login System")
    login_window.geometry("400x400")
    login_window.config(bg=selected_color)

    # Login page elements
    tk.Label(login_window, text="Username:", bg=selected_color, font=("Helvetica", 12)).pack(pady=10)
    username_entry = tk.Entry(login_window, font=("Helvetica", 12))
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:", bg=selected_color, font=("Helvetica", 12)).pack(pady=10)
    password_entry = tk.Entry(login_window, show="*", font=("Helvetica", 12))
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Choose Background Color", command=choose_color, bg="#4CAF50", fg="white").pack(pady=10)
    tk.Button(login_window, text="Login", command=login, font=("Helvetica", 12), bg="#4CAF50", fg="white").pack(pady=20)

    login_window.mainloop()

# Start the app
create_login_window()
