import socket
import threading 

HEADER = 64 # HEADER to prevent messages that are too long, slice them into chunks
PORT = 5050 
#SERVER = "127.0.0.1"
SERVER = socket.gethostbyname(socket.gethostname()) #Knowing the server
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'    #Format for security protocols
DISCONNECT_MESSAGE = "!DISCONNECT"
MAX_MESSAGE = 4096   # largest message length we accept (bytes)
MAX_CLIENTS = 50     # most simultaneous connections
TIMEOUT = 30        #Time to drop a client 

#Starting the CONNECTION
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.settimeout(TIMEOUT)
    
    try:
        connected = True
        while connected:
            header = conn.recv(HEADER).decode(FORMAT)
            if not header:   #Client closed or crash
                break
            
            try:
            msg_length = int(header)
            except ValueError:
                print(f"[REJECTED] {addr} sent a bad header")
                break

            if msg_length <= 0 or msg_length > MAX_MESSAGE: 
                print(f"[REJECTED] {addr} send length {msg_length}")
                break

            # Adding if for later processing to prevent cluster issues
            if msg_length:  
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT) 
            if msg == DISCONNECT_MESSAGE:
                connected = False
        
            print(f"[{addr}]{msg}")
            conn.send("MESSAGE SENT".encode(FORMAT))
        except socket.timeout:
            print(f"[TIMEOUT] {addr} was idle too long")
        except (ConnectionResetError, UnicodeDecodeError):
            print(f"[ERROR] {addr} sent bad data or dropped")
        finally:
            conn.close() 
        

   
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()
