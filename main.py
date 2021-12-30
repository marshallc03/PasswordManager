from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json

# ---------------------------- CONSTANTS ------------------------------- #
FONT = ("Roboto", 10, "normal")
BG_COLOR = "#FEFBF3"
BUTTON_COLOR = "#79B4B7"
TEXT_COLOR = "#9D9D9D"
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
           't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
           'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    """
    Generates a new password when user clicks "Generate Password" button. The password is inserted into the
    password_entry field and copied to clipboard.
    """
    pw_letters = [choice(LETTERS) for letter in range(randint(8, 10))]
    pw_numbers = [choice(NUMBERS) for numbers in range(randint(2, 4))]
    pw_symbols = [choice(SYMBOLS) for symbol in range(randint(2, 4))]

    pw_list = pw_letters + pw_numbers + pw_symbols
    shuffle(pw_list)

    password = ''.join(pw_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_password():
    """
    Saves the website, email/username, and password provided by the user to a json file. If any of the entries are blank
    user will receive a warning message.
    """
    website = website_entry.get()
    username = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": username,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0 or len(username) == 0:
        messagebox.showwarning(title="Warning", message="Unable to proceed: Empty fields!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"Details Entered: \n\nEmail: {username} "
                                                              f" \nPassword: {password} \n\nIs this okay?")

        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- SEARCH BUTTON ------------------------------- #

def search():
    """
    When a user clicks the "Search" button, json file will be searched for account details (email/username, password)
    and the details will be displayed in a message box. If no details are found, message will alert user that no account
    details were found.
    """
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            username = data[website]["email"]
            password = data[website]["password"]
    except FileNotFoundError:
        messagebox.showwarning(title="No Entry", message="Unable to proceed: No account details for that website.")
    except KeyError:
        messagebox.showwarning(title="No Entry", message="Unable to proceed: No account details for that website.")
    else:
        messagebox.showinfo(title=f"{website}", message=f"Account Details: \nEmail: {username} \nPassword: {password}")


# ---------------------------- UI SETUP ------------------------------- #

# Window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=BG_COLOR)

# Image
canvas = Canvas(width=200, height=200, bg=BG_COLOR, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:", font=FONT, bg=BG_COLOR)
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:", font=FONT, bg=BG_COLOR)
email_label.grid(row=2, column=0)
password_label = Label(text="Password:", font=FONT, bg=BG_COLOR)
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=39)
email_entry.grid(row=2, column=1, columnspan=2)
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# Buttons
password_button = Button(text="Generate Password", width=15, highlightthickness=0, command=generate_password)
password_button.grid(row=3, column=2)
search_button = Button(text="Search", width=15, highlightthickness=0, command=search)
search_button.grid(row=1, column=2)
add_button = Button(text="Add", width=40, highlightthickness=0, command=save_password)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
