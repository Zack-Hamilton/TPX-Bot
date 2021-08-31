import discord;
import traceback;
import random;
import aiohttp;
import asyncio;
import pickle;
import os;
import requests;

intents = discord.Intents.default();
intents.members = True;
intents.reactions = True;
TPX = discord.Client(intents=intents);

Tokenread = open("Token.txt","r");
Token = Tokenread.readline();

#---------------------------------------------------------------Variables------------------------------------------------------------------------------------------------------------------------------------------------
class Menu:
    Content = "";
    Available = False;
class Status:
    Content = "";
    Type = "";

#----------------------------------------------------------------Modules-------------------------------------------------------------------------------------------------------------------------------------------------
#Add Command
def AddRec(Text,YorN):
    #Variables
    global eof;
    AddRecord = Menu();

    #Data to be stored
    AddRecord.Content = Text;
    AddRecord.Available = YorN;


    #File write
    Write = open("MainMenu.dat","ab");
    pickle.dump(AddRecord,Write);
    Write.close();

#Print Menu
def MainMenu(message,admin):
    #Variables
    TempRecord = Menu();
    global MessageArr;
    Loop = True;
    PrevCheck = "";
    Count = 0;
    
    #File read
    Read = open("MainMenu.dat","rb");
    
    #Line count
    while Loop:
        try:
            TempRecord = pickle.load(Read);
            Count = Count + 1;
        except Exception as e:
            Loop = False;

    #Read contents
    MessageArr = [""] * Count;
    eof = Read.tell();
    Read.seek(0);
    Count = 0;
    Array = False;
    while (Read.tell() != eof):
        TempRecord = pickle.load(Read);
        if (admin == False) and (TempRecord.Available == True):
            MessageArr[Count] = "⦿ " + TempRecord.Content;
            Count = Count + 1;
            Array = True;
        if (admin == True) and (TempRecord.Available == False):
            MessageArr[Count] = "⦿ " + TempRecord.Content;
            Count = Count + 1;
            Array = True;
    if not Array:
        MessageArr = "";
    Read.close();

#Reset Menu
def MenuReset():
    Write = open("MainMenu.dat","wb");
    Write.close();

#Role Check
def RoleCheck(message):
    for role in message:
        if role.name in ["".join(c.upper() if 1 << i & z else c.lower() for i, c in enumerate("admin")) for z in range(64)]:
            return True;
        else:
            return False;

#Initialize
@TPX.event
async def on_ready():
    #File Read
    Read = open("Status.dat","rb");
    TempRecord = Status();
    TempRecord = pickle.load(Read);
    Read.close();

    if TempRecord.Type == "O":
        await TPX.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=(TempRecord.Content)));
    elif TempRecord.Type == "I":
        await TPX.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.playing, name=(TempRecord.Content)));
    elif TempRecord.Type == "D":
        await TPX.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.playing, name=(TempRecord.Content)));
    elif TempRecord.Type == "N":
        await TPX.change_presence(status=discord.Status.invisible, activity=discord.Activity(type=discord.ActivityType.playing, name=(TempRecord.Content)));
    elif TempRecord.Type == "F":
        await TPX.change_presence(status=discord.Status.offline, activity=discord.Activity(type=discord.ActivityType.playing, name=(TempRecord.Content)));

    print("Successfully loaded");
#-----------------------------------------------------------------Code---------------------------------------------------------------------------------------------------------------------------------------------------

@TPX.event
async def on_message(message):
    try:
        #Prevent bot echo
        if message.author == TPX.user:
            return;

        #Get Admin Status
        Role = RoleCheck(message.author.roles)

#----------Modules
        #Edit Pfp
        async def EditPfp(*args, **void):
            global Loop
            # Checking Attachment
            if message.attachments:
                url = str(message.attachments[0].url)
            # Checking Url
            elif args:
                url = args[0]
            # Initiating Aiohttp Session
            try:
                data = requests.get(url).content
                await TPX.user.edit(avatar=data)
                Loop = False;
                return (f"**```Succesfully changed {TPX.user.name}'s avatar!```**")
            #Error
            except Exception as e:
                return ("**```Invalid URL or image sent. Please upload the correct URL or image.```**");
                print("Error report:\n\n",repr(e));
                print("\nTraceback report:\n\n",traceback.format_exc(), end="");

        #Nickname Edit
        async def Nickname(nickname):
            await message.guild.me.edit(nick=nickname);
            await message.channel.send("**```Successfully updated nickname.```**")

        #Status Edit
        async def StatusEdit(status,presence):
            try:
                if presence == "O":
                    await TPX.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=status));
                elif presence == "I":
                    await TPX.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.playing, name=status));
                elif presence == "D":
                    await TPX.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.playing, name=status));
                elif presence == "N":
                    await TPX.change_presence(status=discord.Status.invisible, activity=discord.Activity(type=discord.ActivityType.playing, name=status));
                elif presence == "F":
                    await TPX.change_presence(status=discord.Status.offline, activity=discord.Activity(type=discord.ActivityType.playing, name=status));
                #Write in Record
                TempRecord = Status();
                TempRecord.Content = status;
                TempRecord.Type = presence;
                #File Write
                Write = open("Status.dat","wb");
                pickle.dump(TempRecord,Write);
                Write.close();
            except:
                 if message.author == TPX.user:
                    await message.channel.send("```An unfortunate error has occurred. If this error is reoccurring, please send details of it to my owner so that he may look into it. I apologize for the inconvenience.```");
                 print("Error report:\n\n",repr(e));
                 print("\nTraceback report:\n\n",traceback.format_exc(), end="");

#----------Regular Commands
        #Info
        if (message.content == "t.info"):
            await message.channel.send(f":star:Hi there! I'm your local {message.guild.me.display_name}, here to help out with whatever you need!\nJust use t.menu to open up my commands list and see what I can do! Have fun!:grin:");
        elif(message.content.startswith("t.ask")):
            if message.content[5:] != "":
                if "flare" in message.content:
                    print();
                else:
                    await message.channel.send("You asked..." + message.content[5:] + "? I dunno, I don't have a good reponse list yet :upside_down:");                
            else:
                await message.channel.send(":eyes:What would you like to ask?")
        #Print Menu
        elif (message.content == "t.menu"):
            MainMenu(message,False);
            Loop = True;
            Count = 0;
            String = "```";
            while Loop:
                try:
                    String = String + MessageArr[Count] + "\n";
                    Count = Count + 1;
                except Exception as e:
                    Loop = False;
            if Count == 0:
                await message.channel.send("**```No commands set.```**");
            else:
                String = String + "```";
                await message.channel.send("**```Here's a list of available functions:```**");
                await message.channel.send(String);
#----------Admin Commands
        elif message.author.guild_permissions.administrator or Role:
            #----------Menu Commands
            #Add Menu Item
            if (message.content == "t.menuedit"):
                await message.channel.send("**```Enter Command Name:```**");
                channel = message.channel;
                def check(m):
                    return m.content != ''  and m.channel == channel;
                ComName = (await TPX.wait_for('message',check=lambda m: m.author == message.author and m.channel == message.channel)).content;
            
                await message.channel.send("**```Admin Only?(Y/N):```**");
                Check = False;
                while not Check:
                    ComAvail = await TPX.wait_for('message',check=lambda m: m.author == message.author and m.channel == message.channel);
                    if (ComAvail.content == "Y") or (ComAvail.content == "N"):
                        Check = True;
                    else:
                        await message.channel.send("**```Invalid Response.```**");
                if (ComAvail.content == "N"):
                    Available = True;
                else:
                    Available = False;
                AddRec(ComName,Available);
                await message.channel.send("**```Successfully Added.```**");
            #Print Admin Menu
            elif (message.content == "t.menuadmin"):
                MainMenu(message,True);
                Loop = True;
                Count = 0;
                String = "```";
                while Loop:
                    try:
                        String = String + MessageArr[Count] + "\n";
                        Count = Count + 1;
                    except Exception as e:
                        Loop = False;
                if Count == 0:
                    await message.channel.send("**```No commands set.```**");
                else:
                    String = String + "```";
                    await message.channel.send("**```Here's a list of available functions:```**");
                    await message.channel.send(String);
            #Reset Menu
            elif (message.content == "t.menureset"):
                MenuReset();
                await message.channel.send("**```Menu successfully reset.```**");
            #Customize
            elif (message.content.startswith("t.customize")):
                #Selection
                await message.channel.send('''**```What would you like to change?:```**
```- Profile Picture(P)
- Nickname(N)
- Status(S)```''');
                def check(m):
                    return m.content != ''  and m.channel == channel;
                Check = False;
                while not Check:
                    choice = (await TPX.wait_for('message',check=lambda m: m.author == message.author and m.channel == message.channel)).content;
                    if (choice == "P") or (choice == "N") or (choice == "S"):
                        Check = True;
                    else:
                        await message.channel.send("```Invalid Response.```");

                #Profile Edit
                if (choice == "P"):
                    await message.channel.send("**```Enter URL or image:```**");
                    Loop = True;
                    while Loop:
                        message = await TPX.wait_for('message',check=lambda m: m.author == message.author and m.channel == message.channel);
                        if (message.content == ""):
                            message.content = "Alpha";
                        Response = await EditPfp(message.content);
                        await message.channel.send(Response);

                #Nickname Edit
                elif (choice == "N"):
                    await message.channel.send("**```Enter Nickname:```**");
                    Nick = (await TPX.wait_for('message',check=lambda m: m.author == message.author and m.channel == message.channel)).content;
                    await Nickname(Nick);

                #Status Edit
                elif (choice == "S"):
                    await message.channel.send("**```Enter Status Name:```**");
                    status = (await TPX.wait_for('message',check=lambda m: m.author == message.author and m.channel == message.channel)).content;
                    await message.channel.send('''**```Enter Status Type:```**
```- Online(O)
- Idle(I)
- Do Not Disturb(D)
- Invisible(N)
- Offline(F)```''');
                    Check = False;
                    while not Check:
                        presence = (await TPX.wait_for('message',check=lambda m: m.author == message.author and m.channel == message.channel)).content;
                        if (presence == "O") or (presence == "I") or (presence == "D") or (presence == "N") or (presence == "F"):
                            Check = True;
                        else:
                            await message.channel.send("**```Invalid Response.```**");
                    Response = await StatusEdit(status,presence);
                    await message.channel.send("**```Status successfully updated.```**");
            #Otherwise
            elif (message.content.startswith("t.")):
                await message.channel.send(":confounded:I'm sorry, I'm afraid I do not understand that command. Use t.menu for a list of my available commands.");
#----------Otherwise
        elif (message.content.startswith("t.")):
            await message.channel.send(":confounded:I'm sorry, I'm afraid I do not understand that command. Use t.menu for a list of my available commands.");
#Error Messages
    except Exception as e:
        await message.channel.send("```An unfortunate error has occurred. If this error is reoccurring, please send details of it to my owner so that he may look into it. I apologize for the inconvenience.```");
        print("Error report:\n\n",repr(e));
        print("\nTraceback report:\n\n",traceback.format_exc(), end="");

TPX.run(Token);