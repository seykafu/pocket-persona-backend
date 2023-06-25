import os

from flask import Flask
from flask import request
import openai
from apikey import api_key

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #if api_key != '':
    # Set up the OpenAI API client
        #api_key = api_key
    @app.route("/")
    def index():

        NPC_ONE = "Jack"
        NPC_TWO = "Tiger"

        def npcContent(start_prompt, lastTalker, conversation):
            if lastTalker != "":
                start_prompt = "Respond to what " + lastTalker + " said: " + start_prompt

            if lastTalker == NPC_ONE:
                lastTalker = NPC_TWO
            elif lastTalker == NPC_TWO:
                lastTalker = NPC_ONE

            conversation += start_prompt + "\n"

            response = ""
            if api_key != '':
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=conversation,
                    max_tokens=50,  # Adjust the value as needed
                )

            start_response = response.choices[0].text.strip()
            conversation += start_response + "\n"

            return (start_response, lastTalker, conversation)

        # Set up the OpenAI API client
        if api_key != '':
            openai.api_key = api_key

        # Set up the conversation
        conversation = ""
        lastTalker = NPC_ONE

        # Define the character intros
        jackIntro = "Play the NPC character of Jack Zhang in first person, a UX developer at Expedia who loves solving problems, playing games, and learning about technology. Jack wants to join a start-up one day. He finds Bob, who is hiring for a new start-up. He'd like to propose himself to him."
        tigerIntro = "Play the NPC character of Bob in first person, Bob is a drop out from york university from studying the envrionment. Bob is out for an new adventure in his life in selling pens, but not just any pens. Pen15 on the NFT market.  Bob's speech is high unprofessional with slang and swearing and is crazy where he always has to mentino about cryptokitties every second he can get." 

        # Generate the conversation
        words, lastTalker, conversation = npcContent(jackIntro, "", conversation)
        print(words, lastTalker)
        words, lastTalker, conversation = npcContent(tigerIntro, lastTalker, conversation)
        print(words, lastTalker)

        # Extend the conversation for 5 more iterations
        for _ in range(5):
            words, lastTalker, conversation = npcContent("", lastTalker, conversation)
            print(words, lastTalker)

        # Print the final conversation without the start prompt
        final_conversation = conversation.replace(jackIntro, "").replace(tigerIntro, "").strip()
        conversation_string = "\n".join(conversation_list)

        return conversation_string

    #else:
    #return("The API key isn't working or has hit its limit :/")

    if __name__ == "__main__":
        app.run(host="127.0.0.1", port=8080, debug=True)

    return app
                