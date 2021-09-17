import random
from PIL import Image, ImageDraw, ImageOps
from math import sqrt
from os import path


class ImageGenerator:
    def __init__(self, size, filename='new_image.png'):
        self.width = size[0]
        self.height = size[1]
        self.filename = filename
        self.background = Image.new('RGBA', size, (0, 0, 0, 0))
        self.draw_image = ImageDraw.Draw(self.background)
        self.image = None
        self.default_path = path.join('C:\\Users\\User\\PycharmProjects\\proceduralpics', 'pics')
        self.heart_gen = HeartGenerator(size)

    def save_image(self, filename, folder):
        self.image = self.background
        self.image.save(path.join(folder, filename))

    def paste_image(self, image_path, offset=(0, 0), scale=(1, 1), center=False):
        image = Image.open(image_path, 'r')
        image = image.resize((int(image.size[0] * scale[0]), int(image.size[1] * scale[1])))

        if center:
            offset = ((self.background.size[0] - image.size[0]) // 2,
                      (self.background.size[1] - image.size[1]) // 2)

        self.background.paste(image, offset)

    def generate_heart(self):
        outline = random.randint(0, 1)
        filled = random.randint(0, 1)
        lines_filled = random.randint(0, 1)
        stripped = random.randint(0, 1)
        colors_num = random.randint(2, 30)
        gradient = random.randint(0, 1)
        heart = self.heart_gen

        if filled:
            heart.line_width = 1
            heart.color_filled(color=random_color())
        elif stripped:
            heart.line_width = 1
            heart.step = random.randint(20, 250)
            colors = []
            for i in range(colors_num):
                colors.append(random_color())
            if random.randint(0, 1):
                heart.stripped_lines(colors)
            else:
                heart.step = 1
                colors = color_shades(random_color(), random.randint(5, 15), random.randint(-15, -5))
                heart.stripped_center(colors)
        elif gradient:
            if random.randint(0, 1):
                heart.gradient_filled(start_color=random_color(), end_color=random_color())
            else:
                heart.gradient_center(start_color=random_color(), end_color=random_color())
        elif lines_filled:
            color = random_color()
            heart.outline_width = random.randint(2, 15)
            heart.outline_color = color
            heart.line_width = heart.outline_width
            heart.lines_filled(color, step=random.randint(2, 50))
            heart.draw_outline(radius=random.randint(0, 100))
        else:
            heart.color_filled(color=(random.randint(150, 255), 100, 100))
        # if outline:
        #     heart.outline_width = random.randint(3, 25)
        #     heart.outline_color = random_color()
        #     heart.draw_outline(100)

        return heart

    def generate_pattern(self):
        pass


class HeartGenerator:
    def __init__(self, size=(700, 700)):
        self.bg_size = size
        self.image = Image.new('RGBA', size, (0, 0, 0, 0))
        self.draw_image = ImageDraw.Draw(self.image)
        self.heart_width = size[0] // 2
        self.heart_height = size[1] // 2
        self.heart_draw_scale = [0.75, 0.65]
        self.step = 1
        self.line_width = 5
        self.outline_width = 10
        self.outline_color = (0, 0, 0)
        self.offset = [0, 0]
        self.points = []
        self.outline_points = []

    @staticmethod
    def graph_points(var):
        """Returns y coordinates of every x to draw points that represents heart shape mathematically"""
        result = []
        y_1 = var ** (2 / 3) + sqrt(1 - var ** 2)
        if type(y_1) != complex:
            result.append(y_1)
        y_2 = sqrt(abs(var)) - sqrt(1 - var ** 2)
        if type(y_2) != complex:
            result.append(y_2)
        y_3 = (-var) ** (2 / 3) + sqrt(1 - (-var) ** 2)
        if type(y_3) != complex:
            result.append(y_3)
        return result

    @staticmethod
    def create_gradient(start_color, end_color):
        """Creates list of color gradient from start_color to end_color"""
        gradient_colors = []

        r_transition = end_color[0] - start_color[0]
        g_transition = end_color[1] - start_color[1]
        b_transition = end_color[2] - start_color[2]

        r_step = round(r_transition / (abs(r_transition) + 1))
        g_step = round(g_transition / (abs(g_transition) + 1))
        b_step = round(b_transition / (abs(b_transition) + 1))

        for i in range(255):
            red, green, blue = start_color
            if red != end_color[0]:
                red += r_step
            if green != end_color[1]:
                green += g_step
            if blue != end_color[2]:
                blue += b_step
            if red == end_color[0] and green == end_color[1] and blue == end_color[2]:
                break
            gradient_colors.append((red, green, blue))
            start_color = (red, green, blue)

        return gradient_colors

    def create_points(self, mode=None, step=1):
        """Creates points for any purpose, according to function"""

        # Not creating outline points if they were once created - helps performance
        if mode == 'outline' and self.outline_points:
            return

        width, height = self.bg_size
        scale = self.heart_draw_scale

        if mode == 'outline':
            draw_range = [-width * 100, width * 100]
            accuracy = width * 100
        else:
            self.points = []
            draw_range = [-width // 2, width // 2]
            accuracy = width // 2

        for x in range(*draw_range, step):
            x_point = x / accuracy
            if -.001 < x_point < .001:
                continue
            y_points = self.graph_points(x_point)
            for y in y_points:
                rect_x = int(x_point * self.heart_width * scale[0]) + width//2 + self.offset[0]
                rect_y = (y * self.heart_height * scale[1]) + int(height * 0.4) + self.offset[1]
                if mode == 'outline':
                    self.outline_points.append((rect_x, rect_y))
                else:
                    self.points.append((rect_x, rect_y))

    def make_look_right(self):
        self.image = self.image.rotate(180)
        self.image = ImageOps.mirror(self.image)

    def show_me(self):
        self.make_look_right()
        self.image.show()

    def clear(self):
        self.image = Image.new('RGBA', self.bg_size, (0, 0, 0, 0))
        self.draw_image = ImageDraw.Draw(self.image)

    def draw_outline(self, radius=100, outline_width=None, color=None):
        if color is None:
            color = self.outline_color
        if outline_width is None:
            outline_width = self.outline_width
        self.create_points(mode='outline', step=1)
        for position in self.outline_points:
            rect_shape = [
                (int(position[0] - outline_width//2), int(position[1] - outline_width//2)),
                (int(position[0] + outline_width), int(position[1] + outline_width))
            ]

            self.draw_image.rounded_rectangle(
                rect_shape,
                radius=radius,
                fill=color
            )

    def color_filled(self, color, width=None):
        if width is None:
            width = self.line_width
        self.create_points()
        length = len(self.points)
        for i in range(length - 1):
            self.draw_image.line(self.points[i:i+2], fill=color, width=width)

    def stripped_lines(self, colors: list, step=None):
        if step is None:
            step = self.step

        self.create_points()
        length = len(self.points)
        color_counter = 0
        for i in range(0, length + step - 1, step):
            self.draw_image.line(self.points[i:i + step], fill=colors[color_counter],
                                 width=self.line_width)

            if color_counter < len(colors) - 1:
                color_counter += 1
            else:
                color_counter = 0

    def stripped_center(self, colors: list, step=None):
        if step is None:
            step = self.step

        length = len(colors)
        color_counter = 0
        for i in range(0, length + step - 1, step):
            self.color_filled(color=colors[color_counter])
            self.heart_draw_scale[0] -= 0.75 / length
            self.heart_draw_scale[1] -= 0.65 / length
            self.offset[1] += 100 / length

            if color_counter < len(colors) - 1:
                color_counter += 1
            else:
                color_counter = 0

        self.heart_draw_scale = [0.75, 0.65]
        self.offset = [0, 0]

    def gradient_filled(self, start_color=None, end_color=None):
        gradient_colors = self.create_gradient(start_color, end_color)
        self.create_points()
        length = len(self.points)
        color_step = int(length / len(gradient_colors)) + 1
        for i in range(0, length, color_step):
            self.draw_image.line(self.points[i:i+color_step], fill=gradient_colors[i//color_step], width=1)

    def gradient_center(self, start_color=None, end_color=None):
        gradient_colors = self.create_gradient(start_color, end_color)
        colors_num = len(gradient_colors)

        for x in gradient_colors:
            self.color_filled(color=x)
            self.heart_draw_scale[0] -= 0.75 / colors_num
            self.heart_draw_scale[1] -= 0.65 / colors_num
            self.offset[1] += 1

        self.heart_draw_scale = [0.75, 0.65]
        self.offset = [0, 0]

    def lines_filled(self, color, step=20, line_width=None):
        if line_width is None:
            line_width = self.line_width
        self.create_points(step=step)
        length = len(self.points)
        for i in range(length - 1):
            self.draw_image.line(self.points[i:i+2], fill=color, width=line_width)


def random_color():
    color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
    return color


def color_shades(color, shade_amount, step):
    shades = []
    main_color = max(color)
    for i in range(shade_amount):
        value_list = []
        for value in color:
            if value != main_color:
                value += step * i
            else:
                value += step * i // 2

            if value < 0:
                value = -value

            value_list.append(value)
        shades.append(tuple(value_list))
    return shades


# -------------------- TESTING ----------------------
if __name__ == '__main__':
    heart1 = HeartGenerator((2000, 2000))
    # for x in range(1, 11):
    #     heart1.line_width = x*10
    #     start_time = time()
    #     heart1.draw_outline()
    #     print(f'Time{x}, line_width = {x*10}: {str(time() - start_time)} seconds')

    heart1.line_width = 10
    heart1.draw_outline()
    heart1.show_me()


