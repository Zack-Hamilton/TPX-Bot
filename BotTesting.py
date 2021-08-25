import discord;
import traceback;
import random;
import asyncio;
import pickle;
import os;

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
def MenuFile(Text,YorN):
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

    await message.channel.send("Successfully Added.");

#Print Menu
def MainMenu(message):
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
        if (TempRecord.Available == True):
            MessageArr[Count] = "- " + TempRecord.Content;
        Count = Count + 1;
    Read.close();

#-----------------------------------------------------------------Code---------------------------------------------------------------------------------------------------------------------------------------------------
@TPX.event
async def on_ready():
    await TPX.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.playing, name="Reworking bot"));
    print("Successfully loaded");

@TPX.event
async def on_message(message):
    try:
        #Prevent bot echo
        if message.author == TPX.user:
            return;

#----------Admin Commands
        #Add Menu Item
        if (message.channel.name == "admin-centre-for-tpx"):
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
                MenuFile(ComName,Available);

#----------Regular Commands
        #Print Menu
        elif (message.content == "t.menu"):
            MainMenu(message);
            await message.channel.send("*Here's a list of available functions:*");
            Loop = True;
            Count = 0;
            while Loop:
                try:
                    await message.channel.send(MessageArr[Count]);
                    Count = Count + 1;
                except Exception as e:
                    Loop = False;

#Error
    except Exception as e:
        if message.author == TPX.user:
            return;
        await message.channel.send("An unfortunate error has occurred. If this error is reoccurring, please send details of it to my owner so that he may look into it. I apologize for the inconvenience.");
        print("Error report:\n\n",repr(e));
        print("\nTraceback report:\n\n",traceback.format_exc(), end="");

TPX.run(Token);