import socket, os, sys, select, signal, subprocess, shutil
from datetime import datetime

def redirect_stderr():
    devnull = os.open('/dev/null', os.O_WRONLY)
    os.dup2(devnull, sys.stderr.fileno())
    
def clean_resources(now):
    if os.path.exists(f"/var/tmp/{now}.fifo"):
        os.remove(f"/var/tmp/{now}.fifo")
    if os.path.exists(f"/var/tmp/{now}.log"):
        os.remove(f"/var/tmp/{now}.log")


def handle_correct_termination(array, now="---", nickname="000000", banned=False):
    if banned:
        clean_resources(now)
        if os.path.exists(f"/var/tmp/{nickname}"):
            shutil.rmtree(f"/var/tmp/{nickname}")
    else:
        clean_resources(now)

    for p in array:
        print("Terminating child process:", p)
        try:
            os.kill(p, signal.SIGTERM)
            pid, _ = os.waitpid(p, 0)
            if pid == 0:
                print(f"Process {p} is still running.")
            else:
                print(f"Ended process: {pid}")
        except ProcessLookupError:
            print(f"Proccess {p} already exited.")
        except ChildProcessError:
            print(f"No child process {p} available.")
    sys.exit(0)


def sigint_handler(sig, frame):
    global termination_required
    termination_required = True    

def sigusr1_handler(sig, frame):
    global termination_required, banned
    termination_required = True 
    banned = True


signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGUSR1, sigusr1_handler)

child_processes = []
termination_required = False
banned = False


MAXBYTES = 4096

if len(sys.argv) != 3:
    print("You need to provide part and address of server to connect")

HOST = sys.argv[1]
PORT = int(sys.argv[2])

socketaddr = (HOST, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(socketaddr)
data = s.recv(MAXBYTES).decode()
nickname = ""

if data == "Firstly, enter your nickname:":
    print(data)
    nickname = os.read(0, MAXBYTES)
    s.send(nickname)
    instructions = s.recv(MAXBYTES).decode()
    nickname = nickname.decode().rstrip("\n")
    if instructions == "SECRETCODECHECK":
        try:
            secret_file = os.open(f"/var/tmp/{nickname}/cookie.txt", os.O_RDONLY)
            code = os.read(secret_file, MAXBYTES).decode().split("\n")[0]
            s.send(code.encode())
        except FileNotFoundError:
            s.send("NULL".encode())
        
        response = s.recv(MAXBYTES).decode()
        if response != "OK":
            print(response)
            sys.exit(0)     
    elif instructions == "ALREADYBANNED":
        print("Sorry, you was banned in current game! Next time try to be polite ;)")
        sys.exit(0)
    else:
        print(instructions)
        sys.exit(0)
        
elif data != "OK":
    print(data)
    sys.exit(0)
else:
    print(f"Connected to {socketaddr}\n")

    print("Firstly enter your nickname: ")
    nickname = os.read(0, MAXBYTES)
    s.send(nickname)

    nickname = nickname.decode().rstrip("\n")
    secret_code = s.recv(MAXBYTES)
    secret_path = f"/var/tmp/{nickname}/cookie.txt"

    if not os.path.exists(os.path.dirname(secret_path)):
        os.makedirs(os.path.dirname(secret_path))
        
    if os.path.exists(secret_path):
        os.remove(secret_path)

    secret_file = os.open(secret_path, os.O_CREAT)
    os.close(secret_file)
    secret_file = os.open(secret_path, os.O_WRONLY)
    os.write(secret_file, secret_code)
    os.close(secret_file)

    print("Commands available: ")
    print("\t 1. Show list of all available clients.")
    print("\t 2. Send the message to one specific client by nickname.")
    print("\t 3. Send message to all the available clients.\n")

main_fork = os.fork()
if main_fork == 0:
    
    def emergency_termination(message):
        print(message)
        os.kill(os.getppid(), signal.SIGINT)
        
    def signal_handler_child(sig, frame):
        global now, nickname
        handle_correct_termination(child_processes_child, now, nickname)
        
        
    def sigchld_handler(sig, frame):
        pid, status = os.waitpid(-1, os.WNOHANG | os.WUNTRACED | os.WCONTINUED)
        if status == 0:
            global child1, child2, child_processes_child, now
            child_processes_child.remove(pid)
            if pid == child1:
                print(f"INPUT TERMINAL IS DEAD: {pid}")
                args = ["xterm", "-e", f"cat > /var/tmp/{now}.fifo"]
                child1 = os.fork()
                if child1 == 0:
                    os.execvp("xterm", args)
                child_processes_child.append(child1)
            else:
                print(f"OUTPUT TERMINAL IS DEAD: {pid}")
                args = ["xterm", "-e", "tail", "-f", f"/var/tmp/{now}.log"]
                child2 = os.fork()
                if child2 == 0:
                    os.execvp("xterm", args)
                child_processes_child.append(child2)


        
    signal.signal(signal.SIGTERM, signal_handler_child)
    signal.signal(signal.SIGCHLD, sigchld_handler)
    child_processes_child = []
    redirect_stderr()
    
    now = datetime.now().strftime("%H%M%S")
    fifo = f"/var/tmp/{now}.fifo"
    if os.path.exists(fifo):
        os.remove(fifo)
    os.mkfifo(fifo)

    args = ["xterm", "-e", f"cat > /var/tmp/{now}.fifo"]
    child1 = os.fork()
    if child1 == 0:
        os.execvp("xterm", args)
    child_processes_child.append(child1)
    
    pipe = os.open(fifo, os.O_RDWR)
    logfile_descriptor = os.open(f"/var/tmp/{now}.log", os.O_CREAT)
    os.close(logfile_descriptor)
    logfile_descriptor = os.open(f"/var/tmp/{now}.log", os.O_WRONLY)

    args = ["xterm", "-e", "tail", "-f", f"/var/tmp/{now}.log"]
    child2 = os.fork()
    if child2 == 0:
        os.execvp("xterm", args)
    child_processes_child.append(child2)

    socketlist = [pipe, s]
    while len(socketlist) > 0:
        (readable, _, _) = select.select(socketlist, [], [])
        for elt in readable:
            if elt == pipe:
                command = os.read(pipe, MAXBYTES)
                if len(command) == 0:
                    break
                try:
                    s.send(command)
                except BrokenPipeError:
                    emergency_termination("The connection to the server was lost. Now there is no possibility to exchange messages. Emergency termination of the program...")
                except ConnectionResetError:
                    emergency_termination("Server crash. Now there is no possibility to exchange messages. Emergency termination of the program...")
                except ConnectionAbortedError:
                    emergency_termination("Your Internet connection has been interrupted. Emergency shutdown of the program...")
                except socket.timeout:
                    emergency_termination("It takes too long to send a message. There is something wrong with your connection or the server connection.")
                except socket.error as e:
                    emergency_termination(f"A network error has occurred: {e}")
            else:
                try:
                    data = s.recv(MAXBYTES).decode()
                except BrokenPipeError:
                    emergency_termination("The connection to the server was lost. Now there is no possibility to exchange messages. Emergency termination of the program...")
                except ConnectionResetError:
                    emergency_termination("Server crash. Now there is no possibility to exchange messages. Emergency termination of the program...")
                except ConnectionAbortedError:
                    emergency_termination("Your Internet connection has been interrupted. Emergency shutdown of the program...")
                except socket.timeout:
                    emergency_termination("It takes too long to send a message. There is something wrong with your connection or the server connection.")
                except socket.error as e:
                    emergency_termination(f"A network error has occurred: {e}")
                    
                    
                if data == "SOS":
                    sys.exit(0)
                elif "YOU ARE BANNED" in data:
                    print(f"\n\n{data}")
                    os.kill(os.getppid(), signal.SIGUSR1)
                elif "YOU ARE FREEZED" in data:
                    os.write(logfile_descriptor, data.encode())
                    os.kill(child1, signal.SIGSTOP)
                elif "YOU ARE UNFREEZED" in data:
                    os.write(logfile_descriptor, data.encode())
                    os.kill(child1, signal.SIGCONT)
                else:
                    os.write(logfile_descriptor, data.encode())
    s.close()
    
else:
    child_processes.append(main_fork)
    print("\nNow you can use this terminal window to type your terminal commands!\n")
    while True:
        if termination_required and banned:
            handle_correct_termination(child_processes, nickname=nickname, banned=True)
        elif termination_required:
            print()
            handle_correct_termination(child_processes, nickname=nickname, banned=False)
        
        readable, _, _ = select.select([sys.stdin], [], [], 0.1)
        if readable:
            command = sys.stdin.readline().strip()
            try:
                result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
                print("STDOUT:")
                print(result.stdout)
                print("STDERR:")
                print(result.stderr)
            except subprocess.CalledProcessError as e:
                print("There is an error while executing your command: ", e)
