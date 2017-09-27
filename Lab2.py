from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

#initialize variables(each text will be the placeholder for the GUI in the output
fcfstext=""
sjftext=""
srpttext=""
priotext=""
roundtext=""


class Process:
    def __init__(self,number,arrival,bursttime, prio):
        self.processid= int(number)
        self.arr= int(arrival)
        self.burst= int(bursttime)
        self.priority= int(prio)
        self.wtime=0
    def __repr__(self):
        #return "<P:%s A:%s t:%s prio:%s>" % (self.processid, self.arr, self.cputime,self.priority)
        return "P:%s t:%s w:%s" % (self.processid, self.burst,self.wtime)
    def __str__(self):
        #return "<P:%s A:%s t:%s prio:%s>" % (self.processid, self.arr, self.cputime,self.priority)
        return "P:%s t:%s  w:%s" % (self.processid, self.burst,self.wtime)

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
    fcfsprocess=[makeprocess(a) for a in content]
    sjfprocess=[makeprocess(a) for a in content]
    prioprocess=[makeprocess(a) for a in content]
    roundprocess = [makeprocess(a) for a in content]
    length = processes.__len__()

    global roundtext
    sum=0
    timer=0
    waiting = [Process]
    waiting = roundprocess
    roundrobin = []
    while waiting.__len__() > 0:
        current = waiting.pop(0)
        roundrobin.append(current.__str__())
        current.wtime -= 4
        sum += current.wtime
        current.burst -= 4
        timer+=4
        if current.burst >= 0:
            current.wtime+=timer
            waiting.append(current)
    roundtext = ([y for y in roundrobin])
    sum = sum/length
    roundtext += "\naverage_waiting_time:"+sum.__str__()
    robinContent.config(text=roundtext)

    global fcfstext
    wait1=0
    for x in fcfsprocess:
        x.wtime=wait1
        wait1 = wait1 + x.burst
    fcfstext = ([x.__str__() for x in fcfsprocess])  # yes, it's dirt cheap!
    wait1 = 0;
    for x in fcfsprocess:
        wait1 += x.wtime
    fcfstext += "\naverage_waiting_time:" + (wait1/length).__str__()
    fcfsContent.config(text=fcfstext)

    global sjftext
    wait2 = 0
    sjfprocess = sorted(sjfprocess,key=lambda x: (x.burst,x.processid), reverse=False)
    for x in sjfprocess:
        x.wtime=wait2
        wait2 +=x.burst
    sjftext = ([x.__str__() for x in sjfprocess])
    sjfprocess = sorted(sjfprocess, key=lambda x: (x.processid), reverse=False)
    wait2=0;
    for x in sjfprocess:
        wait2+=x.wtime
    sjftext += "\naverage_waiting_time:" +(wait2/length).__str__()
    sjfContent.config(text=sjftext)

    global priotext
    wait3 = 0
    prioprocess=  sorted(prioprocess,key=lambda x: (x.priority,x.processid), reverse=False)
    for x in prioprocess:
        x.wtime=wait3
        wait3 +=x.burst
    priotext = ([x.__str__() + " pr:" + x.priority.__str__() for x in prioprocess])
    prioprocess = sorted(prioprocess, key=lambda x: (x.processid), reverse=False)
    wait2 = 0;
    for x in prioprocess:
        wait3 += x.wtime
    priotext += "\naverage_waiting_time:" + (wait3 / length).__str__()
    prioContent.config(text=priotext)



    #todo: include arrival time into calculation
    global srpttext
    srpttext = ([x.__str__() for x in processes])
    srptContent.config(text=srpttext)

def showhelp():
    messagebox.showinfo('Lab 2 description:',"On Processor Management and Job SchedulingImplement the FCFS, SJF, SRPT, Priority and Round-robin scheduling.\n Sample data is given to you (please refer to process1.txt and process2.txt).\n• For FCFS and SJF, assume all processes arrived at time 0 in that order.\n • For SRPT, consider the arrival time of each processes.\n • For Priority, assume that lower-value priorities have higher priorities (that means 0 is the highest priority).\n • For round-robin scheduling, assume a uniform time slice of 4 millisecond.\nDisplay the waiting time for each process for every algorithm, as well as their average computing time.\n Also, perform an algorithm evaluation, based on the datasets given to you.")

root = Tk()

#**************************UI**************** main window code goes  here
root.minsize(width=325,height=100)
#left frame here
mainframe = Frame(root,bg='#2B2B2B')
mainframe.pack()

textwidth=450
backgroundcolor='#2B2B2B'
fgcolor="#A9B7C6"

#labels here
fcfslabel = Label(mainframe,text="FCFS",bg=backgroundcolor)
fcfslabel.grid(column=0,row=0,sticky=E)
fcfslabel.config(foreground=fgcolor)
fcfsContent = Label(mainframe,text=fcfstext,wraplength=textwidth,bg=backgroundcolor)
fcfsContent.grid(column=1,row=0,sticky=W)
fcfsContent.config(foreground=fgcolor)
sjflabel = Label(mainframe,text="SJF",bg=backgroundcolor)
sjflabel.grid(column=0,row=1,sticky=E)
sjflabel.config(foreground=fgcolor)
sjfContent = Label(mainframe,text=sjftext,wraplength=textwidth,bg=backgroundcolor)
sjfContent.grid(column=1,row=1,sticky=W)
sjfContent.config(foreground=fgcolor)
srptlabel = Label(mainframe,text="SRPT",bg=backgroundcolor)
srptlabel.grid(column=0,row=2,sticky=E)
srptlabel.config(foreground=fgcolor)
srptContent = Label(mainframe,text=srpttext,wraplength=textwidth,bg=backgroundcolor)
srptContent.grid(column=1,row=2,sticky=W)
srptContent.config(foreground=fgcolor)
priolabel = Label(mainframe,text="Priority",bg=backgroundcolor)
priolabel.grid(column=0,row=3,sticky=E)
priolabel.config(foreground=fgcolor)
prioContent = Label(mainframe,text=priotext,wraplength=textwidth,bg=backgroundcolor)
prioContent.grid(column=1,row=3,sticky=W)
prioContent.config(foreground=fgcolor)
robinlabel = Label(mainframe,text="Round Robin",bg=backgroundcolor)
robinlabel.grid(column=0,row=4,sticky=E)
robinlabel.config(foreground=fgcolor)
robinContent = Label(mainframe,text=roundtext,wraplength=textwidth,bg=backgroundcolor)
robinContent.grid(column=1,row=4,sticky=W)
robinContent.config(foreground=fgcolor)

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
