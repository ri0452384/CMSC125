from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

fcfstext=""
sjftext=""
srpttext=""
priotext=""
roundtext=""

class Process:
    wtime = 0;
    def __init__(self,number,arrival,burst, prio):
        self.id= number
        self.arr= arrival
        self.cputime= burst
        self.priority= prio
    def __repr__(self):
        return "<P:%s t:%s>" % (self.id, self.cputime)
    def __str__(self):
        return "From str method of Test: <P:%s t:%s>" % (self.id, self.cputime)

def makeprocess(self):
    i = self.split()
    return Process(i[0], i[1], i[2], i[3])

def openfile():
    filename = filedialog.askopenfilename( filetypes = ( ("Text file", "*.txt"),("All files", "*.*")))
    with open(filename) as file:
        content = file.readlines()
    content = [x.strip() for x in content]
    content.pop(0)
    processes = [makeprocess(a) for a in content]
    print([x for x in processes])
    fcfstext.join("FCFS: ")
    fcfstext.join([x.__str__() for x in processes])


def showhelp():
    messagebox.showinfo('Lab 2 description:',"On Processor Management and Job SchedulingImplement the FCFS, SJF, SRPT, Priority and Round-robin scheduling. Sample data is given to you (please refer to process1.txt and process2.txt).• For FCFS and SJF, assume all processes arrived at time 0 in that order. • For SRPT, consider the arrival time of each processes. • For Priority, assume that lower-value priorities have higher priorities (that means 0 is the highest priority). • For round-robin scheduling, assume a uniform time slice of 4 millisecond.Display the waiting time for each process for every algorithm, as well as their average computing time. Also, perform an algorithm evaluation, based on the datasets given to you.")
root = Tk()
#main window code goes  here
root.minsize(width=500,height=175)

#left frame here
mainframe = Frame(root)
mainframe.pack(side=LEFT)

#labels here
fcfslabel = Label(mainframe,text="FCFS")
fcfslabel.grid(column=0,row=0,sticky=E)
fcfsContent = Label(mainframe,text=fcfstext)
fcfsContent.grid(column=1,row=0,sticky=E)
gap1 = Label(mainframe,text=" ")
gap1.grid(column=0,row=1,sticky=E)
sjflabel = Label(mainframe,text="SJF")
sjflabel.grid(column=0,row=2,sticky=E)
sjfContent = Label(mainframe,text=sjftext)
sjfContent.grid(column=1,row=0,sticky=E)
gap2 = Label(mainframe,text=" ")
gap2.grid(column=0,row=3,sticky=E)
srptlabel = Label(mainframe,text="SRPT")
srptlabel.grid(column=0,row=4,sticky=E)
srptContent = Label(mainframe,text=srpttext)
srptContent.grid(column=1,row=0,sticky=E)
gap3 = Label(mainframe,text=" ")
gap3.grid(column=0,row=5,sticky=E)
priolabel = Label(mainframe,text="Priority")
priolabel.grid(column=0,row=6,sticky=E)
prioContent = Label(mainframe,text=priotext)
prioContent.grid(column=1,row=0,sticky=E)
gap4 = Label(mainframe,text=" ")
gap4.grid(column=0,row=7,sticky=E)
robinlabel = Label(mainframe,text="Round Robin")
robinlabel.grid(column=0,row=8,sticky=E)
robinContent = Label(mainframe,text=roundtext)
robinContent.grid(column=1,row=0,sticky=E)

#   main menu here

menu = Menu(root, tearoff=False)
root.title("Scheduling Algorithm Simulator 1.0")
root.config(menu=menu)

#submenu code goes here
filemenu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open...", command=openfile)

filemenu.add_command(label="Help",command=showhelp)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

#bottombar code here
bottombar = Frame(root,bg="white")

bottombar.pack(side=BOTTOM, fill=X)

root.mainloop()
