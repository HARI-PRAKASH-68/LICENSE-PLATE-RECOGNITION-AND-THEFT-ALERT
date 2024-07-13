import tkinter as tk
from tkinter import messagebox
import sqlite3
from genOTP import generate_otp, send_otp  

class SignUpPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.expected_otp = None
    
        self.email_address = None

    def create_widgets(self):
        self.email_label = tk.Label(self, text="Enter your email:")
        self.email_label.pack()

        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        self.send_otp_button = tk.Button(self, text="Send OTP", command=self.send_otp)
        self.send_otp_button.pack(pady=(30, 70))


        
        self.sent_otp_label = tk.Label(self, text="")
        self.sent_otp_label.pack()

    def send_otp(self):
        email = self.email_entry.get()
        self.email_address = email  
        self.expected_otp = generate_otp()
        send_otp(email, self.expected_otp)
        messagebox.showinfo("OTP Sent", f"OTP has been sent to {email}.")

        
        self.sent_otp_label.config(text=f"OTP sent to {email}")

        
        self.email_label.destroy()
        self.email_entry.destroy()
        self.send_otp_button.destroy()

        
        self.otp_label = tk.Label(self, text="Enter OTP:")
        self.otp_label.pack()
        
        self.otp_entry = tk.Entry(self)  
        self.otp_entry.pack()

        self.verify_otp_button = tk.Button(self, text="Verify OTP", command=self.verify_otp)
        self.verify_otp_button.pack(pady=(30, 70))

    def verify_otp(self):
        entered_otp = self.otp_entry.get()

        if self.expected_otp and entered_otp == self.expected_otp:
            messagebox.showinfo("OTP Verified", "OTP verification successful.")

           
            self.otp_label.destroy()
            self.otp_entry.destroy()
            self.verify_otp_button.destroy()

            self.username_label = tk.Label(self, text="Enter your username:")
            self.username_label.pack()

            self.username_entry = tk.Entry(self)
            self.username_entry.pack()

            self.password_label = tk.Label(self, text="Enter your password:")
            self.password_label.pack()

            self.password_entry = tk.Entry(self, show="*")  # Mask the password entry
            self.password_entry.pack()

            self.signup_button = tk.Button(self, text="Sign Up", command=self.sign_up)
            self.signup_button.pack(padx=10,pady=10)
        else:
            messagebox.showerror("OTP Verification Failed", "Invalid OTP.")
    def sign_up(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

    
        conn = sqlite3.connect("license.db")
        cursor = conn.cursor()

   
        cursor.execute("INSERT INTO users (email, otp, username, password) VALUES (?, ?, ?, ?)",
                   (self.email_address, self.expected_otp, username, password))

    
        conn.commit()
        conn.close()


   
        messagebox.showinfo("Sign Up Successful", f"Welcome, {username}! You have successfully signed up.")

    
        self.master.destroy()



root = tk.Tk()
root.geometry("388x210")
root.title("Sign Up")
sign_up_page = SignUpPage(root)
sign_up_page.pack()
root.mainloop()
