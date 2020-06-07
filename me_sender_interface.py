# This module should be replaced by a graphical interface

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json


class UserInterface:
    def __init__(self, question):
        self.language = "english"
        self.question = question
        self.senderid = 0
        self.answer = []

    def positon_name(self, language):
        spanish_list = ["sala", "comedor", "cocina", "baño", "alcoba"]
        english_list = ["living room", "dinning room", "kitchen", "bathroom", "bedroom"]

        switcher = {
            "spanish": spanish_list,
            "english": english_list
        }
        return switcher.get(language, "invalid language")

    def request_senderid(self):
        self.senderid = int(input("User id: "))

    def find_icons(self, icon_index):
        # Return a list with the images from the images/icons folder according to the icon_index set
        names_path = Path.cwd().joinpath("images", "icons", "icons_names")
        name_list = ["n"]*len(icon_index)
        with open(names_path) as names:
            line = 0
            for name in names:
                if line in icon_index:
                    name_list[icon_index.index(line)] = name.strip()
                line += 1
        icons_images = []
        for name in name_list:
            image_path = Path.cwd().joinpath("images", "icons", name)
            icons_images.append(Image.open(image_path))
        return icons_images

    def draw_table(self, corner, backgrnd_img, box_dimension, rows, columns, box_color=(255, 255, 255), line_color=(0, 0, 0)):
        # Draw table and return X positions and Y positions of the cell's centers
        box_corners = (corner[0], corner[1], corner[0]+box_dimension[0], corner[1]+box_dimension[1])
        h_lines_start_points = []
        h_lines_stop_points = []
        v_lines_start_points = []
        v_lines_stop_points = []
        y_point = box_corners[1]
        y_center_cell = [y_point + box_dimension[1]//(2*rows)]
        for h_point in range(rows - 1):
            y_point = y_point + box_dimension[1]//rows
            h_lines_start_points.append((box_corners[0], y_point))
            h_lines_stop_points.append((box_corners[2], y_point))
            y_center_cell.append(y_point + box_dimension[1]//(2 * rows))
        x_point = box_corners[0]
        x_center_cell = [x_point + box_dimension[0]//(2*columns)]
        for v_point in range(columns - 1):
            x_point = x_point + box_dimension[0]//columns
            v_lines_start_points.append((x_point, box_corners[1]))
            v_lines_stop_points.append((x_point, box_corners[3]))
            x_center_cell.append(x_point + box_dimension[0]//(2*columns))
        brush = ImageDraw.Draw(backgrnd_img)
        brush.rectangle(box_corners, fill=box_color, outline=line_color)
        for h_line in range(rows - 1):
            brush.line((h_lines_start_points[h_line], h_lines_stop_points[h_line]), fill=line_color)
        for v_line in range(columns - 1):
            brush.line((v_lines_start_points[v_line], v_lines_stop_points[v_line]), fill=line_color)
        return x_center_cell, y_center_cell

    def show_general_info(self, general_info):
        img_width = 600    # Background of the icon list
        img_height = 500   # Background of the icon list
        alph_table_width = 150    # Table with the public alphabet
        alph_table_height = 150   # Table with the public alphabet
        # Read alphabet
        alphabet_path = Path.cwd().joinpath("public_alphabet")
        with open(alphabet_path) as alphabet:
            public_alphabet = json.load(alphabet)

        # Table headers
        col_header = public_alphabet["letters"]
        alph = public_alphabet["alphabets"]
        row_header = []
        for line in range(len(alph)):
            row_header.append("Alphabet {}".format(line + 1))
        intro_img = Image.new(mode="RGBA", size=(img_width, img_height), color=(255, 255, 255))

        # Draw table with alphabet
        table_corner = (img_width/2 - alph_table_width, img_height - alph_table_height - 10)
        (xcenter, ycenter) = self.draw_table(table_corner, intro_img, (alph_table_width, alph_table_height), 4, 4)
        brush = ImageDraw.Draw(intro_img)
        font_table = ImageFont.truetype("arial.ttf", size=12)
        brush.text((table_corner[0], table_corner[1]-30), "Remember the public alphabets are:", font=font_table, fill=(0, 0, 0), align="left")
        for xpos, col in zip(xcenter, range(len(xcenter))):
            brush.text((xpos, table_corner[1]-15), col_header[col], font=font_table, fill=(0, 0, 0), align="center")
        for ypos, row in zip(ycenter, range(len(ycenter))):
            brush.text((table_corner[0] - 60, ypos), row_header[row], font=font_table, fill=(0, 0, 0), align="left")
        for xpos, col in zip(xcenter, range(len(xcenter))):
            for ypos, row in zip(ycenter, range(len(ycenter))):
                brush.text((xpos, ypos), alph[row][col], font=font_table, fill=(0, 0, 0), align="center")
        # Draw question introduction
        font_intro = ImageFont.truetype("arial.ttf", size=15)
        brush.text((10, 10), general_info, font=font_intro, fill=(0, 0, 0), align="left")

        intro_img.show()

        print(general_info)
        print("Remember the public alphabets are:")
        print("           |  a   b   c   d")
        print("---------------------------")
        print("Alphabet 1 |  *   #   @   +")
        print("Alphabet 2 |  #   @   +   *")
        print("Alphabet 3 |  @   +   *   #")
        print("Alphabet 4 |  +   *   #   @")
        print("---------------------------")

    def draw_position_list(self, num_letter):
        # Draw the list with the positions to show to the user

        position_list = self.question.pos_list_set[num_letter].list
        position_names_list = []
        for count_item in range(len(position_list)):
            position = position_list[count_item]
            position_names_list.append(self.positon_name(self.language)[position])
        # Draw position table
        img_width = 900  # Background of the icon list
        img_height = 150  # Background of the icon list
        pos_table_width = 880  # Positions table
        pos_table_height = 50  # Positions table
        pos_list_img = Image.new(mode="RGBA", size=(img_width, img_height), color=(255, 255, 255))
        brush = ImageDraw.Draw(pos_list_img)
        font = ImageFont.truetype("arial.ttf", size=12)
        cell_width = pos_table_width//10
        cell_num = 1
        cols = len(position_list)
        ycorner = 10
        while cols > 10:
            (xcenter, ycenter) = self.draw_table((img_width//2 - pos_table_width//2, ycorner), pos_list_img,
                                                 (cell_width*10, pos_table_height), 2, 10)
            for x in xcenter:
                brush.text((x - cell_width//2 + 2, ycenter[0]), position_names_list[cell_num - 1], font=font, fill=(0, 0, 0),
                           align="left")
                brush.text((x, ycenter[1]), "{}".format(cell_num), font=font, fill=(0, 0, 0), align="left")
                cell_num += 1
            ycorner += pos_table_height + 5
            cols -= 10
        (xcenter, ycenter) = self.draw_table((img_width//2 - pos_table_width//2, ycorner), pos_list_img,
                                             (cell_width*cols, pos_table_height), 2, cols)
        for x in xcenter:
            brush.text((x - cell_width//2 + 2, ycenter[0]), position_names_list[cell_num - 1], font=font, fill=(0, 0, 0),
                       align="left")
            brush.text((x, ycenter[1]), "{}".format(cell_num), font=font, fill=(0, 0, 0), align="left")
            cell_num += 1

        file_name = "pos_list_{}.png".format(num_letter)
        pos_list_img.save(file_name)


        print("The list of positions to encrypt the letter {} is the following:".format(num_letter+1))
        [print("|{0:^12}".format(pos), end='') for pos in position_names_list]
        print("\n")
        [print("|{0:^12}".format(count+1), end='') for count in range(len(position_names_list))]
        print("\n")

    def draw_icon_groups(self, num_groups, num_letter):
        # Draw the icons classified in group

        # Classify the icons in groups
        key = self.question.icons_set[num_letter].group_icons(num_groups)

        img_width = 900  # Background of the icon list
        img_height = 950  # Background of the icon list
        icons_table_width = 880  # Icons area
        icons_table_height = 880  # Icons area
        icons_bckground = Image.new(mode="RGBA", size=(img_width, img_height), color=(255, 255, 255))
        font = ImageFont.truetype("arial.ttf", size=20)
        cell_width = icons_table_width//10
        cell_height = icons_table_height//10
        # Find the images for the question icons
        icons_img = []
        for icons_group in key:
            icons_img.append(self.find_icons(icons_group))

        # Resize if required
        my_icons_list = []
        for group in range(len(key)):
            my_icons_list.append([])
            for icon_img in icons_img[group]:
                org_width = icon_img.size[0]
                org_height = icon_img.size[1]
                icon_add = icon_img
                if org_width > cell_width:
                    new_width = cell_width
                    new_height = ((cell_width) * org_height) // org_width
                    icon_add = icon_img.resize((new_width, new_height))
                if org_height > cell_height:
                    new_height = cell_height
                    new_width = ((cell_height) * org_width) // org_height
                    icon_add = icon_img.resize((new_width, new_height))
                my_icons_list[group].append(icon_add)

        # Draw icons
        cell_index = 0
        cols = len(key)*len(key[0])
        ycorner = 10
        while cols > 10:
            (xcenter, ycenter) = self.draw_table((img_width // 2 - icons_table_width // 2, ycorner), icons_bckground,
                                                 (cell_width * 10, cell_height), 1, 10)
            for x in xcenter:
                new_icon = my_icons_list[cell_index % num_groups][cell_index // num_groups]
                alph = str(cell_index % num_groups + 1)
                brush = ImageDraw.Draw(new_icon)
                brush.ellipse((new_icon.size[0]-font.getsize(alph)[0], 0, new_icon.size[0], font.getsize(alph)[1]),
                              fill=(255, 255, 0))
                brush.text((new_icon.size[0]-font.getsize(alph)[0], 0), alph, font=font, fill=(0, 0, 0), align="center")
                icons_bckground.paste(new_icon, (x - new_icon.size[0]//2, ycenter[0] - new_icon.size[1]//2))
                cell_index += 1
            ycorner += cell_height + 5
            cols -= 10
        (xcenter, ycenter) = self.draw_table((img_width//2 - icons_table_width //2, ycorner), icons_bckground,
                                             (cell_width*cols, cell_height), 1, cols)
        for x in xcenter:
            new_icon = my_icons_list[cell_index % num_groups][cell_index // num_groups]
            alph = str(cell_index % num_groups + 1)
            brush = ImageDraw.Draw(new_icon)
            brush.ellipse((new_icon.size[0]-font.getsize(alph)[0], 0, new_icon.size[0], font.getsize(alph)[1]),
                          fill=(255, 255, 0))
            brush.text((new_icon.size[0]-font.getsize(alph)[0], 0), alph, font=font, fill=(0, 0, 0), align="center")
            icons_bckground.paste(new_icon, (x - new_icon.size[0] // 2, ycenter[0] - new_icon.size[1] // 2))
            cell_index += 1

        file_name = "icons_key_{}.png".format(num_letter)
        icons_bckground.save(file_name)

        print("\n")
        print("To cipher the letter number {} use the alphabet according to the group of your icon:". format(num_letter+1))
        for alph in range(num_groups):
            print("alphabet {0}: {1}".format(alph+1, key[alph]))

    def show_icon_position(self, num_letter):
        # Show the positions and cell for each letter
        icons = Image.open("icons_key_{}.png".format(num_letter))
        positions = Image.open("pos_list_{}.png".format(num_letter))
        font = ImageFont.truetype("arial.ttf", size=20)
        title = "Letter {}, find the alphabet according to the following:".format(num_letter + 1)
        bckground_width = max(icons.size[0], positions.size[0])
        bckground_height = icons.size[1] + positions.size[1] + font.getsize(title)[1] + 10
        background = Image.new(mode="RGBA", size=(bckground_width, bckground_height), color=(255, 255, 255))
        brush = ImageDraw.Draw(background)
        brush.text((bckground_width//2 - font.getsize(title)[0]//2, 5), title, font=font, fill=(0, 0, 0), align="center")
        background.paste(positions, (bckground_width//2 - positions.size[0]//2, font.getsize(title)[1] + 5))
        background.paste(icons, (bckground_width // 2 - icons.size[0]//2, font.getsize(title)[1] + 5 + positions.size[1]))
        background.show()

    def read_answer(self):
        print("\n")
        for count in range(self.question.num_answer_letters):
            letter = input("Enter the symbol that represents the letter number {} in your answer: ".format(count+1))
            self.answer.append(letter)
