import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Generator")
        self.master.geometry("400x300")
        self.master.config(bg="#2C3E50")

        self.label_font = ("Helvetica", 12, "bold")
        self.button_font = ("Helvetica", 10, "bold")

        self.setup_widgets()

    def setup_widgets(self):
        tk.Label(self.master, text="Password Length:", font=self.label_font, bg="#2C3E50", fg="white").grid(row=0, column=0, padx=20, pady=15, sticky="w")
        self.length_entry = tk.Entry(self.master, font=self.label_font)
        self.length_entry.grid(row=0, column=1, padx=20, pady=15, sticky="w")

        self.letters_var = tk.IntVar()
        tk.Checkbutton(self.master, text="Include Letters", variable=self.letters_var, font=self.label_font, bg="#2C3E50", fg="white", selectcolor="#2C3E50").grid(row=1, column=0, padx=20, pady=10, columnspan=2, sticky="w")

        self.numbers_var = tk.IntVar()
        tk.Checkbutton(self.master, text="Include Numbers", variable=self.numbers_var, font=self.label_font, bg="#2C3E50", fg="white", selectcolor="#2C3E50").grid(row=2, column=0, padx=20, pady=10, columnspan=2, sticky="w")

        self.symbols_var = tk.IntVar()
        tk.Checkbutton(self.master, text="Include Symbols", variable=self.symbols_var, font=self.label_font, bg="#2C3E50", fg="white", selectcolor="#2C3E50").grid(row=3, column=0, padx=20, pady=10, columnspan=2, sticky="w")

        tk.Button(self.master, text="Generate Password", command=self.generate_password, font=self.button_font, bg="#3498DB", fg="white").grid(row=4, column=0, columnspan=2, pady=(40, 10), padx=20, sticky="w")

        tk.Button(self.master, text="Copy to Clipboard", command=self.copy_to_clipboard, font=self.button_font, bg="#E74C3C", fg="white").grid(row=4, column=1, columnspan=2, pady=(40, 10), padx=20, sticky="e")

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            use_letters = self.letters_var.get() == 1
            use_numbers = self.numbers_var.get() == 1
            use_symbols = self.symbols_var.get() == 1
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the password length.")
            return

        characters = ""
        if use_letters:
            characters += string.ascii_letters
        if use_numbers:
            characters += string.digits
        if use_symbols:
            characters += string.punctuation

        if not characters:
            messagebox.showerror("Error", "Please choose at least one character type.")
            return

        password = ''.join(random.choice(characters) for _ in range(length))
        messagebox.showinfo("Generated Password", f"Your generated password is:\n{password}")

        # Corrected the pyperclip.copy() call
        pyperclip.copy(password)

    def copy_to_clipboard(self):
        password = messagebox.askquestion("Copy to Clipboard", "Do you want to copy the generated password to the clipboard?")
        if password == 'yes':
            # Use the actual password instead of the question string
            pyperclip.copy(self.generated_password)

def main():
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
