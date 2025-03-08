import threading
from time import sleep
import tkinter as tk
from tkinter import messagebox
import pystray
from PIL import Image, ImageDraw

def show_tray_notification(title, message, duration=10):
    def create_image(width, height, color1, color2):
        image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
        dc.rectangle((0, height // 2, width // 2, height), fill=color2)
        return image

    def notify():
        icon = pystray.Icon("tray_icon")
        icon.icon = create_image(64, 64, "black", "white")
        icon.title = title
        icon.message = message
        icon.visible = True
        sleep(duration)
        icon.stop()

    threading.Thread(target=notify).start()

def show_message_box(title, message):
    def show():
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(title, message)

    threading.Thread(target=show).start()
