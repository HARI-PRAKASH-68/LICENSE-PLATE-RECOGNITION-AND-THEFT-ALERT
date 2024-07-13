import db
import tkinter as tk
from tkinter import messagebox
from login import login
import subprocess
db
class HomePage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.login_button = tk.Button(self, text="Login", width=10, height=2, command=self.show_login_page,highlightbackground="black")
        self.login_button.pack(side=tk.LEFT,padx=10,pady=70)

        self.signup_button = tk.Button(self, text="Sign Up", width=10, height=2, command=self.show_signup_window,highlightbackground="black")
        self.signup_button.pack(side=tk.LEFT,padx=30)


    def show_login_page(self):
        self.destroy()  # Close the current page
        login_page = LoginPage(self.master)
        login_page.pack()

    def show_signup_window(self):
        # Run signup.py as a separate process
        subprocess.run(['python', 'signup.py'], check=True)
        #os.system('python signup.py')

        # After signup is finished, you may want to update your login window
        # For example, destroy the current window and recreate the login window
        self.destroy()
        login_window = tk.Tk()
        login_window.geometry("388x210")
        login_window.title("Login")
        login_page = LoginPage(login_window)
        login_page.pack()
    def animate_button(self, button):
        current_bg_color = button.cget("bg")
        new_bg_color = "blue" if current_bg_color == "green" else "green"
        button.configure(bg=new_bg_color)
        self.after(1000, self.animate_button, button)
    def animate_button1(self, button):
        current_bg_color = button.cget("bg")
        new_bg_color = "yellow" if current_bg_color == "pink" else "pink"
        button.configure(bg=new_bg_color)
        self.after(1000, self.animate_button1, button)
    def on_enter(self, event):
        event.widget.config(bg="#6E007E")  # Change background color on mouse enter
    def on_leave(self, event):
        event.widget.config(bg=self)

class LoginPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.username_label = tk.Label(self, text="Username or Email:")
        self.username_label.pack()

        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login",width=10, height=2, command=self.show_login_option_page,background="green",highlightbackground="yellow")
        self.login_button.pack(pady=(30, 70))

    def get_login_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        return username, password

    def show_login_option_page(self):
        username_or_email = self.username_entry.get()
        password = self.password_entry.get()
        result = login(username_or_email, password)
        if result:
            self.destroy()
            login_option_page = LoginOptionPage(self.master, result)
            login_option_page.pack()
            return username_or_email, password
        else:
            messagebox.showerror("Login Failed", "Invalid username/email or password")

class LoginOptionPage(tk.Frame):
    def __init__(self, master=None, user_data=None):
        super().__init__(master)
        self.master = master
        self.user_data = user_data
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.login_option_label = tk.Label(self, text=f"WELCOME \n {self.user_data[1]}")
        self.login_option_label.pack()
        # Button to start license plate detection
        self.start_plate_detection_button = tk.Button(self, text="Start", width=10, height=2, command=self.start_plate_detection, highlightbackground="blue")
        self.start_plate_detection_button.pack(side=tk.TOP, pady=(40, 70), anchor=tk.CENTER)

    def start_plate_detection(self):
        subprocess.run(['python', 'main.py'], check=True)
# Create the main application window
root = tk.Tk()
root.title("License Plate App")
root.geometry("388x210")
# Start with the home page
home_page = HomePage(root)
home_page.pack()

# Start the Tkinter GUI event loop
root.mainloop()