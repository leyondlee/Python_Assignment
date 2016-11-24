import sys
import socket
import threading
import select
from Tkinter import *
from ScrolledText import ScrolledText

root = None
size = 4096
run = True

def monitor(con):
    global run
    while run:
        #Wait for IO ready
        rlist, wlist, xlist = select.select([socket],[],[],5)
        for r in rlist:
	    disconnect = False;
            if r == socket: #Check if data is from server
                try:
                    data = socket.recv(size)
                    if data:
                        displayT.configure(state="normal")
                        displayT.insert(END,data)
                        displayT.see(END) # simulate autoscroll
                        displayT.configure(state="disabled")
                    else:
                        #Disconnect
                        disconnect = True
                except:
                    disconnect = True
                        
            if disconnect:
                run = False
                break

    print "connection is closed"
    quit(None)
 
def quit(event):
    global run
    run = False
    if socket:
        # after the socket is closed. the monitor function will be receiving a
        # socket closed exception and exit.
        socket.close()
    try:
        root.destroy()
    except:
        pass # in case the root has been destroyed already
    sys.exit()

def sendmsg(event):
    contents = inputT.get(1.0, END).strip()
    #1.0 refer to 1st line, 0th col
    if contents:
        if contents == '!help':
            #Help menu
            string = '============================== HELP =============================\n'
            string = string + 'Commands:\n'
            string = string + '!show - Show all client info\n'
            string = string + '!shutdown - Shut down server\n'
            string = string + '!broadcast <message> - Broadcast message to all users in server\n'
            string = string + '!kick <address> - Kick user\n'
            string = string + '@<address> <message> - Send private message to user\n'
            string = string + '=================================================================\n'
            displayT.configure(state="normal")
            displayT.insert(END,string)
            displayT.see(END) # simulate autoscroll
            displayT.configure(state="disabled")
        else:
            try:
                msg = contents
                if contents[0] not in ['!','@']:
                    #Add header if not command
                    msg = '[Admin-%s]:%s\n' % (nickName,contents)
                socket.sendall(msg)

                if contents == '!shutdown':
                    #Shutdown
                    quit(None)
            except:
                quit(None)
    # delete the current input from the textbox. (from 1st char to the end)        
    inputT.delete(1.0,END)
##  #set cursor back to row 1, col 0
    inputT.see(1.0)
    
def inputKeyup(event):
    if len(event.char)<1: #ignore 'shift, crtl ... key release
        return
    val = ord(event.char)
    if val==13:   # detected an enter key
        sendmsg(None)

#main program starts here
if len(sys.argv)<3:
    print "Usage: ",sys.argv[0]," server_ip user_nick_name"
    # program still proceeds, using the following two default settings.
    host = 'localhost'
    nickName = 'Anonymous'
else:     
    host = sys.argv[1]
    nickName= sys.argv[2]

try:
    socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.connect((host, 8090))
except:
    print "Connection Failed. Please try again later"
    sys.exit()

# The following is the gui programming part to create a
# window to display the incoming messages, and accept user input to send to
# chat server
root = Tk()
root.title("Admin Client v.0.1")

# Display textbox (15 rows by 80 columns) 
displayT = ScrolledText(root, height=15, width=80)
displayT.insert(END, "")
displayT.configure(state="disabled")
displayT.pack()

# User input textbox (at the lower part of the window, only 2 rows x 80 column)
inputT = Text(root, height=2, width=80, bg='#ffa64d')
inputT.insert(END, "")
inputT.bind('<KeyRelease>', inputKeyup)

inputT.pack(side=LEFT)
sendbutton = Button(root,text="Send")
sendbutton.bind('<Button-1>',sendmsg)
sendbutton.pack()
quitbutton = Button(root,text="Quit")
quitbutton.bind('<Button-1>',quit)
quitbutton.pack()
inputT.focus_set() # ensure focus on the input textbox

#Startup message
displayT.configure(state="normal")
displayT.insert(END,'Enter "!help" for the list of available commands.\n')
displayT.see(END) # simulate autoscroll
displayT.configure(state="disabled")

# starting a separate thread to monitor and display incoming message from
# chat server
t = threading.Thread(target=monitor, args=(socket,)) 
t.start()

# mainloop() is required to start the window activities.
mainloop()
