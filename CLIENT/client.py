#------------- Boilerplate Code Start------
import socket
from tkinter import *
from  threading import Thread
from PIL import ImageTk, Image
import random

screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None


canvas1 = None
canvas2= None

playerName = None
nameEntry = None
nameWindow = None
gameScreen=None
dice=None
finishingBox=None
playerType=None
rollButton=None
playerTurn=None


leftBoxes=[]
rightBoxes=[]

#------------- Boilerplate Code End------


def leftBoard():
    global gameScreen
    global leftBoxes
    global screen_height
    global screen_width
    xPos=20
    for box in range(0,11):
        if box==0:
            boxLabel=Label(gameScreen,font=("Chalkboard SE",30), width=2,height=1,relief="ridge",borderwidth=0,bg="red")
            boxLabel.place(x=xPos,y=screen_height/2-88)
            leftBoxes.append(boxLabel)
            xPos+=40
        else:
            boxLabel=Label(gameScreen,font=("Chalkboard SE",30), width=2,height=1,relief="ridge",borderwidth=0,bg="white")
            boxLabel.place(x=xPos,y=screen_height/2-100)
            leftBoxes.append(boxLabel)
            xPos+=60

def rightBoard():
    global gameScreen
    global rightBoxes
    global screen_height
    global screen_width
    xPos=725
    for box in range(0,11):
        if box==10:
            boxLabel=Label(gameScreen,font=("Chalkboard SE",30), width=2,height=1,relief="ridge",borderwidth=0,bg="yellow")
            boxLabel.place(x=xPos,y=screen_height/2-88)
            rightBoxes.append(boxLabel)
            xPos+=40
        else:
            boxLabel=Label(gameScreen,font=("Chalkboard SE",30), width=2,height=1,relief="ridge",borderwidth=0,bg="white")
            boxLabel.place(x=xPos,y=screen_height/2-100)
            rightBoxes.append(boxLabel)
            xPos+=60

def finishBox():
    global gameScreen
    global screen_height
    global screen_width
    global finishingBox

    finishingBox=Label(gameScreen,font=("Chalkboard SE",24), width=4,height=1,borderwidth=0,bg="green",fg="white",text="Home")
    finishingBox.place(x=screen_width/2-20,y=screen_height/2-100)

def rollDice():
    global SERVER
    global dice
    global playerType
    global rollButton
    global playerTurn
    diceChoices=["\u2680","\u2681","\u2682","\u2683","\u2684","\u2685"]
    value=random.choice(diceChoices)
    rollButton.destroy()
    playerTurn=False
    if playerType=="Player1":
        SERVER.send(f"{value} player 2 turn".encode())
    if playerType=="Player2":
        SERVER.send(f"{value} player 1 turn".encode())



def gameWindow():
    global gameScreen
    global canvas2
    global dice
    global screen_height
    global screen_width
    global rollButton
    
    global playerType
    global playerName
    global playerTurn

    gameScreen=Tk()
    gameScreen.title("Ludo Ladder")
    gameScreen.attributes("-fullscreen",True)
    screen_height=gameScreen.winfo_screenheight()
    screen_width=gameScreen.winfo_screenwidth()
    canvas2=Canvas(gameScreen,width=500,height=500)
    canvas2.pack(fill="both",expand=True)
    bg = ImageTk.PhotoImage(file = "./assets/background.png")
    canvas2.create_image(0,0,image=bg,anchor = "nw")
    canvas2.create_text(screen_width/2,screen_height/5, text="LUDO LADDER",font=("Chalkboard SE",100), fill="white")
    
    leftBoard()
    rightBoard()
    finishBox()

    dice=canvas2.create_text(screen_width/2+10,screen_height/2+250,text="\u2680",font=("Chalkboard SE",100), fill="white")
    rollButton=Button(gameScreen,text="Roll dice",fg="black",bg="grey",width=20,height=5,command=rollDice,font=("Chalkboard SE",20))
    if (playerType=="Player1" and playerTurn):
        rollButton.place(x=screen_width/2-80,y=screen_height/2+250)
    else:
        rollButton.pack_forget()


    gameScreen.resizable(True,True)
    gameScreen.mainloop()



def saveName():
    global SERVER
    global playerName
    global nameEntry
    global nameWindow
    playerName=nameEntry.get()
    nameEntry.delete(0,END)
    nameWindow.destroy()
    SERVER.send(playerName.encode('utf-8'))
    gameWindow()

def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1
    global screen_width
    global screen_height

    nameWindow  = Tk()
    nameWindow.title("Ludo Ladder")
    nameWindow.attributes('-fullscreen',True)


    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas1 = Canvas( nameWindow, width = 500,height = 500)
    canvas1.pack(fill = "both", expand = True)
    # Display image
    canvas1.create_image( 0, 0, image = bg, anchor = "nw")
    canvas1.create_text( screen_width/2, screen_height/5, text = "Enter Name", font=("Chalkboard SE",100), fill="white")

    nameEntry = Entry(nameWindow, width=15, justify='center', font=('Chalkboard SE', 50), bd=5, bg='white')
    nameEntry.place(x = screen_width/2 - 220, y=screen_height/4 + 100)

    button = Button(nameWindow, text="Save", font=("Chalkboard SE", 30),width=15, command=saveName, height=2, bg="#80deea", bd=3)
    button.place(x = screen_width/2 - 130, y=screen_height/2 - 15)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()



# Boilerplate Code
def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT  = 5000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))


    # Creating First Window
    askPlayerName()




setup()
