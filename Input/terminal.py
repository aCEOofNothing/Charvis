from shared import input_queue

def terminal_input():
    while True:
        text = input("> ")
        input_queue.put(text)