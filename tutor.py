import tkinter as tk
from tkinter import simpledialog, scrolledtext
import openai
from pathlib import Path
import tkinter.ttk as ttk

# Set up OpenAI
openai.api_key = "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"

class PythonTutor:

    def __init__(self, master):
        self.master = master
        master.title("Python Tutor")

        self.label = tk.Label(master, text="Python Tutor", font=('Arial', 24))
        self.label.pack(pady=20)

        self.chat_box = scrolledtext.ScrolledText(master, width=80, height=20, font=('Arial', 14))
        self.chat_box.pack(pady=20)
        self.chat_box.configure(state=tk.DISABLED)

        self.user_input = scrolledtext.ScrolledText(master, width=80, height=4, font=('Arial', 14))
        self.user_input.pack(pady=20)
        self.master.bind("<Return>", self.send_message)

        self.curriculum = [
            "Introduction to Python",
            "Python Basics: Variables, Data Types, and I/O",
            "Control Structures: If statements, loops, and more",
            "Python Functions: Definition, Calling, and Scope",
            "Python Lists, Dictionaries, and Data Structures",
            "Python OOP: Classes, Objects, and Inheritance",
            "File Handling in Python",
            "Python Modules and Libraries",
            "Error Handling: Try, Except, Finally",
            "Advanced Topics: List Comprehensions, Lambda Functions",
            "Python and Databases: SQLite, MySQL",
            "Web Scraping with Python: Beautiful Soup, Requests",
            "Web Development with Flask",
            "Python for Data Science: NumPy, Pandas",
            "Visualization with Python: Matplotlib, Seaborn"
        ]

        self.current_topic = self.load_progress()

        self.introduce_topic()

    def introduce_topic(self):
        topic_intro = {
            "Introduction to Python": "Let's start with the basics. Python is a high-level, interpreted programming language. Do you have Python installed?",
            "Python Basics: Variables, Data Types, and I/O": "Now that we're familiar with Python, let's dive into variables, data types, and input/output. Do you know what a variable is?",
            "Control Structures: If statements, loops, and more": "Moving forward, control structures dictate the flow of your program. Let's begin with if statements. Do you know what an if statement is?",
        }
        self.update_chat("Tutor", topic_intro[self.curriculum[self.current_topic]])

    def send_message(self, event=None):
        message = self.user_input.get("1.0", tk.END).strip()
        self.user_input.delete("1.0", tk.END)
        if message:
            self.update_chat("User", message)
            response = self.ask_gpt(message)
            self.update_chat("Tutor", response)

    def update_chat(self, sender, message):
        self.chat_box.configure(state=tk.NORMAL)
        self.chat_box.insert(tk.END, f"{sender}: {message}\n")
        self.chat_box.configure(state=tk.DISABLED)
        self.chat_box.yview(tk.END)

    def ask_gpt(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert Python tutor. You are the primary source of knowledge and should provide detailed, direct teaching without referring to external sources. The student is relying on you for a comprehensive understanding of Python."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()

    def load_progress(self):
        if Path("progress.txt").exists():
            with open("progress.txt", "r") as f:
                try:
                    return int(f.read().strip())
                except ValueError:
                    return 0
        else:
            return 0

    def save_progress(self):
        with open("progress.txt", "w") as f:
            f.write(str(self.current_topic))

root = tk.Tk()
app = PythonTutor(master=root)
root.mainloop()
