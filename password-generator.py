import tkinter as tk
from tkinter import filedialog, messagebox
import random
import string
from datetime import datetime

class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Генератор паролей")

        # Интерфейс
        self._create_widgets()

    def _create_widgets(self):
        tk.Label(self.master, text="Длина пароля (не менее 12 символов):").pack(pady=5)
        self.entry_length = tk.Entry(self.master)
        self.entry_length.pack(pady=5)

        tk.Label(self.master, text="Количество паролей:").pack(pady=5)
        self.entry_count = tk.Entry(self.master)
        self.entry_count.pack(pady=5)

        generate_button = tk.Button(self.master, text="Сгенерировать пароли", command=self.generate_passwords)
        generate_button.pack(pady=10)

    def generate_passwords(self):
        try:
            length = int(self.entry_length.get())
            if length < 12:
                raise ValueError("Минимальная длина пароля — 12 символов.")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число для длины пароля (не менее 12).")
            return

        try:
            count = int(self.entry_count.get())
            if count < 1:
                raise ValueError("Количество паролей должно быть положительным.")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число для количества паролей.")
            return

        passwords = [
            self._generate_password(length) + "\n" + '*' * 20
            for _ in range(count)
        ]
        self.save_to_file(passwords)

    @staticmethod
    def _generate_password(length):
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choices(chars, k=length))

    def save_to_file(self, passwords):
        current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = f"PASS_{current_time}.txt"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            initialfile=filename
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write("\n\n".join(passwords))
                messagebox.showinfo("Сохранено", f"Пароли сохранены в файле:\n{file_path}")
            except IOError as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
