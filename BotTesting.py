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
    Count = 0
    while (Read.tell() != eof):
        TempRecord = pickle.load(Read);
        if (admin == False) and (TempRecord.Available == True):
            MessageArr[Count] = "- " + TempRecord.Content;
            Count = Count + 1;
        if (admin == True) and (TempRecord.Available == False):
            MessageArr[Count] = "- " + TempRecord.Content;
            Count = Count + 1;
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

#Status Edit
@TPX.event
async def on_ready():
    await TPX.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.playing, name="Reworking bot"));
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
        async def EditPfp(args, **void):            
            # Checking Attachment
            if message.attachments:
                url = str(message.attachments[0].url)
            # Checking Url
            elif args:
                url = args[0:]
            else:
                return (f"Please input an image by URL or attachment.")
            # Initiating Aiohttp Session
            try:
                data = requests.get(url).content
                await TPX.user.edit(avatar=data)
                return (f"Succesfully changed {TPX.user.name}'s avatar!")
            #Error
            except Exception as e:
                if message.author == TPX.user:
                    return;
                await message.channel.send("An unfortunate error has occurred. If this error is reoccurring, please send details of it to my owner so that he may look into it. I apologize for the inconvenience.");
                print("Error report:\n\n",repr(e));
                print("\nTraceback report:\n\n",traceback.format_exc(), end="");


#----------Regular Commands
        #Print Menu
        if (message.content == "t.menu"):
            MainMenu(message,False);
            await message.channel.send("*Here's a list of available functions:*");
            Loop = True;
            Count = 0;
            while Loop:
                try:
                    await message.channel.send(MessageArr[Count]);
                    Count = Count + 1;
                except Exception as e:
                    Loop = False;

#----------Admin Commands
        elif message.author.guild_permissions.administrator or Role:
            #----------Menu Commands
            #Add Menu Item
            if (message.content == "t.menuedit"):
                await message.channel.send("Enter Command Name:");
                channel = message.channel;
                def check(m):
                    return m.content != ''  and m.channel == channel;
                ComName = (await TPX.wait_for('message',check=lambda m: m.author == message.author and m.channel == message.channel)).content;
            
                await message.channel.send("Admin Only?(Y/N):");
                Check = False;
                while not Check:
                    ComAvail = await TPX.wait_for('message',check=lambda m: m.author == message.author and m.channel == message.channel);
                    if (ComAvail.content == "Y") or (ComAvail.content == "N"):
                        Check = True;
                    else:
                        await message.channel.send("Invalid Response.");
                if (ComAvail.content == "N"):
                    Available = True;
                else:
                    Available = False;
                AddRec(ComName,Available);
                await message.channel.send("Successfully Added.");
            #Print Admin Menu
            elif (message.content == "t.menuadmin"):
                MainMenu(message,True);
                await message.channel.send("*Here's a list of available functions:*");
                Loop = True;
                Count = 0;
                while Loop:
                    try:
                        await message.channel.send(MessageArr[Count]);
                        Count = Count + 1;
                    except Exception as e:
                        Loop = False;
            #Reset Menu
            elif (message.content == "t.menureset"):
                MenuReset();
                await message.channel.send("Menu successfully reset.");
            #Edit Pfp
            if (message.content.startswith("t.customize")):
                Response = await EditPfp(message.content[12:]);
                await message.channel.send(Response);
                
#Error Messages
    except Exception as e:
        if message.author == TPX.user:
            return;
        await message.channel.send("An unfortunate error has occurred. If this error is reoccurring, please send details of it to my owner so that he may look into it. I apologize for the inconvenience.");
        print("Error report:\n\n",repr(e));
        print("\nTraceback report:\n\n",traceback.format_exc(), end="");

TPX.run(Token);