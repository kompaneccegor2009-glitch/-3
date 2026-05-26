import tkinter as tk
from tkinter import messagebox, Listbox
import requests
import json
import os

# Файл для хранения избранных пользователей
favorites_file = 'favorites.json'

def load_favorites():
    """Загрузка избранных пользователей из файла JSON."""
    if os.path.exists(favorites_file):
        with open(favorites_file, 'r') as f:
            return json.load(f)
    return []

# Сохраняем избранных пользователей в файл JSON
def save_favorites(favorites):
    with open(favorites_file, 'w') as f:
        json.dump(favorites, f)

# Поиск пользователя по имени
def search_user():
    username = entry.get().strip()
    if not username:
        messagebox.showerror("Ошибка", "Поле поиска не должно быть пустым.")
        return
    
    url = f'https://api.github.com/users/{username}'
    response = requests.get(url)
    
    if response.status_code == 200:
        user = response.json()
        listbox.delete(0, tk.END)  # Очищаем список перед добавлением
        listbox.insert(tk.END, f'{user["login"]} - {user["html_url"]}')
    else:
        messagebox.showerror("Ошибка", "Пользователь не найден.")

# Добавляем пользователя в избранное
def add_to_favorites():
    selected = listbox.curselection()
    if not selected:
        messagebox.showinfo("Информация", "Выберите пользователя для добавления в избранное.")
        return
    
    user_info = listbox.get(selected)
    username = user_info.split(' - ')[0]  # Извлекаем имя пользователя

    # Загружаем существующие избранные пользователи и добавляем нового
    favorites = load_favorites()
    if username not in favorites:
        favorites.append(username)
        save_favorites(favorites)
        messagebox.showinfo("Успех", f"{username} добавлен в избранные!")
    else:
        messagebox.showinfo("Информация", f"{username} уже в избранных.")

# Создание GUI
root = tk.Tk()
root.title("GitHub User Finder")

entry = tk.Entry(root, width=50)
entry.pack(pady=20)

search_button = tk.Button(root, text="Поиск", command=search_user)
search_button.pack(pady=10)

listbox = Listbox(root, width=50)
listbox.pack(pady=20)

favorites_button = tk.Button(root, text="Добавить в Избранное", command=add_to_favorites)
favorites_button.pack(pady=10)

root.mainloop()