import socket
from  threading import Thread

SERVER = None
PORT = None
IP_ADDRESS = None

CLIENTS = {}

def handleClient(player_socket,player_name):
    global CLIENTS
    playerType=CLIENTS[player_name]["Player_type"]
    if (playerType=="Player1"):
        CLIENTS[player_name]["turn"]=True
        player_socket.send(str({"Player_type":CLIENTS[player_name]["Player_type"],"turn":CLIENTS[player_name]["turn"],"player_name":player_name}.encode()))
    else:
        CLIENTS[player_name]["turn"]=False
        player_socket.send(str({"Player_type":CLIENTS[player_name]["Player_type"],"turn":CLIENTS[player_name]["turn"],"player_name":player_name}.encode()))

    while True:
        try:
            message=player_socket.recv(2048)
            if(message):
                for CName in CLIENTS:
                    CSocket=CLIENTS[CName]["player_socket"]
                    CSocket.send(message)
        except:
            pass
    
def acceptConnections():
    global CLIENTS
    global SERVER

    while True:
        player_socket, addr = SERVER.accept()
        player_name=player_socket.recv(1024).decode().strip()
        if(len(CLIENTS.keys())==0):
            CLIENTS[player_name]={"Player_type":"Player1"}
        else:
            CLIENTS[player_name]={"Player_type":"Player2"}
    
        CLIENTS[player_name]["player_socket"]=player_socket
        CLIENTS[player_name]["address"]=addr
        CLIENTS[player_name]["player_name"]=player_name

        CLIENTS[player_name]["turn"]=False
        print(f"Connection established with {player_name}: {addr}")

        thread=Thread(target=handleClient,args=(player_socket,player_name,))
        thread.start()


def setup():
    print("\n")
    print("\t\t\t\t\t\t*** LUDO LADDER ***")


    global SERVER
    global PORT
    global IP_ADDRESS

    IP_ADDRESS = '127.0.0.1'
    PORT = 5000
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    SERVER.listen(10)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")

    acceptConnections()


setup()
