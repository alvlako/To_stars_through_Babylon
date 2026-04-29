# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define shibtu_talks = Character("Shibtu")
image Shibtu = "Shibtu.png"

define muranu_talks = Character("Muranu")
image Muranu = "Muranu.png"

define clay_seller_talks = Character("Clay seller")
image clay_seller = "clay_seller.png"

init python:
    import os, subprocess, sys, time, atexit
    CONDA_ENV_ROOT = "/Users/sasha/miniconda3/envs/text_process_env"
    PYTHON_EXE = os.path.join(CONDA_ENV_ROOT, "bin/python" if os.name != "nt" else "python.exe")

    # Full path to the server script (put it next to your Ren'Py project)
    SERVER_SCRIPT = os.path.abspath(os.path.join(config.basedir,
                                                 "..", "nlp_service.py"))

    SERVER_PROC = None

    def start_nlp_server():
        global SERVER_PROC
        if SERVER_PROC is None:
            # Launch the server in its own process group so we can kill it later.
            SERVER_PROC = subprocess.Popen(
                [PYTHON_EXE, SERVER_SCRIPT],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=os.path.dirname(SERVER_SCRIPT)
            )
            # Give the server a moment to bind the port.
            time.sleep(1.0)

    def stop_nlp_server():
        global SERVER_PROC
        if SERVER_PROC is not None:
            SERVER_PROC.terminate()
            SERVER_PROC.wait()
            SERVER_PROC = None

    # Register callbacks so Ren'Py starts the server when the game launches
    # and stops it when the player quits.
    renpy.config.start_callbacks.append(start_nlp_server)
    renpy.config.quit_callbacks.append(stop_nlp_server)

    # Also make sure the server is killed if Python exits unexpectedly.
    atexit.register(stop_nlp_server)

#init python:
#    import json, requests

#    NLP_ENDPOINT = "http://127.0.0.1:8000/reply"

#    def get_nlp_reply(user_text):
#        """
#        Sends *user_text* to the external FastAPI server and returns the reply.
#        If the server is unreachable, returns a safe fallback string.
#        """
#        try:
#            payload = {"text": user_text}
#            # `timeout` prevents the game from hanging forever.
#            r = requests.post(NLP_ENDPOINT, json=payload, timeout=2.0)
#            r.raise_for_status()               # raise on HTTP error
#            data = r.json()
#            return data.get("reply", "Sorry, I didn’t understand.")
#        except Exception as e:
#            # You can log `e` to a file for debugging.
#            renpy.log("NLP service error: {}".format(e))
#            return "Sorry, I’m having trouble answering right now."

# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene babylon_street
    show Shibtu

    # These display lines of dialogue.

    shibtu_talks "My father was a priest-astronomer, Bel-aba-usur, he used to work at Esagila temple in Babylon. The temple paid him with  a piece of land and one silver mina per year. "
    shibtu_talks "Chaldean usurper Marduk-apla-iddina II exiled my father. As other temple personnel, Bel-aba-usur dared to protest against emptying the treasury of Esagila temple for the needs of the growing army and greedy interests of the invader." 
    shibtu_talks "I do not know where my father is. His position at the temple was given to someone else." 
    shibtu_talks "My mother entered the house of another man. But I do not want to stay there."
    shibtu_talks "I want to go and take my father’s job as it is usually done for sons of the temple astronomers. I am a girl, but I am not scared, and I am not worse in computing calendars than any boy!" 


    scene babylon_street
    show Shibtu at left with moveinleft
    
    show Muranu at right with moveinright

    muranu_talks "Shibtu! Where are you going? "

    python:
        answer = renpy.input("say something", length=100)
        answer = answer.strip()
        if not answer:
            silence = True
        else:
            silence = False

    $ bot_reply = get_nlp_reply(answer)
    shibtu_talks "[bot_reply]"

    if silence == True:
        menu:
         "Variants of the answer for Shibtu:"

         "Be polite and talk to the boy":
            shibtu_talks "Muranu, I am going to the market, my mom has sent me to buy a perfume. The lord of our house is going to visit her today"
            muranu_talks "Ah, you are going to the market! I will go with you. From Ur came the best toy-maker, have you heard? They have animal figures on wheels, and new whistles!"
            #Shibtu says to herself: “What a silly little boy! Only games in mind. Now I have to go to the stupid market. The good thing is, it is almost on the way to the temple.”

            jump market

         "Get rid of the annoying boy":
            shibtu_talks "I am going to Esagila temple, do not bother me."
            #jump situation2
    return
    

label market:
    scene babylon_market

    muranu_talks "Do you want to look at the toys?"
    #shibtu_talks ""

    menu:
     "Variants of the answer for Shibtu:"

     "Agree":
         shibtu_talks "Sure"
        #And she told to herself: “when he gets distracted by toys, I will simply disappear”

     "Get rid of the annoying boy":
         #“Oh”, said Shibtu to herself, - “Actually I can not know if they would have clay and stylus for me. Shall they have it, they might consider me unthoughtful and unprepared by coming to them without my essential tools. Indeed, they might not even let me prove my skills. My dad told me that story of how he came to the temple and showed what he was capable of astronomy. He also described in every detail what were the questions but he never told me what he took with him”.
         shibtu_talks "I have to go get perfumes, excuse me."
         jump clay_stall
    return

label clay_stall:
    
    scene clay_stall
    show Shibtu at left with moveinleft
    show clay_seller at right with moveinright

    shibtu_talks "Good morning, my lord. May Marduk keep you in good health!" 
    shibtu_talks "My father sends me to buy some tablets and styluses."
    #Shibtu thought to herself: “That is not completely a lie. Even though my father might most likely be dead by now, I think he would approve of me going to the examination to take over his place”.

    clay_seller_talks "Good morning, young and beautiful lady, let Inanna send you a good husband soon. Why has your most respected father not sent a servant with you?"
    clay_seller_talks "The city these days is full of foreigners and people of unknown origin and intentions. Judging from your appearance, you must have been from a noble family. Be careful, my lady, with your jewelry." 
    clay_seller_talks "Or must you be a future priestess? Then excuse my words about a husband, and pray to Inanna for me. "

    # “This merchant is clearly bored and has nothing to do” - said Shibtu to herself. 
    shibtu_talks "Thank you for your kind words, my lord. I would be glad to buy a bunch of tablets, how much would this sack of tablets cost? And also, how much would 2 styluses cost?"
    clay_seller_talks "All together, my young lady, would cost 3 gerahs. "

    
    return