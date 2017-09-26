from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from operator import itemgetter, attrgetter, methodcaller

#initialize variables(each text will be the placeholder for the GUI in the output
fcfstext=""
sjftext=""
srpttext=""
priotext=""
roundtext=""

class Process:
    wtime = 0;
    def __init__(self,number,arrival,burst, prio):
        self.processid= int(number)
        self.arr= int(arrival)
        self.cputime= int(burst)
        self.priority= int(prio)
    def __repr__(self):
        return "<P:%s A:%s t:%s prio:%s>" % (self.processid, self.arr, self.cputime,self.priority)
    def __str__(self):
        return "<P:%s A:%s t:%s prio:%s>" % (self.processid, self.arr, self.cputime,self.priority)

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

    global fcfstext
    fcfstext=([x.__str__() for x in processes]) #yes, it's dirt cheap!
    wait=0
    for x in processes:
        x.wtime=wait
        wait +=x.cputime
    fcfsContent.config(text=fcfstext)

    global sjftext
    sjfprocess = sorted(processes,key=lambda x: (x.cputime,x.processid), reverse=False)
    sjftext = ([x.__str__() for x in sjfprocess])
    for x in processes:
        x.wtime=wait
        wait +=x.cputime
    sjfContent.config(text=sjftext)

    global priotext
    prioprocess=  sorted(processes,key=lambda x: (x.priority,x.processid), reverse=False)
    priotext = ([x.__str__() for x in prioprocess])
    prioContent.config(text=priotext)

    #todo: implement time slicing
    global roundtext
    roundtext = ([x.__str__() for x in processes])
    robinContent.config(text=roundtext)

    #todo: include arrival time into calculation
    global srpttext
    srpttext = ([x.__str__() for x in processes])
    srptContent.config(text=srpttext)

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
fcfsContent.grid(column=1,row=0,sticky=E,rowspan=2)
sjflabel = Label(mainframe,text="SJF")
sjflabel.grid(column=0,row=2,sticky=E)
sjfContent = Label(mainframe,text=sjftext)
sjfContent.grid(column=1,row=2,sticky=E)
srptlabel = Label(mainframe,text="SRPT")
srptlabel.grid(column=0,row=4,sticky=E)
srptContent = Label(mainframe,text=srpttext)
srptContent.grid(column=1,row=4,sticky=E)
priolabel = Label(mainframe,text="Priority")
priolabel.grid(column=0,row=6,sticky=E)
prioContent = Label(mainframe,text=priotext)
prioContent.grid(column=1,row=6,sticky=E)
robinlabel = Label(mainframe,text="Round Robin")
robinlabel.grid(column=0,row=8,sticky=E)
robinContent = Label(mainframe,text=roundtext)
robinContent.grid(column=1,row=8,sticky=E)

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
