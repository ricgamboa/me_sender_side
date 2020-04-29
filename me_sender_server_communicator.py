# This module must be replaced with secure communication between the local client in the sender side
# and the remote server that manages the questions and save the answers

import requests

import me_components


class Communicator:

    def __init__(self):
        self.question = me_components.Question(0, 0)
        self.answer = []
        self.senderid = 0

    def request_question(self, url):
        # This method must be replaced by secure server communication
        # The method reads the question, and save the values
        # to the member variable question changing to the right format

        try:
            response = requests.get(url=url)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        question_res = response.json()
        self.question.id = question_res["question_id"]
        self.question.num_answer_letters = question_res["number_letters"]
        icons_list = question_res["icons_lists"]
        for ic_li in icons_list:
            self.question.append_icon_set(ic_li)
        position_list = question_res["positions_lists"]
        for pos_li in position_list:
            self.question.append_position_list(pos_li)

    def send_answer(self, url):
        # This method must be replaced by secure server communication
        # This method send answer to the server

        answer_send = {"user_id": self.senderid, "answer": self.answer, "question_id": self.question.id}
        try:
            response = requests.post(url=url, json=answer_send)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        print("Status code: ", response.status_code)
