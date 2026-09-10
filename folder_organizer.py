import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

EXTENSIONS = {
    'Зображення': ['.jpg', '.png', '.gif', '.jpeg'],
    'Документи': ['.pdf', '.docx', '.txt', '.xlsx'],
    'Відео_та_Музика': ['.mp4', '.mov', '.mp3', '.wav'],
    'Архіви': ['.zip', '.rar']
}


class FolderOrganizer:

    def __init__(self, window):
        self.window = window
        self.window.title("Мій сортувальик")
        self.window.geometry("500x400")
        self.window.config(bg="#f0f0f0")

        self.selected_path = ""

        self.create_widgets()

    def create_widgets(self):
        tk.Label(
            self.window,
            text="Органайзер папок",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0"
        ).pack(pady=20)

        self.btn_select = tk.Button(
            self.window,
            text="Обрати папку",
            command=self.choose_folder,
            bg="#e1bee7",
            font=("Arial", 12)
        )
        self.btn_select.pack(pady=10)

        self.label_path = tk.Label(
            self.window,
            text="Папка не обрана",
            bg="#f0f0f0",
            fg="gray"
        )
        self.label_path.pack()

        self.log_box = tk.Text(
            self.window,
            height=10,
            width=50,
            font=("Arial", 10)
        )
        self.log_box.pack(pady=20, padx=20)

        self.btn_start = tk.Button(
            self.window,
            text="Розсортувати",
            command=self.start_sorting,
            state="disabled",
            bg="#c5cae9",
            font=("Arial", 12, "bold")
        )
        self.btn_start.pack(pady=10)

    def log(self, message):
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)

    def choose_folder(self):
        folder = filedialog.askdirectory()

        if folder:
            self.selected_path = folder
            self.label_path.config(text=f"Обрана папка: {folder}", fg="black")
            self.btn_start.config(state="normal")
            self.log(f"Обрана папка: {os.path.basename(folder)}")

    def start_sorting(self):
        if not self.selected_path:
            messagebox.showwarning("Увага", "Спочатку оберіть папку.")
            return

        count = 0
        self.log("Починаю сортування...")

        try:
            for filename in os.listdir(self.selected_path):
                file_path = os.path.join(self.selected_path, filename)

                if os.path.isdir(file_path):
                    continue

                ext = os.path.splitext(filename)[1].lower()
                moved = False

                for category, exts in EXTENSIONS.items():
                    if ext in exts:
                        dest_folder = os.path.join(self.selected_path, category)
                        os.makedirs(dest_folder, exist_ok=True)

                        target_path = os.path.join(dest_folder, filename)
                        if os.path.exists(target_path):
                            base_name, suffix = os.path.splitext(filename)
                            index = 1
                            while True:
                                candidate = os.path.join(dest_folder, f"{base_name}_{index}{suffix}")
                                if not os.path.exists(candidate):
                                    target_path = candidate
                                    break
                                index += 1

                        shutil.move(file_path, target_path)
                        self.log(f"{filename} -> {category}")
                        count += 1
                        moved = True
                        break

                if not moved and ext:
                    other_folder = os.path.join(self.selected_path, "Інше")
                    os.makedirs(other_folder, exist_ok=True)

                    target_path = os.path.join(other_folder, filename)
                    if os.path.exists(target_path):
                        base_name, suffix = os.path.splitext(filename)
                        index = 1
                        while True:
                            candidate = os.path.join(other_folder, f"{base_name}_{index}{suffix}")
                            if not os.path.exists(candidate):
                                target_path = candidate
                                break
                            index += 1

                    shutil.move(file_path, target_path)
                    self.log(f"{filename} -> Інше")
                    count += 1

            self.log(f"Завершено! Оброблено файлів: {count}")
            messagebox.showinfo("Успіх!", f"Готово! Переміщено файлів: {count}")

        except Exception as error:
            messagebox.showerror("Ой!", f"Сталася помилка: {error}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FolderOrganizer(root)
    root.mainloop()
