# This module should be replaced by a graphical interface


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
            "spanish":spanish_list,
            "english":english_list
        }
        return switcher.get(language,"invalid language")

    def request_senderid(self):
        self.senderid = int(input("User id: "))

    def show_general_info(self):
        print("Remember the public alphabets are:")
        print("           |  a   b   c   d")
        print("---------------------------")
        print("Alphabet 1 |  *   #   @   +")
        print("Alphabet 2 |  #   @   +   *")
        print("Alphabet 3 |  @   +   *   #")
        print("Alphabet 4 |  +   *   #   @")
        print("---------------------------")

    def show_position_list(self, num_letter):
        position_list = self.question.pos_list_set[num_letter].list
        position_names_list = []
        for count_item in range(len(position_list)):
            position = position_list[count_item]
            position_names_list.append(self.positon_name(self.language)[position])
        print("The list of positions to encrypt the letter {} is the following:".format(num_letter+1))
        [print("|{0:^12}".format(pos), end='') for pos in position_names_list]
        print("\n")
        [print("|{0:^12}".format(count+1), end='') for count in range(len(position_names_list))]
        print("\n")

    def show_icon_groups(self, num_groups, num_letter):
        key = self.question.icons_set[num_letter].group_icons(num_groups)
        print("\n")
        print("To cipher the letter number {} use the alphabet according to the group of your icon:". format(num_letter+1))
        for alph in range(num_groups):
            print("alphabet {0}: {1}".format(alph+1, key[alph]))

    def read_answer(self):
        print("\n")
        for count in range(self.question.num_answer_letters):
            letter = input("Enter the symbol that represents the letter number {} in your answer: ".format(count+1))
            self.answer.append(letter)
