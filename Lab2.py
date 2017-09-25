from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

class Process:
    def __init__(self,number,arrival,burst, prio):
        self.id= number
        self.arr= arrival
        self.cputime= burst
        self.priority= prio


def makeprocess(self):
    i = self.split()
    #print(i[0], i[1], i[2], i[3])
    return Process(i[0], i[1], i[2], i[3])

def openfile(self):
    root.filename = filedialog.askopenfilename( filetypes = ( ("Text file", "*.txt"),("All files", "*.*")))
    with open(root.filename) as file:
        content = file.readlines()
    content = [x.strip() for x in content]
    content.pop(0)
    processes = [makeprocess(a) for a in content]
    [x.print() for x in processes]

def displayname():
    print("TEST!")


def showhelp():
    messagebox.showinfo('Lab 2 description:',"On Processor Management and Job SchedulingImplement the FCFS, SJF, SRPT, Priority and Round-robin scheduling. Sample data is given to you (please refer to process1.txt and process2.txt).• For FCFS and SJF, assume all processes arrived at time 0 in that order. • For SRPT, consider the arrival time of each processes. • For Priority, assume that lower-value priorities have higher priorities (that means 0 is the highest priority). • For round-robin scheduling, assume a uniform time slice of 4 millisecond.Display the waiting time for each process for every algorithm, as well as their average computing time. Also, perform an algorithm evaluation, based on the datasets given to you.")
root = Tk()
#main window code goes  here
root.minsize(width=500,height=175)

#left frame here
mainframe = Frame(root)
mainframe.pack(side=LEFT)

#labels here
fcfsbutton = Button(mainframe,text="FCFS", command=displayname)
fcfsbutton.grid(row=0,sticky=NW)
sjfbutton = Button(mainframe,text="SJF", command=displayname)
sjfbutton.grid(row=1,sticky=NW)
srptbutton = Button(mainframe,text="SRPT", command=displayname)
srptbutton.grid(row=2,sticky=NW)
priobutton = Button(mainframe,text="Priority", command=displayname)
priobutton.grid(row=3,sticky=NW)
robinbutton = Button(mainframe,text="Round Robin", command=displayname)
robinbutton.grid(row=4,sticky=NW)

#   main menu here

menu = Menu(root, tearoff=False)
root.title("Scheduling Algorithm Simulator 1.0")
root.config(menu=menu)

#submenu code goes here
subMenu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Help",command=showhelp)
subMenu.add_command(label="Exit", command=root.quit)

#toolbar code here
bottombar = Frame(root,bg="black")

openButton = Button(bottombar,text="Open data file")
openButton.bind("<Button-1>",openfile)
openButton.grid(row=0, column=0)



quitButton = Button(bottombar, text="Quit", command=root.quit)
quitButton.grid(row=0,column=6)

bottombar.pack(side=BOTTOM, fill=X)

root.mainloop()
