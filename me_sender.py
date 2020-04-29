# Main program used by the sender to receive question and send encrypted answer

from pathlib import Path
import me_sender_server_communicator
import me_sender_interface
import json


def main():
    # Read configuration file
    config_info_path = Path.cwd().joinpath("config_file")
    with open(config_info_path) as config:
        config_info = json.load(config)
        alphabet_size = config_info["ALPHABET_SIZE"]
        url_question_get = config_info["QUESTION_REQUEST_URL"]
        url_answer_send = config_info["QUESTION_SEND_URL"]

    # Request question
    communicator = me_sender_server_communicator.Communicator()
    communicator.request_question(url_question_get)
    interface = me_sender_interface.UserInterface(communicator.question)
    # Request sender id
    interface.request_senderid()

    # Show general information to the sender
    interface.show_general_info()

    # Show the list of random positions to the sender and the encrypt alphabet
    # for each letter
    for num_letter in range(communicator.question.num_answer_letters):
        interface.show_position_list(num_letter)
        interface.show_icon_groups(alphabet_size, num_letter)

    # Read the encrypted answer
    interface.read_answer()

    # Send the answer
    communicator.answer = interface.answer
    communicator.senderid = interface.senderid
    communicator.send_answer(url_answer_send)


if __name__ == "__main__":
    main()
