# Bad Romance

I created this basic chatbot to test the feasability of running a romance scam or other social engineering with AI on lightweight computers like a raspberry pi 5. 

This script should be used only as a learning tool or for demonstration. 

## How to get started

First install ollama from the official source [https://ollama.com/download](here)

Next pull down your model of choice to run, right now the chat bot is using chat prompts (system, assistant, user) so you'll need to pick a chat based model. 

I also suggest using an uncensored model or else you'll run into the guard rails of most models. 

If you want to run the one that I'm using you can pull it with:

```bash
ollama pull wizard-vicuna-uncensored
```

## Hardware Requirements

As a general rule at a bare minimum you'll need approximately 1 gb of ram per billion parameters in a model. If you're on a standard raspi 5 with 8gb of ram you'll be limited to 7b models or lower. I'm running mine on one of the new Raspberry Pi 5s with 16gb of RAM. You don't need a raspi though this could also run very well on an old laptop or desktop or your main computer. 

## Running the Script

Since this is a proof of concept script it uses text files to send and read the messages. The message handler takes care of reading messages and passing them to the chat bot. 

First start the message handler:

```bash
python3 message_handler.py
```

Second start the chatbot script:

```bash
python3 bad_romance.py
```

The chatbot script will start with the seed message which is saved in seed_message.txt. In my experimentation I had the best results by writing a seed message myself and giving the AI the context of that message being the first one it sent. This way it can pick up on the tone and formatting you want it to use. 

## Modify parameters

There are many parameters you can modify such as the seed message itself, the initial system prompt of how you want the chatbot to respond, the amount of messages you want the chatbot to send before it tries to ask for money and any keywords that should trigger a specific response. 
