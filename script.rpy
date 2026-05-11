# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define shibtu_talks = Character("Shibtu")
image Shibtu = "Shibtu.png"

define muranu_talks = Character("Muranu")
image Muranu = "Muranu.png"

define clay_seller_talks = Character("Clay seller")
image clay_seller = "clay_seller.png"

define scribe_1_talks = Character("First scribe")
define scribe_2_talks = Character("Second scribe")
image scribes = "scribes.png"

define ahatabisha_talks = Character("Ahat-abisha")
image Ahatabisha = "Ahatabisha.png"

init python:
    import os, subprocess, sys, time, atexit
    CONDA_ENV_ROOT = "/Users/sasha/miniconda3/envs/text_process_env"
    PYTHON_EXE = os.path.join(CONDA_ENV_ROOT, "bin/python" if os.name != "nt" else "python.exe")

    # Full path to the server script (put it next to your Ren'Py project)
    #SERVER_SCRIPT = os.path.abspath(os.path.join(config.basedir,"..", "nlp_service.py"))
    SERVER_SCRIPT = '/Users/sasha/personal_projects/ancient_near_east_novel/nlp_service.py'

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
    start_nlp_server()
    renpy.config.start_callbacks.append(start_nlp_server)
    renpy.config.quit_callbacks.append(stop_nlp_server)

    # Also make sure the server is killed if Python exits unexpectedly.
    atexit.register(stop_nlp_server)

init python:
    import json, requests

    NLP_ENDPOINT = "http://127.0.0.1:8000/reply"

    def get_nlp_reply(user_text):
        """
#        Sends *user_text* to the external FastAPI server and returns the reply.
#        If the server is unreachable, returns a safe fallback string.
#        """
        try:
            payload = {"text": user_text}
            # `timeout` prevents the game from hanging forever.
            r = requests.post(NLP_ENDPOINT, json=payload, timeout=2.0)
            r.raise_for_status()               # raise on HTTP error
            data = r.json()
            #return data.get("reply", "Sorry, I didn’t understand.")
            reply = data.get("reply", "Sorry, I didn’t understand.")
            jump_loc = data.get("jump_loc")
            return reply, jump_loc
        except Exception as e:
            # You can log `e` to a file for debugging.
            renpy.log("NLP service error: {}".format(e))
            return "Sorry, I’m having trouble answering right now.", None

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

    if silence == False:
        $ bot_reply, jump_loc = get_nlp_reply(answer)
        muranu_talks "[bot_reply]"
        jump expression jump_loc

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
            jump market # change later to another situation
    return
    

label market:
    scene babylon_market

    muranu_talks "Do you want to look at the toys?"
    #shibtu_talks ""

    menu:
     "Variants of the answer for Shibtu:"

     "Agree":
         shibtu_talks "Sure"
         jump clay_stall # change later

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
        
    shibtu_talks "Here are your 3 gerahs, my lord. "
    clay_seller_talks "Here are your tablets and styluses, my young lady. "

    shibtu_talks "Do not they come in the sack, my lord?"
    clay_seller_talks "Oh, my young lady, would you like to have a sack? That would be 3 more gerahs. That is a really good sack, my daughter weaves these for me from the very good material. "
    clay_seller_talks "It takes longer to weave a sack than make a tablet out of clay, you know, my lady? That is why I can not give them away for free."

    menu:
        "Did he do this on purpose? He is clearly trying to fool me. Can I spend 3 more gerahs or should I better save it, who knows what will happen next? What do I answer?"

        "Do not bother, just give the merchant money":
            shibtu_talks "As you say, my lord, here are the other 3 gerahs. "
            jump scribes_arrival

        "Decline a sack, go without it":
            shibtu_talks "Ah then, my lord, I think I can manage without the sack. "
            jump scribes_arrival # change

        "Argue":
            shibtu_talks "How did it happen, my lord, that I now have to pay 3 more gerahs? You told me, all together it costs 3 gerahs. And then, how come it costs so much? Weaving such a sack could not be a day of work. "
            jump scribes_arrival #change

    
    return

label scribes_arrival:
    
    scene clay_stall
    show Shibtu at left with moveinleft
    show clay_seller at right with moveinright

    show scribes at center with moveinleft

    scribe_1_talks "Good morning, my lord, let Marduk prolong your days. I am Nabu-apla-usur, a scribe from Esagila temple. I should ask you what prices you set this year for your pottery. We need to register it together with astronomical observations. "

    clay_seller_talks "Good morning, my lord, let Marduk give you strong health. I would be happy to help my lords but I am afraid that it would cause problems for me to negotiate with my customers. What if I would have to change the price?"

    scribe_1_talks "Worry not, my most respectable merchant. We are not going to let your customers know about the prices. Also, it is a part of our temple duty, and by helping us you also serve the temple and Marduk, our patron. "
    scribe_1_talks "Do not doubt that Marduk, in response, would give you good deals. "

    clay_seller_talks "Here are the prices, my lords. I ask 1 gerah for a bunch of clay tablets, and 1 gerah for a stylus. I also ask 2 gerahs for these big clay pots."

    hide clay_seller with moveoutright

    scribe_1_talks "Hence, I believe we are done for today. Our observations are perhaps a bit strange. Our lord said that the prices on the market rise when water in the canal around the city walls becomes green. "
    scribe_2_talks "However, today we saw the water, and it was green, but the prices are the same, if not smaller! How can we explain this?"
    scribe_1_talks "There is no need to explain. We only collect these records. For the rest - our lord, Anu-aba-uter, is responsible."
    scribe_2_talks "But if we made a mistake?"


    menu:
        "I have something to say on this topic. Should I intervene or not?"

        "Intervene":
            jump argument_with_scribes

        "Do not bother, leave":
            jump argument_with_scribes #change
    return

label argument_with_scribes:
    scene clay_stall
    show Shibtu at left
    show scribes at center

    shibtu_talks "O most respectable lords temple scribes, I beg your pardon that I dare to bother you and interrupt your wisest conversation. But I thought I might know what happened with the prices."
    scribe_1_talks "Who is this little girl? What is she talking about? What can she know? It is funny!"
    shibtu_talks "My lords, I believe prices rise when the water is green, because the water is green after long periods of hot weather. The tiny plants grow in the moat then. "
    shibtu_talks"And when the weather is hot, the villagers prefer to stay at home, instead of coming to the city with their grain, wool, meat and other products. "
    shibtu_talks "But today, even though it was being hot for a few days, the caravans arrived from other cities and countries. Our merchants do not want to completely lose the customers, that is why they keep the prices to compete."
    scribe_1_talks "Why would they do it? Silly little girl, do you think you are smarter than me, Nabu-apla-usur, temple scribe, or than our lord, temple astronomer Anu-aba-uter? In the temple, we observe divine omens for years, and we know what they mean. "
    scribe_1_talks "A mortal man shall not try to find the reasons of the gods’ actions, as they are uncognizable. And who are you? Have you at least worked at the temple? Of course not!" 
    scribe_1_talks "You look like a spoiled girl from a rich family. Your parents did not educate you right, so you become a polite and obedient girl, good for marriage and pleasant to elders. Who is your father?"

    show Ahatabisha at right with moveinright

    scribe_1_talks "Our lady Ahat-Abisha!" 
    scribe_2_talks "She recently sent her prophecy to the king! See that she cut the edge of her garment and her loci to send as an authenticity note." 
    ahatabisha_talks "Good morning, scribes, let Marduk keep you in good health. I wish to talk to this girl. Let Marduk bless you in your deeds. "

    hide scribes


    ahatabisha_talks "What is your name, my young lady?"
    shibtu_talks "I am Shibtu, my lady, let Inanna bless you with perfect health." 
    ahatabisha_talks "Shibtu, I have heard how you talked to these scribes. Who told you all of this?"
    shibtu_talks "No one, my lady. I have learned it myself. On hot nights it is harder for me to observe stars. I do not like these days. That is why I remember everything about such days very well. I just noticed what seems to be related." 
    ahatabisha_talks "That is very smart, Shibtu. You probably understand market prices better than any of those scribes who record them but do not even trouble themselves to think for a moment about what they write down. You should forgive them for their ignorance."
    ahatabisha_talks "I am Ahat-Abisha, I am a high priestess of Ishtar from Ishtar temple. I shall please myself talking to you a bit more. Would you go with me to the tavern?"

    menu:
        "Do not agree, no time to talk":
            shibtu_talks "I beg you forgiveness, my blessed lady, but I do not have time to talk. I have an important business to do. "
            jump tavern # change
        "Agree":
            shibtu_talks "Oh my lady, that shall be a great blessing for me, to have the joy of talking to you."
            jump tavern



label tavern:

    scene tavern_interior
    show Shibtu at left with moveinleft
    show Ahatabisha at right with moveinright

    ahatabisha_talks "Tanatha, the owner of this tavern, is a very respectable woman. She always has everything in order, and no ugly fights ever happen at her place. I will ask her to send us servants with the food."
    shibtu_talks "As you wish, my lady Ahat-Abisha."
    ahatabisha_talks "Shibtu, you said that you observe stars? Is that true so?"
    shibtu_talks "Yes, my lady. My father taught me how to observe the celestial omens, to know when comes spring and new year, and when seasons change. "
    ahatabisha_talks "And so why do you do this? Is that what your father asks you to do? Who is your father, Shibtu?"
    shibtu_talks "I just love doing this, my lady. There is something mystic in the celestial movements, something that charms me deeply." 
    ahatabisha_talks "And then, your father is?"
    shibtu_talks "Oh, forgive me, my lady. My father is Bel-aba-usur. He used to be the astronomer of Esagila temple."
    ahatabisha_talks "Well, I shall have recognized myself the features of him in your face. That was only reasonable to assume that your father was an astronomer. I knew your father. And I know what happened to him though I do not know where he is now. "
    shibtu_talks "My lady, I do not know either. "
    ahatabisha_talks "He was a fine service to the temple and to the people of this city. If not him, I do not know if Esagila temple could keep the observations, compute the calendars and let people enjoy the festivities and do sacrifices. "
    shibtu_talks "My lady, dare I ask you some more about my father?" 
    ahatabisha_talks "Shibtu, not here and not now. Let me be short, I also have not that much time. Now you know me, and I am looking for a daughter to adopt. My position does not let me marry, and I am getting older and wish to have a child to care about. "
    ahatabisha_talks "Shall I need help in my declining years, I wish to also rely on my adopted daughter." 
    ahatabisha_talks "Of course, I do not expect her to be only a service to my gray hairs but I would supervise her in her training to be a priestess. I shall think that you, Shibtu, might now be not in the best position since your father is absent. 
    ahatabisha_talks "Moreover, you seem to be a smart girl who might enjoy serving in a higher position. What would you say?"


    return




#My lords, I believe prices rise when the water is green, because the water is green after long periods of hot weather. The tiny plants grow in the moat then. And when the weather is hot, the villagers prefer to stay at home, instead of coming to the city with their grain, wool, meat and other products. But today, even though it was being hot for a few days, the caravans arrived from other cities and countries. Our merchants do not want to completely lose the customers, that is why they keep the prices to compete.
#Why would they do it? Silly little girl, do you think you are smarter than me, Nabu-apla-usur, temple scribe, or than our lord, temple astronomer Anu-aba-uter? In the temple, we observe divine omens for years, and we know what they mean. A mortal man shall not try to find the reasons of the gods’ actions, as they are uncognizable. And who are you? Have you at least worked at the temple? Of course not! You look like a spoiled girl from a rich family. Your parents did not educate you right, so you become a polite and obedient girl, good for marriage and pleasant to elders. Who is your father?




