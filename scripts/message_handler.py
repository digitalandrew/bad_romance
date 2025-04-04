import time
import os


def get_file_mtime(filename):
    try:
        return os.path.getmtime(filename)
    except FileNotFoundError:
        return None


def read_file(filename):
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        return "[File not found]"


def main():
    message_dir = "/home/andrew/bad_romance/messages/"
    message_file = message_dir + "scammer_message.txt"
    reply_file = message_dir + "victim_message.txt"
    last_modified = get_file_mtime(message_file)

    print("Message Handler Running")

    while True:
        current_modified = get_file_mtime(message_file)

        if current_modified != last_modified:
            last_modified = current_modified
            print("\n--- New message Received ---")
            content = read_file(message_file)
            print(content)
            reply = input("\nYour reply: ")
            with open(reply_file, "w") as out_file:
                out_file.write(reply)
            print("Reply Sent")

        time.sleep(1)


if __name__ == "__main__":
    main()
