import tkinter as tk
from tkinter import messagebox
import json
import os

# Quiz data created a dictionary to store the questions along with their
# possible options and the correct answer for that particular question

questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Lisbon"],
        "answer": "Paris"
    },
    {
        "question": "Which city is known as the city of golden gate?",
        "options": ["Rome", "New York", "London", "San Francisco"],
        "answer": "San Francisco"
    },
    {
        "question": "Which city is known as the Big Apple?",
        "options": ["Los Angeles", "Chicago", "Miami", "New York"],
        "answer": "New York"
    },
    {
        "question": "Which city is known as the city of seven hills?",
        "options": ["Beijing", "Washington DC", "Rome", "Cape Town"],
        "answer": "Rome"
    },
    {
        "question": "What is the capital of Australia?",
        "options": ["Sydney", "Melbourne", "Brisbane", "Canberra"],
        "answer": "Canberra"
    },
    {
        "question": "What is the capital of Canada?",
        "options": ["Toronto", "Vancouver", "Ottawa", "Montreal"],
        "answer": "Ottawa"
    },
    {
        "question": "Which country is known as the Land of the Rising Sun?",
        "options": ["China", "Japan", "South Korea", "Thailand"],
        "answer": "Japan"
    },
    {
        "question": "Which country is known as the Land of the Thunder Dragon?",
        "options": ["Bhutan", "Nepal", "Tibet", "Mongolia"],
        "answer": "Bhutan"
    },
    {
        "question": "Which country is known as the Land of the Midnight Sun?",
        "options": ["Norway", "Sweden", "Finland", "Iceland"],
        "answer": "Norway"
    },
    {
        "question": "What is the capital of Russia?",
        "options": ["St. Petersburg", "Moscow", "Kazan", "Novosibirsk"],
        "answer": "Moscow"
    },
]

class QuizApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Quiz Game")
        self.root.configure(bg="lightblue")  # Set background color

        self.question_index = 0
        self.score = 0
        self.selected_option = tk.StringVar()

        self.create_widgets()
        self.display_question()

    def create_widgets(self):
        self.question_label = tk.Label(self.root, text="", font=('Arial', 14), bg="lightblue")
        self.question_label.pack(pady=20)

        self.option_buttons = []
        for _ in range(4):
            btn = tk.Radiobutton(self.root,
                                 text="",
                                 variable=self.selected_option,
                                 value="",
                                 font=('Arial', 12),
                                 bg="lightblue")
            btn.pack(anchor='w')
            self.option_buttons.append(btn)

        self.submit_button = tk.Button(self.root,
                                       text="Submit",
                                       command=self.check_answer,
                                       bg="blue", fg="white")  # Set button colors
        self.submit_button.pack(pady=20)

    def display_question(self):
        question = questions[self.question_index]
        self.question_label.config(text=question["question"])

        self.selected_option.set(None)  # Reset selected option
        for i, option in enumerate(question["options"]):
            self.option_buttons[i].config(text=option, value=option)

    def check_answer(self):
        selected_answer = self.selected_option.get()
        correct_answer = questions[self.question_index]["answer"]

        if selected_answer == correct_answer:
            self.score += 1

        self.question_index += 1
        if self.question_index < len(questions):
            self.display_question()
        else:
            self.show_result()

    def show_result(self):
        result_text = f"{self.username}, your score is {self.score} out of {len(questions)}"
        messagebox.showinfo("Quiz Result", result_text)
        self.root.destroy()

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.configure(bg="lightblue")  # Set background color

        self.username_label = tk.Label(self.root, text="Username", font=('Arial', 12), bg="lightblue")
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(self.root, font=('Arial', 12))
        self.username_entry.pack(pady=10)

        self.password_label = tk.Label(self.root, text="Password", font=('Arial', 12), bg="lightblue")
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(self.root, show="*", font=('Arial', 12))
        self.password_entry.pack(pady=10)

        self.login_button = tk.Button(self.root, text="Login", command=self.check_login, bg="blue", fg="white")
        self.login_button.pack(pady=10)
        
        self.register_button = tk.Button(self.root, text="Register", command=self.register, bg="green", fg="white")
        self.register_button.pack(pady=10)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check username and password
        if self.verify_credentials(username, password):
            self.root.destroy()
            self.start_quiz(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def register(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("Register")
        register_window.configure(bg="lightblue")  # Set background color

        tk.Label(register_window, text="Username", font=('Arial', 12), bg="lightblue").pack(pady=10)
        username_entry = tk.Entry(register_window, font=('Arial', 12))
        username_entry.pack(pady=10)

        tk.Label(register_window, text="Password", font=('Arial', 12), bg="lightblue").pack(pady=10)
        password_entry = tk.Entry(register_window, show="*", font=('Arial', 12))
        password_entry.pack(pady=10)

        def save_credentials():
            username = username_entry.get()
            password = password_entry.get()
            if username and password:
                credentials = self.load_credentials()
                if username in credentials:
                    messagebox.showerror("Error", "Username already exists")
                else:
                    credentials[username] = password
                    self.save_credentials(credentials)
                    messagebox.showinfo("Success", "Account created successfully")
                    register_window.destroy()
            else:
                messagebox.showerror("Error", "Please fill in both fields")

        tk.Button(register_window, text="Register ", command=save_credentials, bg="green", fg="white").pack(pady=10)

    def verify_credentials(self, username, password):
        credentials = self.load_credentials()
        return credentials.get(username) == password

    def load_credentials(self):
        if not os.path.exists("credentials.json"):
            return {}
        with open("credentials.json", "r") as file:
            return json.load(file)

    def save_credentials(self, credentials):
        with open("credentials.json", "w") as file:
            json.dump(credentials, file)

    def start_quiz(self, username):
        quiz_root = tk.Tk()
        app = QuizApp(quiz_root, username)
        quiz_root.mainloop()

# Create the login window
login_root = tk.Tk()
login_app = LoginApp(login_root)
login_root.mainloop()

