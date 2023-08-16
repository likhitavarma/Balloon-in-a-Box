import tkinter as tk
import itertools
import numpy as np
import math
import intro
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import pygame


intro.mainloop()
pygame.mixer.init()
pygame.mixer.music.load("C:/Users/likhi/Downloads/button.mp3")

global box, points, simulate_points, radius_dict

box = []
points = []
volume = []
sphere = []
radius_dict = {}
simulate_points = []
radi = {}
vo = []

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

def get_max_volume(points, box1, box2):
        max_volume = 0

        for n in range(1, len(points) + 1):
            for combo in itertools.combinations(points, n):
                volume1 = place_balloons(box1, box2,combo)
                if volume1 > max_volume:
                    max_volume = volume1
                    simulate_points = list(combo)
            for p in simulate_points:
                if p in radius_dict:
                    vo.append((4 / 3) * math.pi * radius_dict[p] ** 3)

        return max_volume, simulate_points, radius_dict

def place_balloons(box1, box2, points):
    x_min, y_min, z_min = box1
    x_max, y_max, z_max = box2
    total_volume = 0
    radius = []
    for point in set(points):
        x, y, z = point
        if x_min <= x <= x_max and y_min <= y <= y_max and z_min <= z <= z_max:

            dx = min(x - x_min, x_max - x)
            dy = min(y - y_min, y_max - y)
            dz = min(z - z_min, z_max - z)

            r = np.min([dx, dy, dz])
            for point1 in points:
                for r1 in radius:
                    if point != point1:
                        if distance(point1, point) < r + r1:
                            r = 0
            if r != 0:
                radius.append(r)
                radius_dict.update({point1:r})

            total_volume += 4 / 3 * math.pi * r ** 3
    return round(total_volume)


def calculate_volume():
    try:

        pygame.mixer.music.play()
        n = int(entry_num_points.get())
        corner1 = tuple(map(int, entry_corner1.get().split()))
        corner2 = tuple(map(int, entry_corner2.get().split()))
        box_volume = abs(corner1[0] - corner2[0]) * abs(corner1[1] - corner2[1]) * abs(corner1[2] - corner2[2])
        box.append(corner1)
        box.append(corner2)
        bp1 = entry_points.get()[:6]
        point = tuple(map(int, bp1.format().split()))
        points.append(point)
        if n > 1:
            bp2 = entry_points.get()[6:12]
            point = tuple(map(int, bp2.format().split()))
            points.append(point)
        if n > 2:
            bp2 = entry_points.get()[12:18]
            point = tuple(map(int, bp2.format().split()))
            points.append(point)
        if n > 3:
            bp2 = entry_points.get()[18:24]
            point = tuple(map(int, bp2.format().split()))
            points.append(point)
        max_volume, simulate_points, radius_dict = get_max_volume(points, corner1, corner2)
        balloon_volume = place_balloons(corner1, corner2, points)
        unenclosed = box_volume - max_volume
        output_text.set(f"Box: {unenclosed}")
    except Exception as e:
        output_text.set(f"Error: {e}")

def simulation_call2():

    pygame.mixer.music.play()

    class Balloon:
        def __init__(self, canvas):
            self.canvas = canvas
            self.x = 250
            self.y = 250
            self.speed = 5
            self.radius = 0
            self.color = '#FC85FF'
            self.finished_expanding = False

        def expand(self):
            self.radius += 1.5
            if self.radius >= 210:
                self.radius = 210
                self.finished_expanding = True
            self.draw()

        def draw(self):
            self.canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius,
                                    self.y + self.radius, fill=self.color, outline=self.color)

    class Balloon1:
        def __init__(self, canvas):
            self.canvas = canvas
            self.x = 521
            self.y = 521
            self.speed = 5
            self.radius = 0
            self.color = '#B29FFF'
            self.finished_expanding = False

        def expand(self):
            if balloon.finished_expanding:
                self.radius += 1.5
                if self.radius >= 175:
                    self.radius = 175
                    self.finished_expanding = True
                self.draw()

        def draw(self):
            self.canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius,
                                    self.y + self.radius, fill=self.color, outline=self.color)


    root = tk.Tk()
    root.title("Balloons")
    canvas = tk.Canvas(root, width=800, height=800, bg="black", highlightthickness=0)
    canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
    canvas.pack()


    canvas.create_rectangle(40, 40, 752, 752, outline="white")


    balloon = Balloon(canvas)
    balloon2 = Balloon1(canvas)


    def game_loop():

        balloon.expand()
        if balloon.finished_expanding:
            balloon2.expand()
        balloon.draw()
        balloon2.draw()


        root.after(16, game_loop)


    game_loop()


    root.mainloop()

def simulation_call():


        pygame.mixer.music.play()

        max_volume, simulate_points, radius_dict = get_max_volume(points, box[0], box[1])


        x = [box[0][0], box[1][0]]
        y = [box[0][1], box[1][1]]
        z = [box[0][2], box[1][2]]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        verts = np.array([
            [x[0], y[0], z[0]],
            [x[1], y[0], z[0]],
            [x[1], y[0], z[1]],
            [x[0], y[0], z[1]],
            [x[0], y[1], z[0]],
            [x[1], y[1], z[0]],
            [x[1], y[1], z[1]],
            [x[0], y[1], z[1]]
        ])
        faces = np.array([
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [0, 1, 5, 4],
            [2, 3, 7, 6],
            [1, 2, 6, 5],
            [3, 0, 4, 7]
        ])
        poly = Poly3DCollection(verts[faces], alpha=0.5)
        poly.set_facecolor('gainsboro')
        poly.set_edgecolor('black')
        ax.add_collection3d(poly)
        ax.set_xlim([x[0] - 1, x[1] + 1])
        ax.set_ylim([y[0] - 1, y[1] + 1])
        ax.set_zlim([z[0] - 1, z[1] + 1])
        plt.grid(False)
        plt.axis('off')

        for point in simulate_points:
            if point in radius_dict:
                x, y, z = point
                r = radius_dict[point]
                u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
                x1 = r * np.cos(u) * np.sin(v) + x
                y1 = r * np.sin(u) * np.sin(v) + y
                z1 = r * np.cos(v) + z

                for r1 in np.arange(0.1, radius_dict[point], 0.7):
                    u, v = np.mgrid[0:2 * np.pi:100j, 0:np.pi:50j]
                    x1 = x + r1 * np.cos(u) * np.sin(v)
                    y1 = y + r1 * np.sin(u) * np.sin(v)
                    z1 = z + r1 * np.cos(v)
                    ax.plot_surface(x1, y1, z1, color="deeppink")
                    mgr = plt.get_current_fig_manager()
                    mgr.window.state('zoomed')
                    plt.pause(0.05)

        ax.set_xlim3d(box[0][0], box[1][0])
        ax.set_ylim3d(box[0][1], box[1][1])
        ax.set_zlim3d(box[0][2], box[1][2])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()


root = tk.Tk()
root.title("Balloons in a Box")
root.geometry("500x800")


root.wm_attributes('-fullscreen', True)


root.geometry("500x500+100+100")


bg_image = tk.PhotoImage(file="inputbackground.png")


bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


label_num_points = tk.Label(root, text="Number of Points:",bg='#E2E7FF', font=('Showcard Gothic', 30, "bold"),  highlightthickness=0)
entry_num_points = tk.Entry(root, font=('Algerian', 26), justify="center", width=20, bg="white",fg="#FF8373", disabledbackground="#1E6FBA", disabledforeground="yellow",highlightbackground="black", highlightcolor="red", highlightthickness=1, bd=0)
label_corner1 = tk.Label(root, text="Box Corner 1:",bg='#DCEBFF', font=('Showcard Gothic', 30, "bold"))
entry_corner1 = tk.Entry(root, font=('Algerian', 26), justify="center", width=20, bg="white", fg="#FF8373",disabledbackground="#1E6FBA", disabledforeground="yellow", highlightbackground="black",highlightcolor="red", highlightthickness=1, bd=0)
label_corner2 = tk.Label(root, text="Box Corner 2:",bg='#DCEBFF', font=('Showcard Gothic', 30, "bold") )
entry_corner2 = tk.Entry(root, font=('Algerian', 26), justify="center", width=20, bg="white", fg="#FF8373",disabledbackground="#1E6FBA", disabledforeground="yellow", highlightbackground="black",highlightcolor="red", highlightthickness=1, bd=0)
label_points = tk.Label(root, text="Points:",bg='#E5F1FF', font=('Showcard Gothic', 30, "bold") )
entry_points = tk.Entry(root, font=('Algerian', 26), justify="center", width=20, bg="white", fg="#FF8373",disabledbackground="#1E6FBA", disabledforeground="yellow", highlightbackground="black",highlightcolor="red", highlightthickness=1, bd=0)
output_label = tk.Label(root, text="")


submit_button1 = tk.Button(root, text="Calculate", font=('Showcard Gothic', 20),bg='#F9D3FF', command=calculate_volume)
submit_button2 = tk.Button(root, text="3D Stimulate",bg='#FFC2E4', font=('Showcard Gothic', 20), command=simulation_call)
submit_button3 = tk.Button(root, text="2D Stimulate",bg='#BBFFF4',font=('Showcard Gothic', 20), command=simulation_call2)

for i in range(30):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)


label_num_points.grid(row=9, column=9)
entry_num_points.grid(row=9, column=10)
label_corner1.grid(row=10, column=9)
entry_corner1.grid(row=10, column=10)
label_corner2.grid(row=11, column=9)
entry_corner2.grid(row=11, column=10)
label_points.grid(row=12, column=9)
entry_points.grid(row=12, column=10)
submit_button1.grid(row=16, column=10)
submit_button2.grid(row=21, column=11)
submit_button3.grid(row=21, column=9)


output_text = tk.StringVar()
output_text.set("")


output = tk.Label(root, textvariable=output_text,font=("Algerian", 20),bg= "#EBE5FF")
output.grid(row=18, column=10)

root.mainloop()
