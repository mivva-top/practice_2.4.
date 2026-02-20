import tkinter as tk
from tkinter import messagebox
import urllib.request
import urllib.error
import json
from datetime import datetime
from PIL import Image, ImageTk
import io
import threading


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Погодное приложение")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        # Ваш API ключ
        self.API_KEY = "704100048e419bd65c73aad55c9e0052"

        # Популярные города
        self.popular_cities = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань", "Сочи"]

        # Словарь для перевода погодных условий
        self.weather_translations = {
            "clear sky": "Ясно",
            "few clouds": "Малооблачно",
            "scattered clouds": "Облачно с прояснениями",
            "broken clouds": "Облачно",
            "overcast clouds": "Пасмурно",
            "mist": "Туман",
            "fog": "Туман",
            "haze": "Дымка",
            "rain": "Дождь",
            "light rain": "Небольшой дождь",
            "moderate rain": "Умеренный дождь",
            "heavy rain": "Сильный дождь",
            "thunderstorm": "Гроза",
            "snow": "Снег",
            "light snow": "Небольшой снег"
        }

        # Текущая иконка
        self.current_icon = None

        # Создаем интерфейс
        self.create_widgets()

    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="☀️ Погодное приложение ☀️",
            font=("Arial", 18, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=10)

        # Фрейм для ввода
        input_frame = tk.Frame(self.root, bg="#ecf0f1", relief=tk.RAISED, bd=2)
        input_frame.pack(pady=10, padx=20, fill=tk.X)

        # Поле ввода
        tk.Label(input_frame, text="Введите город:", font=("Arial", 11), bg="#ecf0f1").pack(pady=5)
        self.city_entry = tk.Entry(input_frame, font=("Arial", 12), width=25, justify='center')
        self.city_entry.pack(pady=5, padx=10)
        self.city_entry.bind('<Return>', lambda event: self.get_weather())

        # Кнопка поиска
        search_btn = tk.Button(
            input_frame,
            text="🔍 Узнать погоду",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=5,
            command=self.get_weather
        )
        search_btn.pack(pady=10)

        # Быстрый выбор
        quick_frame = tk.Frame(self.root)
        quick_frame.pack(pady=5)

        tk.Label(quick_frame, text="Быстрый выбор:", font=("Arial", 9)).pack()

        cities_frame = tk.Frame(quick_frame)
        cities_frame.pack()

        for city in self.popular_cities:
            city_btn = tk.Button(
                cities_frame,
                text=city,
                font=("Arial", 8),
                bg="#95a5a6",
                fg="white",
                command=lambda c=city: self.quick_select(c)
            )
            city_btn.pack(side=tk.LEFT, padx=2, pady=5)

        # Фрейм для погоды
        self.weather_frame = tk.Frame(self.root, bg="#bdc3c7", relief=tk.SUNKEN, bd=3)
        self.weather_frame.pack(pady=15, padx=20, fill=tk.BOTH, expand=True)

        # Метка для иконки погоды (PIL)
        self.icon_label = tk.Label(
            self.weather_frame,
            bg="#bdc3c7"
        )
        self.icon_label.pack(pady=10)

        # Город
        self.city_label = tk.Label(
            self.weather_frame,
            text="",
            font=("Arial", 16, "bold"),
            bg="#bdc3c7",
            fg="#2c3e50"
        )
        self.city_label.pack(pady=5)

        # Температура
        self.temp_label = tk.Label(
            self.weather_frame,
            text="",
            font=("Arial", 32, "bold"),
            bg="#bdc3c7",
            fg="#e74c3c"
        )
        self.temp_label.pack(pady=5)

        # Описание
        self.desc_label = tk.Label(
            self.weather_frame,
            text="",
            font=("Arial", 12),
            bg="#bdc3c7",
            fg="#34495e"
        )
        self.desc_label.pack(pady=5)

        # Дополнительная информация
        info_frame = tk.Frame(self.weather_frame, bg="#bdc3c7")
        info_frame.pack(pady=10)

        # Влажность
        humidity_frame = tk.Frame(info_frame, bg="#bdc3c7")
        humidity_frame.pack(side=tk.LEFT, padx=15)

        tk.Label(humidity_frame, text="💧", font=("Arial", 16), bg="#bdc3c7").pack()
        self.humidity_label = tk.Label(humidity_frame, text="", font=("Arial", 10), bg="#bdc3c7")
        self.humidity_label.pack()

        # Ветер
        wind_frame = tk.Frame(info_frame, bg="#bdc3c7")
        wind_frame.pack(side=tk.LEFT, padx=15)

        tk.Label(wind_frame, text="🌪️", font=("Arial", 16), bg="#bdc3c7").pack()
        self.wind_label = tk.Label(wind_frame, text="", font=("Arial", 10), bg="#bdc3c7")
        self.wind_label.pack()

        # Давление
        pressure_frame = tk.Frame(info_frame, bg="#bdc3c7")
        pressure_frame.pack(side=tk.LEFT, padx=15)

        tk.Label(pressure_frame, text="📊", font=("Arial", 16), bg="#bdc3c7").pack()
        self.pressure_label = tk.Label(pressure_frame, text="", font=("Arial", 10), bg="#bdc3c7")
        self.pressure_label.pack()

        # Статус бар
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе. Введите город...")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 8),
            bg="#ecf0f1"
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def quick_select(self, city):
        """Быстрый выбор города"""
        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, city)
        self.get_weather()

    def get_weather(self):
        """Получение погоды через API"""
        city = self.city_entry.get().strip()

        if not city:
            messagebox.showwarning("Предупреждение", "Введите название города")
            return

        self.status_var.set(f"Загрузка данных для города {city}...")
        self.root.update()

        # Кодируем город для URL
        import urllib.parse
        city_encoded = urllib.parse.quote(city)

        # URL для API запроса (используем HTTPS)
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_encoded}&appid={self.API_KEY}&units=metric&lang=ru"

        try:
            # Создаем запрос
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )

            # Отправляем запрос
            response = urllib.request.urlopen(req, timeout=10)

            # Читаем ответ
            data_json = response.read().decode('utf-8')
            data = json.loads(data_json)

            # Отображаем погоду
            self.display_weather(data)
            self.status_var.set(f"Данные обновлены: {datetime.now().strftime('%H:%M:%S')}")

        except urllib.error.HTTPError as e:
            if e.code == 401:
                messagebox.showerror("Ошибка", "Неверный API ключ")
            elif e.code == 404:
                messagebox.showerror("Ошибка", f"Город '{city}' не найден")
            else:
                messagebox.showerror("Ошибка", f"Ошибка HTTP {e.code}")
            self.status_var.set("Ошибка")

        except urllib.error.URLError:
            messagebox.showerror("Ошибка", "Нет подключения к интернету")
            self.status_var.set("Ошибка подключения")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить данные о погоде: {str(e)}")
            self.status_var.set("Ошибка")

    def display_weather(self, data):
        """Отображение погодных данных"""
        try:
            # Название города
            city_name = data['name']
            country = data['sys']['country']
            self.city_label.config(text=f"{city_name}, {country}")

            # Температура
            temp = round(data['main']['temp'])
            feels_like = round(data['main']['feels_like'])
            self.temp_label.config(text=f"{temp}°C")

            # Погодные условия
            weather_desc = data['weather'][0]['description']
            icon_code = data['weather'][0]['icon']

            # Переводим описание
            translated_desc = self.weather_translations.get(weather_desc.lower(), weather_desc)
            self.desc_label.config(text=f"{translated_desc}\nОщущается как {feels_like}°C")

            # Загружаем иконку
            self.load_weather_icon(icon_code)

            # Влажность
            humidity = data['main']['humidity']
            self.humidity_label.config(text=f"{humidity}%")

            # Ветер
            wind_speed = data['wind']['speed']
            self.wind_label.config(text=f"{wind_speed} м/с")

            # Давление
            pressure = data['main']['pressure']
            self.pressure_label.config(text=f"{pressure} гПа")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось отобразить данные: {str(e)}")

    def load_weather_icon(self, icon_code):
        """Загрузка и отображение иконки погоды с помощью PIL"""
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"

        def download_icon():
            try:
                # Скачиваем иконку
                req = urllib.request.Request(
                    icon_url,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                response = urllib.request.urlopen(req, timeout=5)
                icon_data = response.read()

                # Открываем изображение с помощью PIL
                icon_image = Image.open(io.BytesIO(icon_data))

                # Изменяем размер для отображения
                icon_image = icon_image.resize((100, 100), Image.Resampling.LANCZOS)

                # Конвертируем в PhotoImage
                self.current_icon = ImageTk.PhotoImage(icon_image)

                # Обновляем метку в главном потоке
                self.root.after(0, lambda: self.icon_label.config(image=self.current_icon))

            except Exception as e:
                # Если не удалось загрузить иконку, ничего не делаем
                pass

        # Запускаем загрузку в отдельном потоке
        thread = threading.Thread(target=download_icon)
        thread.daemon = True
        thread.start()


def main():
    root = tk.Tk()
    app = WeatherApp(root)

    def on_closing():
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(f"Ошибка: {e}")
        print("Убедитесь, что установлены необходимые библиотеки:")
        print("pip install Pillow")
        input("Нажмите Enter для выхода...")