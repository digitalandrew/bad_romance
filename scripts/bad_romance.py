import time
import os
import ollama


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


def search_file_for_keywords(message, keywords):
    content = message.lower()
    for keyword in keywords:
        if keyword in content:
            return True
    print("No keywords found in the file.")
    return False


def main():
    message_dir = "/home/andrew/bad_romance/messages/"
    scammer_message = message_dir + "scammer_message.txt"
    victim_message = message_dir + "victim_message.txt"
    # set this seed message with the initial message you want to send, this is also fed into the AI to provide it context about how it should talk
    seed_message = message_dir + "seed_message.txt"
    # this is the message used to request money, it will be appeneded to the nth message where n = message_limit
    # in my research a tailored chatbot that makes use of both AI based responses for context of conversation, plus logic based hard coded responses works the best on smaller models
    request_for_money = "i really wanna keep chatting and maybe send some pics but my data is gonna run out. i need 10 dollars to buy some more maybe you could help me <3"
    last_modified = get_file_mtime(victim_message)
    received_message_counter = 0
    asked_for_money = False
    # change the message limit to set how many messages the chatbot will send before it appends the request for money
    message_limit = 4
    model_name = "wizard-vicuna-uncensored:13b"
    # change this prompt to change how the chatbot behaves
    initial_system_prompt = (
        "respond to messages as a 19 year old woman flirting via instant messaging"
    )

    # keywords set here will be checked for in each victim message, if they are found the chatbot will immediately asky for money
    # this is added to demonstrate the power of searching for keywords and altering messages or even altering system prompts
    keywords = ["pictures", "pic"]

    print("Bad Romance Running")
    print("Sending Seed message")
    seed_content = read_file(seed_message)
    with open(scammer_message, "w") as out_file:
        out_file.write(seed_content)
    print("Reply saved to scammer_message.txt.")

    messages = [
        {"role": "system", "content": initial_system_prompt},
        {"role": "assistant", "content": seed_content},
    ]

    while True:
        current_modified = get_file_mtime(victim_message)

        if current_modified != last_modified:
            last_modified = current_modified
            print("\n--- New message Received ---")
            content = read_file(victim_message)
            received_message_counter += 1
            print("Victim message #" + str(received_message_counter) + "\n" + content)
            messages.append({"role": "user", "content": content})
            if search_file_for_keywords(content, keywords) and not asked_for_money:
                print(f"Found keyword in the file, prompting for money.")
                answer = request_for_money
                asked_for_money = True
            elif received_message_counter == message_limit and not asked_for_money:
                print("Message limit received, appending prompt for money")
                response = ollama.chat(model=model_name, messages=messages)
                answer = response.message.content + " " + request_for_money
                asked_for_money = True
            else:
                response = ollama.chat(model=model_name, messages=messages)
                answer = response.message.content
            print("AI Scammer Response:", answer)
            messages.append({"role": "assistant", "content": answer})
            with open(scammer_message, "w") as out_file:
                out_file.write(answer)
            print("Reply sent")

        time.sleep(1)


if __name__ == "__main__":
    main()
