import tkinter as tk
from tkinter import messagebox, ttk
import urllib.request
import urllib.error
import json
from PIL import Image, ImageTk
import io
import threading


class AnimalImagesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Случайные животные")
        self.root.geometry("600x700")
        self.root.resizable(False, False)

        self.cat_api_url = "https://api.thecatapi.com/v1/images/search"
        self.dog_api_url = "https://dog.ceo/api/breeds/image/random"

        self.current_image = None
        self.current_photo = None

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(
            self.root,
            text="🐱 Случайные животные 🐶",
            font=("Arial", 18, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=10)

        button_frame = tk.Frame(self.root, bg="#ecf0f1", relief=tk.RAISED, bd=2)
        button_frame.pack(pady=10, padx=20, fill=tk.X)

        self.cat_button = tk.Button(
            button_frame,
            text=" Получить кота",
            font=("Arial", 14, "bold"),
            bg="#e67e22",
            fg="white",
            padx=30,
            pady=10,
            command=self.get_cat_image,
            cursor="hand2"
        )
        self.cat_button.pack(side=tk.LEFT, padx=20, pady=10, expand=True)

        self.dog_button = tk.Button(
            button_frame,
            text=" Получить собаку",
            font=("Arial", 14, "bold"),
            bg="#3498db",
            fg="white",
            padx=30,
            pady=10,
            command=self.get_dog_image,
            cursor="hand2"
        )
        self.dog_button.pack(side=tk.RIGHT, padx=20, pady=10, expand=True)

        self.image_frame = tk.Frame(self.root, bg="#bdc3c7", relief=tk.SUNKEN, bd=3)
        self.image_frame.pack(pady=15, padx=20, fill=tk.BOTH, expand=True)

        self.image_label = tk.Label(
            self.image_frame,
            text="Нажмите кнопку, чтобы получить изображение",
            font=("Arial", 12),
            bg="#bdc3c7",
            fg="#34495e",
            wraplength=500
        )
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.info_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 10),
            fg="#7f8c8d"
        )
        self.info_label.pack(pady=5)

        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 8),
            bg="#ecf0f1"
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def get_cat_image(self):
        """Получение случайного изображения кота"""
        self.status_var.set("Загрузка кота...")
        self.root.update()

        self.cat_button.config(state=tk.DISABLED)
        self.dog_button.config(state=tk.DISABLED)

        def load_image():
            try:
                req = urllib.request.Request(
                    self.cat_api_url,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                response = urllib.request.urlopen(req, timeout=10)
                data = json.loads(response.read().decode('utf-8'))

                if data and len(data) > 0:
                    image_url = data[0]['url']
                    self.download_and_display_image(image_url, "Кот")
                else:
                    self.root.after(0, lambda: messagebox.showerror("Ошибка", "Не удалось получить изображение кота"))
                    self.root.after(0, lambda: self.status_var.set("Ошибка загрузки"))

            except urllib.error.URLError:
                self.root.after(0, lambda: messagebox.showerror("Ошибка", "Нет подключения к интернету"))
                self.root.after(0, lambda: self.status_var.set("Ошибка подключения"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("Ошибка"))
            finally:
                self.root.after(0, lambda: self.cat_button.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.dog_button.config(state=tk.NORMAL))

        thread = threading.Thread(target=load_image)
        thread.daemon = True
        thread.start()

    def get_dog_image(self):
        """Получение случайного изображения собаки"""
        self.status_var.set("Загрузка собаки...")
        self.root.update()

        self.cat_button.config(state=tk.DISABLED)
        self.dog_button.config(state=tk.DISABLED)

        def load_image():
            try:
                req = urllib.request.Request(
                    self.dog_api_url,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                response = urllib.request.urlopen(req, timeout=10)
                data = json.loads(response.read().decode('utf-8'))

                if data and 'message' in data:
                    image_url = data['message']

                    breed = image_url.split('/')[-2] if '/breeds/' in image_url else "неизвестная порода"
                    self.download_and_display_image(image_url, f"Собака ({breed})")
                else:
                    self.root.after(0, lambda: messagebox.showerror("Ошибка", "Не удалось получить изображение собаки"))
                    self.root.after(0, lambda: self.status_var.set("Ошибка загрузки"))

            except urllib.error.URLError:
                self.root.after(0, lambda: messagebox.showerror("Ошибка", "Нет подключения к интернету"))
                self.root.after(0, lambda: self.status_var.set("Ошибка подключения"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("Ошибка"))
            finally:
                self.root.after(0, lambda: self.cat_button.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.dog_button.config(state=tk.NORMAL))

        thread = threading.Thread(target=load_image)
        thread.daemon = True
        thread.start()

    def download_and_display_image(self, image_url, animal_type):
        """Скачивание и отображение изображения"""
        try:
            req = urllib.request.Request(
                image_url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            response = urllib.request.urlopen(req, timeout=10)
            image_data = response.read()

            image = Image.open(io.BytesIO(image_data))

            max_size = (500, 500)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

            self.current_photo = ImageTk.PhotoImage(image)

            self.image_label.config(
                image=self.current_photo,
                text="",
                bg="#bdc3c7"
            )

            self.info_label.config(
                text=f"{animal_type} | Размер: {image_data.__sizeof__() // 1024} KB"
            )

            self.status_var.set("Изображение загружено")

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {str(e)}"))
            self.status_var.set("Ошибка загрузки изображения")


def main():
    root = tk.Tk()
    app = AnimalImagesApp(root)

    def on_closing():
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    try:
        from PIL import Image, ImageTk

        main()
    except ImportError:
        print("Ошибка: Необходимо установить библиотеку Pillow")
        print("Установите её командой: pip install Pillow")

        input("Нажмите Enter для выхода...")
