import tkinter as tk
from tkinter import *
import pygame

splash_win = Tk()
pygame.init()
sound = pygame.mixer.Sound("C:/Users/likhi/Downloads/audio.wav")
sound.play()

image_file = "welcome.png"
image = tk.PhotoImage(file=image_file)
image_label = tk.Label(splash_win, image=image)
image_label.pack()

splash_win.attributes('-fullscreen', True)

splash_win.geometry("700x700")

splash_win.overrideredirect(True)

def merge():
    splash_win.destroy()

splash_win.after(5000, merge)