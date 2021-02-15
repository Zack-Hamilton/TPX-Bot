import discord;
import traceback;
import random;

intents = discord.Intents.default();
intents.members = True;
intents.reactions = True;
TPX = discord.Client(intents=intents);

Tokenread = open("Token.txt","r");
Token = Tokenread.readline();

@TPX.event
async def on_ready():
    await TPX.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.playing, name="nothing special, just working on some code again."));
    print("Successfully loaded");

@TPX.event
async def on_message(message):
    try:
        if message.author == TPX.user:
            return;

        if (message.content.startswith("t.hello")): #message.content[:2] also works
            await message.channel.send("Hello there, {.author}! :wave: Do you require my assistance?".format(message));

        elif (message.content.startswith("t.data")):
            await message.channel.send("I'm TPX bot. I was created on the 9th of January, 2021, and am programmed for the sole purpose of assisting you and other users in their needs. If you have any queries, don't hesitate to ask! ^^");

        elif (message.content.startswith("t.ask")):
            if (message.content[5:] == ""):
                await message.channel.send("What would you like me to ask? :eyes:")
            else:
                count = 0;
                RandomReply = open("BotRandomReplies.txt","r");
                PrestoredReply = open("BotPrestoredReplies.txt","r");
                line_string = PrestoredReply.readline();
                prestored = False;

                while (line_string != "") and (prestored == False):
                    if (message.content.find(line_string.rstrip("\n")) != -1):
                        line_string = PrestoredReply.readline();
                        reply = line_string.rstrip("\n");
                        response = reply;
                        prestored = True;
                    else:
                        prestored = False;
                        line_string = PrestoredReply.readline();
                    line_string = PrestoredReply.readline();
            
                if (prestored == False):
                    count = 0;
                    line_string = RandomReply.readline();
                    arraycount = line_string.rstrip("\n"); #Keep array count 1 more than actual count of items in file
                    Replyarray = [""] * int(arraycount);
                
                    while (line_string != ""):
                        line_string = RandomReply.readline();
                        reply = line_string.rstrip("\n");
                        Replyarray[count] = reply;
                        count = count + 1;

                    response = random.choice(Replyarray);
            
                text = "So you asked..." + message.content[5:] + "? " + response;
            
                await message.channel.send(text.format(message));
                RandomReply.close();
                PrestoredReply.close();

        elif (message.content.startswith("t.echo")):
            if (message.content[6:] == ""):
                await message.channel.send("ECHO, ECHo, ECho, Echo, echo, ech...")
            else:
                await message.channel.send(message.content[6:]);

        elif (message.content.startswith("t.guess")):

            guess = 1;
            randomnumber = random.randint(0,100);
            status = False;
            await message.channel.send("I'm thinking of a number between 1 and 100. Can you guess what it is?");

            while (status == False):
                error = True;
                channel = message.channel;
                def check(m):
                    return m.content != ''  and m.channel == channel;

                while (error == True):
                    while True:
                        try:
                            temp = await TPX.wait_for('message',check=lambda m: m.author == message.author and m.channel == message.channel);
                            usernumber = int(temp.content);
                            if (usernumber < 100) or (usernumber < 0):
                                error = False;
                            else:
                                await message.channel.send("Sorry, but your guess is out of range. Please try again.");
                                error = True;
                            break;
                        except Exception as e:
                            await message.channel.send("Sorry, but that's not a number. Please try again.");
       
                if (usernumber != randomnumber):
                    if (usernumber > randomnumber):
                        await message.channel.send("That's too high! Try again.");
                    else:
                        await message.channel.send("That's too low! Try again.");
                    guess = guess + 1;
                else:
                    status = True;

            wintext = "That's correct! Hooray! :tada:\nYou took about " + str(guess) + " number of tries."
            await message.channel.send(wintext);
            await message.channel.send("Thanks for playing!");

        elif (message.content.startswith("t.roshambo")):
            playcount = 0;
            computercount = 0;
            await message.channel.send("Let's play Rock :rock: Paper :newspaper: Scissors :scissors:! Choose your item.");

            while (playcount != 3) and (computercount != 3):
                playchoice = 0;
                item = 0;
                while (playchoice != 1) and (playchoice != 2) and (playchoice != 3) or (item != 1):
                    item = 0;
                    channel = message.channel;
                    def check(m):
                        return m.content != ''  and m.channel == channel;
                    temp = await TPX.wait_for('message',check=lambda m: m.author == message.author and m.channel == message.channel);

                    if (temp.content.find("rock") != -1) or (temp.content.find("Rock") != -1) or (temp.content.find("ROCK") != -1) or (temp.content.find("🪨") != -1):
                        playchoice = 1;
                        item = item + 1;
                    if (temp.content.find("paper") != -1) or (temp.content.find("Paper") != -1) or (temp.content.find("📰") != -1) or (temp.content.find("🗞️") != -1) or (temp.content.find("PAPER") != -1):
                        playchoice = 2;
                        item = item + 1;
                    if (temp.content.find("scissors") != -1) or (temp.content.find("Scissors") != -1) or (temp.content.find("✂") != -1) or (temp.content.find("SCISSORS") != -1):
                        playchoice = 3;
                        item = item + 1;
                    
                    if (item == 0):
                        await message.channel.send("Um, I'm afraid that's not a valid selection. Please try again.");
                    elif (item > 1):
                        await message.channel.send("You're only supposed to select one item, silly. Try again.");

                computerchoice = random.randint(1,3);
                if (computerchoice == 1):
                    selection = ":rock:";
                elif (computerchoice == 2):
                    selection = ":newspaper:";
                else:
                    selection = ":scissors:";
                chosetext = "I choose " + selection;
                await message.channel.send(chosetext);

                if (playchoice == computerchoice):
                    await message.channel.send("Daww, it's a draw.");
                elif (playchoice == 1) and (computerchoice == 3):
                    await message.channel.send("Oh hey, you won! You get a point!");
                    playcount = playcount + 1;
                elif (playchoice == 2) and (computerchoice == 1):
                    await message.channel.send("Oh hey, you won! You get a point!");
                    playcount = playcount + 1;
                elif (playchoice == 3) and (computerchoice == 2):
                    await message.channel.send("Oh hey, you won! You get a point!");
                    playcount = playcount + 1;
                elif (playchoice == 1) and (computerchoice == 2):
                    await message.channel.send("Looks like I won! I get a point!");
                    computercount = computercount + 1;
                elif (playchoice == 2) and (computerchoice == 3):
                    await message.channel.send("Looks like I won! I get a point!");
                    computercount = computercount + 1;
                elif (playchoice == 3) and (computerchoice == 1):
                    await message.channel.send("Looks like I won! I get a point!");
                    computercount = computercount + 1;
                scoretext = "So far, you have " + str(playcount) + " points, while I have " + str(computercount) + " points.";
                await message.channel.send(scoretext);

            if (playcount == 3):
                await message.channel.send("You won the round! Congratulations! :tada:");
            if (computercount == 3):
                await message.channel.send("Looks like I win this time! That was fun! :smile:");
            await message.channel.send("Thanks for playing!");

        elif (message.content.startswith("t.tableflip")):
            await message.channel.send("Yeah, screw tables (╯°□°）╯︵ ┻━┻");

        elif (message.content.startswith("t.menu")):
            await message.channel.send('Here is a menu of the the commands I am currently able to run:');
            await message.channel.send('```json\n1)    Say Hi! ("t.hello")\n2)    Check my info ("t.data")\n3)    Ask me a question ("t.ask")\n4)    Echo! ("t.echo")\n5)    Play guess the number! ("t.guess")\n5)    Play Rock Paper Scissors! ("t.roshambo")\n```');

        elif (message.content.startswith("t.")):
            await message.channel.send("Um, sorry, but I couldn't quite understand that. Could you repeat that once more?");
    
    except Exception as e:
        if message.author == TPX.user:
            return;
        await message.channel.send("An unfortunate error has occurred. If this error is reoccurring, please send details of it to my owner so that he may look into it. I apologize for the inconvenience.");
        print("Error report:\n\n",repr(e));
        print("\nTraceback report:\n\n",traceback.format_exc(), end="");

TPX.run(Token);