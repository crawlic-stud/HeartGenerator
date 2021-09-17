import tkinter.messagebox
from PIL import ImageTk
from PIL_generator_class import *
from tkinter import colorchooser
from tkinter import filedialog
from idlelib.tooltip import Hovertip


class App:
    def __init__(self, title: str, size: tuple[int, int], main_color: str, resizable: tuple[bool, bool]):
        self.running = False
        self.size = size
        self.title = title
        self.main_color = main_color
        self.resizable = resizable

        # ------------------ SETUP -----------------
        self.root = tkinter.Tk()
        self.root['bg'] = self.main_color
        self.root.title(self.title)
        self.root.geometry(str(self.size[0]) + 'x' + str(self.size[1]))
        self.root.resizable(width=self.resizable[0], height=self.resizable[1])

    def run(self):
        if not self.running:
            return
        self.root.mainloop()


class HeartImageApp(App):
    def __init__(self):
        super().__init__('Image generator', (500, 700), main_color='#E3ACA0', resizable=(False, False))
        # ----------------------- FRAMES -------------------------
        self.canvas_frame = tkinter.Frame(self.root, bg='#E38484')
        self.frame_top_right = tkinter.Frame(self.root, bg='#E38484')
        self.frame_top_left = tkinter.Frame(self.root, bg='#E38484')
        self.frame_main = tkinter.Frame(self.root, bg='#E38484')

        # ----------------------- CANVASES -------------------------
        self.canvas = tkinter.Label(self.canvas_frame)
        self.gradient_canvas = tkinter.Label(self.frame_main)
        self.stripped_canvas = tkinter.Label(self.frame_main)

        # ----------------------- BUTTONS -------------------------
        self.save = tkinter.Button(self.frame_top_left, text='Save', fg='white', font=('Arial', 15),
                                   bg='#9B2E4D', width=10, height=10)
        self.clear = tkinter.Button(self.frame_top_left, text='Clear', fg='white', font=('Arial', 15),
                                    bg='#9B2E4D', width=10, height=10)

        self.first_color = tkinter.Button(self.frame_main, bg='black', fg='white', text='1', width=6, height=1, font=('Arial', 15))
        self.second_color = tkinter.Button(self.frame_main, bg='white', text='2', width=6, height=1, font=('Arial', 15))

        self.gradient1 = tkinter.Button(self.frame_main, text='Gradient 1', fg='white', font=('Arial', 15),
                                        bg='#9B2E4D', width=8, height=1)
        self.gradient2 = tkinter.Button(self.frame_main, text='Gradient 2', fg='white', font=('Arial', 15),
                                        bg='#9B2E4D', width=8, height=1)
        self.filled = tkinter.Button(self.frame_main, text='Fill color', fg='white', font=('Arial', 15),
                                     bg='#9B2E4D', width=8, height=1)
        self.lines_filled = tkinter.Button(self.frame_main, text='Fill lines', fg='white', font=('Arial', 15),
                                           bg='#9B2E4D', width=8, height=1)
        self.stripped1 = tkinter.Button(self.frame_main, text='Stripped 1', fg='white', font=('Arial', 15),
                                        bg='#9B2E4D', width=8, height=1)
        self.stripped2 = tkinter.Button(self.frame_main, text='Stripped 2', fg='white', font=('Arial', 15),
                                        bg='#9B2E4D', width=8, height=1)
        self.outline = tkinter.Button(self.frame_main, text='Outline', fg='white', font=('Arial', 15),
                                      bg='#9B2E4D', width=8, height=1)
        self.random_heart = tkinter.Button(self.frame_main, text='Random', fg='white', font=('Arial', 15),
                                           bg='#9B2E4D', width=8, height=1)

        # ----------------------- WIDGETS -------------------------
        self.step_widget = tkinter.Scale(self.frame_main, from_=5, to=50, orient=tkinter.HORIZONTAL, bg='#9B2E4D',
                                         width=12, sliderlength=20, font=('Arial', 10), length=140)
        self.line_width_widget1 = tkinter.Scale(self.frame_main, from_=1, to=100, orient=tkinter.HORIZONTAL, bg='#9B2E4D',
                                                width=12, sliderlength=20, font=('Arial', 10), length=110)
        self.line_width_widget2 = tkinter.Scale(self.frame_main, from_=1, to=100, orient=tkinter.HORIZONTAL, bg='#9B2E4D',
                                                width=12, sliderlength=20, font=('Arial', 10), length=110)
        self.line_step_widget = tkinter.Scale(self.frame_main, from_=2, to=400, orient=tkinter.HORIZONTAL, bg='#9B2E4D',
                                              width=12, sliderlength=20, font=('Arial', 10), length=110)
        self.line_step_widget.set(50)

        # ----------------------- GLOBALS -------------------------
        self.heart = HeartGenerator((2000, 2000))
        self.generator = ImageGenerator((2000, 2000))
        self.color1 = (0, 0, 0)
        self.color2 = (255, 255, 255)

    def pack(self):
        """Place and pack all widgets"""
        self.canvas_frame.place(relx=0.01, rely=0.09, relwidth=0.98, relheight=0.6)
        self.frame_top_right.place(relx=0.5, rely=0.02, relwidth=0.48, relheight=0.05)
        self.frame_top_left.place(relx=0.02, rely=0.02, relwidth=0.48, relheight=0.05)
        self.frame_main.place(rely=0.7, relwidth=1, relheight=0.5)

        self.save.pack(side='left')
        self.clear.pack(side='right')

        self.step_widget.place(x=250, y=45)
        self.line_width_widget1.place(x=105, y=45)
        self.line_width_widget2.place(x=105, y=135)
        self.line_step_widget.place(x=105, y=90)

        self.first_color.place(x=250, y=135)
        self.second_color.place(x=320, y=135)

        self.gradient1.place(x=5, y=0)
        self.gradient2.place(x=395, y=0)
        self.filled.place(x=5, y=45)
        self.lines_filled.place(x=395, y=45)
        self.stripped1.place(x=5, y=90)
        self.stripped2.place(x=395, y=90)
        self.outline.place(x=5, y=135)
        self.random_heart.place(x=395, y=135)

        self.canvas.pack()
        self.gradient_canvas.place(x=105, y=1)
        self.stripped_canvas.place(x=250, y=90)

    def start(self):
        """Start the app"""
        self.update_screen()
        self.update_stripes()
        self.config_commands()
        self.config_tooltips()
        self.pack()
        self.run()

    def convert_(self):
        heart = HeartGenerator((2000, 2000))
        heart.image = self.heart.image
        heart.make_look_right()
        return heart

    def update_screen(self, image=None):
        """Update current image"""
        if image is not None:
            self.heart = image

        heart = self.convert_()

        new_image = ImageTk.PhotoImage(heart.image.resize((500, 500)))
        self.canvas.configure(image=new_image)
        self.canvas.image = new_image

        gradient = self.create_gradient().resize((285, 35))
        new_image = ImageTk.PhotoImage(gradient)
        self.gradient_canvas.configure(image=new_image)
        self.gradient_canvas.image = new_image

    def update_stripes(self, num=None):
        stripes = self.create_strips(strip_width=self.line_step_widget.get()).resize((142, 35))
        new_image = ImageTk.PhotoImage(stripes)
        self.stripped_canvas.configure(image=new_image)
        self.stripped_canvas.image = new_image

    def config_commands(self):
        """Configure widgets"""
        self.gradient1.config(
            command=lambda: (self.heart.gradient_filled(self.color1, self.color2), self.update_screen()))
        self.gradient2.config(
            command=lambda: (self.heart.gradient_center(self.color1, self.color2), self.update_screen()))

        self.first_color.config(command=lambda: (self.change_color(self.first_color), self.update_screen(),
                                                 self.update_stripes()))
        self.second_color.config(command=lambda: (self.change_color(self.second_color), self.update_screen()))

        self.line_step_widget.config(command=self.update_stripes)

        self.clear.config(command=self.clear_canvas)
        self.save.config(command=lambda: (self.save_image()))
        self.filled.config(command=lambda: (self.heart.color_filled(self.color1, self.line_width_widget1.get()), self.update_screen()))
        self.lines_filled.config(command=lambda: (self.heart.lines_filled(
            self.color1, step=self.step_widget.get(), line_width=self.line_width_widget1.get()),
                                                  self.update_screen()))
        self.stripped1.config(command=lambda: (self.heart.stripped_lines(color_shades(self.color1, 10, 10),
                                                                         step=self.line_step_widget.get()),
                                               self.update_screen()))
        self.stripped2.config(command=lambda: (self.heart.stripped_center(color_shades(self.color1, 10, 10), step=1),
                                               self.update_screen()))
        self.outline.config(command=lambda: (self.heart.draw_outline(
            color=self.color1, outline_width=self.line_width_widget2.get()), self.update_screen()))
        self.random_heart.config(command=lambda: (self.heart.clear(), self.update_screen(self.generator.generate_heart())))

    def config_tooltips(self):
        """Configure tooltips for widgets"""
        Hovertip(self.random_heart, 'Creates random heart.')
        Hovertip(self.save, 'Press to save')
        Hovertip(self.clear, 'Erase everything.')
        Hovertip(self.first_color, 'Main color.')
        Hovertip(self.second_color, 'Secondary color.')
        Hovertip(self.gradient1, 'Creates gradient from color 1 to 2.')
        Hovertip(self.gradient2, 'Creates gradient from color 1 to 2\n'
                                 'heading center.')
        Hovertip(self.stripped1, 'Creates stripped image.')
        Hovertip(self.stripped2, 'Creates stripped image\n'
                                 'heading center.')
        Hovertip(self.filled, 'Fill image with color 1.')
        Hovertip(self.lines_filled, 'Fill image with lines.')
        Hovertip(self.outline, 'Creates an outline of color 1.')

        Hovertip(self.line_step_widget, 'Width of strip.')
        Hovertip(self.step_widget, 'Line\' step.')
        Hovertip(self.line_width_widget1, 'Line\'s width')
        Hovertip(self.line_width_widget2, 'Outline width.')

    # ------------------------------------- BUTTON FUNCTIONS --------------------------------------------
    def change_color(self, button):
        color = colorchooser.askcolor()
        if color == (None, None):
            return
        if button == self.first_color:
            self.color1 = color[0]
        elif button == self.second_color:
            self.color2 = color[0]

        button.config(bg=color[1])
        return color[1]

    def clear_canvas(self):
        are_you_sure = tkinter.messagebox.askyesno('', 'Are you sure you want to erase everything?')
        if are_you_sure:
            self.heart.clear()
            self.update_screen()
        else:
            return

    def save_image(self):
        directory = filedialog.asksaveasfile(mode='w', defaultextension='.png', filetypes=[('PNG', '*.png')])
        if directory is None:
            return
        heart = self.convert_()
        heart.image.save(directory.name)

    def create_gradient(self):
        new_gradient = HeartGenerator((300, 300))
        colors = new_gradient.create_gradient(self.color1, self.color2)
        points = create_points(300)
        color_step = int(len(points) / len(colors)) + 1
        for i in range(0, len(points), color_step):
            new_gradient.draw_image.line(points[i:i + color_step], fill=colors[i // color_step])
        return new_gradient.image

    def create_strips(self, strip_width):
        new_strips = HeartGenerator((2000, 350))
        colors = color_shades(self.color1, 10, 10)
        points = create_points(2000)
        length = len(points)
        color_counter = 0
        for i in range(0, length + strip_width - 1, strip_width):
            new_strips.draw_image.line(points[i:i + strip_width], fill=colors[color_counter], width=1)

            if color_counter < len(colors) - 1:
                color_counter += 1
            else:
                color_counter = 0
        return new_strips.image


def create_points(length):
    points = []
    for i in range(length):
        points.append((i, 0))
        points.append((i, length))
    return points


if __name__ == '__main__':
    my_app = HeartImageApp()
    my_app.running = True
    my_app.start()
