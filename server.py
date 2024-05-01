import select, socket, sys, os, random, signal

def correct_signal_handler(sig, frame):
    print('\nReceived: SIGINT')
    sigint_handler(child_processes)
    sys.exit(0)
    
def redirect_stderr():
    devnull = os.open('/dev/null', os.O_WRONLY)
    os.dup2(devnull, sys.stderr.fileno())
    
def clean_resources():
    if os.path.exists("/var/tmp/messages.log"):
        os.remove("/var/tmp/messages.log")

def sigint_handler(array):
    for p in array:
        print("Terminating child process:", p)
        try:
            os.kill(p, signal.SIGTERM)
            os.waitpid(p, 0)
        except ProcessLookupError:
            print(f"Proccess {p} already exited.")
    clean_resources()

def find_by_socket(sock):
    for key, value in allAvailable.items():
        s = value[0]
        if s == sock:
            return key
    return None

    
def send_to_everyone(message: str):
    for _, value in allAvailable.items():
        s = value[0]
        if s != None:
            s.send(message.encode())

def send_to_person(nick, message, s, ifServer=False):
    nickname = nick[1:]
    if nickname == "ADMIN" or nickname == "Admin":
        print(f"\n@{find_by_socket(s)}: {message}\n")
        return
    friend_socket = allAvailable.get(nickname)
    if friend_socket is not None:
        friend_socket = allAvailable.get(nickname)[0]
        if friend_socket == None:
            s.send("\n@SERVER: User you want to send message was disconnected or banned.\n".encode())
            return
            
        if ifServer:
            friend_socket.send(f"\n@ADMIN: {message}\n".encode())
        else:
            friend_socket.send(f"\n@{find_by_socket(s)}: {message}\n".encode())
            s.send(f"\n@{find_by_socket(s)} to @{nickname}: {message}\n".encode())
    else:
        if ifServer:
            print("\n@SERVER: currently there is no such user connected :(\n")
        else:
            s.send("\n@SERVER: currently there is no such user connected :(\n".encode())
        

def send_list_of_connected_users(s):
    keys_list = list(allAvailable.keys())
    resp = "\nAll connected users: "
    for key in keys_list:
        client_status = allAvailable.get(key)[1]
        resp += f"\n\t-- {key}\n\t\t{client_status}"
    resp += "\n"
    s.send(resp.encode())


def stop_client(s, mode="ban"):
    nickname = find_by_socket(s)
    if nickname:
        code = allAvailable[nickname][2]
        if mode == "ban":
            allAvailable[nickname] = (None, "banned", code)
        else:
            allAvailable[nickname] = (None, "disconnected manually", code)
    s.close()
    if s in socketlist:
        socketlist.remove(s)
        
def contains_in_dict_value(generated_code):
    for _, value in allAvailable.items():
        if generated_code == value[2]:
            return True
    return False

if len(sys.argv) < 2:
    print("You need to provide port of server.")
    sys.exit(1)
    
HOST = "127.0.0.1"
PORT = int(sys.argv[1])
MAXBYTES = 4096
child_processes = []
signal.signal(signal.SIGINT, correct_signal_handler)
redirect_stderr()


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((HOST, PORT))
serversocket.listen()
socketlist = [serversocket, sys.stdin]

allAvailable: dict = {}
isAvailable = True

server_logfile_name = "/var/tmp/messages.log"
if os.path.exists(server_logfile_name):
    os.remove(server_logfile_name)
server_logfile = os.open(server_logfile_name, os.O_CREAT)
os.close(server_logfile)
server_logfile = os.open(server_logfile_name, os.O_WRONLY)

args = ["xterm", "-e", "tail", "-f", f"/var/tmp/messages.log"]
child2 = os.fork()
if child2 == 0:
    os.execvp("xterm", args)
child_processes.append(child2)

while len(socketlist) > 0:
    (readable, _, _) = select.select(socketlist, [], [])
    for s in readable:
        if s == serversocket:
            (clientsocket, (addr, port)) = s.accept()
            if isAvailable:
                clientsocket.send(f"OK".encode())

                print("\nWaiting for the nickname...")
                nickname = clientsocket.recv(MAXBYTES).decode().rstrip("\n")

                print(f"connection from: {addr} {port}, with nickname: {nickname}\n")
            
                socketlist.append(clientsocket)
                
                random_number = random.randint(100000, 1000000)
                while contains_in_dict_value(random_number):
                    random_number = random.randint(100000, 1000000)
                
                clientsocket.send(f"{random_number}".encode())
                allAvailable[nickname] = (clientsocket, "active", random_number)
            else:
                clientsocket.send("Firstly, enter your nickname:".encode())
                nickname = clientsocket.recv(MAXBYTES).decode().rstrip("\n")
                if nickname in allAvailable:
                    if allAvailable[nickname][1] == "banned":
                        clientsocket.send(f"ALREADYBANNED".encode())
                        continue
                            
                    clientsocket.send(f"SECRETCODECHECK".encode())
                    secret_code_client = clientsocket.recv(MAXBYTES).decode().rstrip("\n")
                    if secret_code_client == "NULL":
                        clientsocket.send("Sorry, you was not part of current game. See you on the next game!".encode())
                    else:
                        secret_code_server = str(allAvailable[nickname][2])
                        if secret_code_client != secret_code_server:
                            clientsocket.send("NOT VALID SECRET CODE!".encode())
                        else:
                            allAvailable[nickname] = (clientsocket, "active", int(secret_code_server))
                            socketlist.append(clientsocket)
                            clientsocket.send("OK".encode())
                else:
                    clientsocket.send("Sorry, you was not part of current game. See you on the next game!".encode())

        elif s == sys.stdin:
            command = os.read(0, MAXBYTES).decode()
            parts = command.split(" ")
            message = " ".join(parts[1:])
            server_collection = ""
            
            if "!ban" in command:
                nickname = command.split(" ")[0]
                send_to_everyone(f"\n@Everyone from @ADMIN: WAS BANNED {nickname}\n")
                send_to_person(nickname, "YOU ARE BANNED", s, ifServer=True)
                socket_to_ban = allAvailable[nickname[1:]][0]
                stop_client(socket_to_ban)
            elif "!suspend" in command:
                nickname = command.split(" ")[0][1:]
                send_to_everyone(f"\n@Everyone from @ADMIN: WAS FREEZED @{nickname}\n")
                send_to_person(f"@{nickname}", "YOU ARE FREEZED", s, ifServer=True)
                cliend_socket = allAvailable[nickname][0]
                code = allAvailable[nickname][2]
                allAvailable[nickname] = (cliend_socket, "freezed", code)
            elif "!forgive" in command:
                nickname = command.split(" ")[0][1:]
                send_to_everyone(f"\n@Everyone from @ADMIN: WAS UNFREEZED @{nickname}\n")
                send_to_person(f"@{nickname}", "YOU ARE UNFREEZED", s, ifServer=True)
                cliend_socket = allAvailable[nickname][0]
                code = allAvailable[nickname][2]
                allAvailable[nickname] = (cliend_socket, "active", code)
            elif command == "!start\n":
                isAvailable = False
                server_collection = "\n------------!START------------\n"
            elif "@" in parts[0]:
                nicks = []
                i = 0
                while i < len(parts) and "@" in parts[i]:
                    nicks.append(parts[i])
                    i += 1

                j = 0
                message = " ".join(parts[i:])
                while j < len(nicks):
                    server_collection = f"\n@{find_by_socket(s)} to {nicks[j]}: {message}\n"
                    send_to_person(nicks[j], message, s, True)
                    os.write(server_logfile, server_collection.encode())
                    j += 1
            else:
                message = f"\n@Everyone from @ADMIN: {message}\n"
                server_collection = message
                send_to_everyone(message)
            os.write(server_logfile, server_collection.encode())
        
        else:
            command = s.recv(MAXBYTES).decode().rstrip("\n")            
            if len(command) == 0:
                stop_client(s, "manually")
                continue

            if command == "!list":
                send_list_of_connected_users(s)
            else:
                server_collection = ""
                parts = command.split(" ")
                if "@" in parts[0]:
                    nicks = []
                    i = 0
                    while i < len(parts) and "@" in parts[i]:
                        nicks.append(parts[i])
                        i += 1

                    j = 0
                    message = " ".join(parts[i:])
                    while j < len(nicks):
                        server_collection = f"\n@{find_by_socket(s)} to {nicks[j]}: {message}\n"
                        send_to_person(nicks[j], message, s)
                        os.write(server_logfile, server_collection.encode())
                        j += 1
                else:
                    message = f"\n@Everyone from @{find_by_socket(s)}: {command}\n"
                    server_collection = message
                    send_to_everyone(message)
                    os.write(server_logfile, server_collection.encode())
                    
            
            
serversocket.close()