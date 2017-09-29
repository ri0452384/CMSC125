from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

# initialize variables(each text will be the placeholder for the GUI in the output
fcfstext = ""
sjftext = ""
srpttext = ""
priotext = ""
roundtext = ""

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
        return "P:%s t:%s" % (self.processid, self.burst)
    def __copy__(self):
        return Process(self.processid,self.arr,self.burst,self.priority)


def makeprocess(self):
    i = self.split()
    return Process(i[0], i[1], i[2], i[3])

def openfile():
    # initialize variables(each text will be the placeholder for the GUI in the output
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
    srptprocess=[makeprocess(a) for a in content]
    length = processes.__len__()

    global roundtext
    sum=0
    timer=0
    waiting = roundprocess.copy()
    finalprocess=[Process]
    finalprocess.__init__()
    while waiting.__len__() > 0:
        current = waiting.pop(0).__copy__()
        roundtext += "{P:%s t:%s} "  % (current.processid.__str__(),current.burst.__str__())
        current.wtime -= 4
        current.burst -= 4
        timer += 4
        if current.burst > 0:
            waiting.append(current)
        else:
            current.wtime += timer
            finalprocess.append(current)
    finalprocess = sorted(finalprocess, key=lambda x: x.processid, reverse=False)
    sum = 0;
    roundtext += "\nwaiting_time:"
    for x in finalprocess:
        roundtext += "P:%s,w:%s|" % (x.processid.__str__(),x.wtime.__str__())
        sum += x.wtime
    roundtext += "\naverage_waiting_time:"+(sum/length).__str__()
    robinContent.config(text=roundtext)

    global fcfstext
    wait1=0
    for x in fcfsprocess:
        x.wtime=wait1
        wait1 = wait1 + x.burst
    fcfstext = ([x.__str__() for x in fcfsprocess])  # yes, it's dirt cheap!
    wait1 = 0;
    fcfstext += "\nwaiting_time:"
    for x in fcfsprocess:
        fcfstext += "P:%s,w:%s|" % (x.processid.__str__(), x.wtime.__str__())
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
    sjftext += "\nwaiting_time:"
    for x in sjfprocess:
        sjftext += "P:%s,w:%s|" % (x.processid.__str__(), x.wtime.__str__())
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
    wait3 = 0;
    priotext += "\nwaiting_time:"
    for x in prioprocess:
        priotext += "P:%s,w:%s|" % (x.processid.__str__(), x.wtime.__str__())
        wait3 += x.wtime
    priotext += "\naverage_waiting_time:" + (wait3 / length).__str__()
    prioContent.config(text=priotext)

    #todo: include arrival time into calculation
    global srpttext
    elements= 0
    timer = 0
    waiting = [Process]
    waiting.__init__()
    srptfinalprocess = [Process]
    srptfinalprocess.__init__()
    stop=False
    current=None
    while stop == False:
        #load processes with same arrival time to the waiting queue
        for x in srptprocess:
            if x.arr == timer:
                waiting.append(x)
        waiting = sorted(waiting, key=lambda x : x.burst, reverse=False)
        if current == None:
            #print(timer)
            current = waiting.pop(0)
            srpttext += "{P:%s t:%s} " % (current.processid.__str__(), current.burst.__str__())
            current.wtime -= timer
            srptfinalprocess.append(current.__copy__())
            elements +=1
        else:
            current.burst -= 1
        if current.burst <= 0:
            current=None
        timer += 1
        for x in waiting:
            x.wtime +=1
        if waiting.__len__() == 0 and elements == 20:
            stop=True
    wait4 = 0
    for x in srptfinalprocess:
        x.wtime = wait4 - x.arr
        wait4 += x.burst
    srptfinalprocess = sorted(srptfinalprocess, key=lambda x: x.processid, reverse=False)
    wait4=0
    srpttext += "\nwaiting_time:"
    print(srptfinalprocess)
    for x in srptfinalprocess:
        wait4+=x.wtime
        srpttext += "P:%s,w:%s|" % (x.processid.__str__(), x.wtime.__str__())
    srpttext += "\naverage_waiting_time:" + (wait4 / length).__str__()
    srptContent.config(text=srpttext)

def showhelp():
    messagebox.showinfo('Lab 2 description:',"On Processor Management and Job SchedulingImplement the FCFS, SJF, SRPT, Priority and Round-robin scheduling.\n Sample data is given to you (please refer to process1.txt and process2.txt).\n• For FCFS and SJF, assume all processes arrived at time 0 in that order.\n • For SRPT, consider the arrival time of each processes.\n • For Priority, assume that lower-value priorities have higher priorities (that means 0 is the highest priority).\n • For round-robin scheduling, assume a uniform time slice of 4 millisecond.\nDisplay the waiting time for each process for every algorithm, as well as their average computing time.\n Also, perform an algorithm evaluation, based on the datasets given to you.")

root = Tk()

#**************************UI**************** main window code goes  here
root.minsize(width=325,height=100)

#left frame here
mainframe = Frame(root,bg='#2B2B2B')
mainframe.pack()

textwidth=1000
backgroundcolor='#2B2B2B'
fgcolor="#A9B7C6"

#labels here
fcfslabel = Label(mainframe,text="FCFS",bg=backgroundcolor,borderwidth=1)
fcfslabel.grid(column=0,row=0,sticky=NE)
fcfslabel.config(foreground=fgcolor)
fcfsContent = Label(mainframe,text=fcfstext,wraplength=textwidth,bg=backgroundcolor,relief=SUNKEN,borderwidth=1)
fcfsContent.grid(column=1,row=0,sticky=W)
fcfsContent.config(foreground=fgcolor)
sjflabel = Label(mainframe,text="SJF",bg=backgroundcolor,borderwidth=1)
sjflabel.grid(column=0,row=1,sticky=NE)
sjflabel.config(foreground=fgcolor)
sjfContent = Label(mainframe,text=sjftext,wraplength=textwidth,bg=backgroundcolor,relief=SUNKEN,borderwidth=1)
sjfContent.grid(column=1,row=1,sticky=W)
sjfContent.config(foreground=fgcolor)
srptlabel = Label(mainframe,text="SRPT",bg=backgroundcolor,borderwidth=1)
srptlabel.grid(column=0,row=2,sticky=NE)
srptlabel.config(foreground=fgcolor)
srptContent = Label(mainframe,text=srpttext,wraplength=textwidth,bg=backgroundcolor,relief=SUNKEN,borderwidth=1)
srptContent.grid(column=1,row=2,sticky=W)
srptContent.config(foreground=fgcolor)
priolabel = Label(mainframe,text="Priority",bg=backgroundcolor,borderwidth=1)
priolabel.grid(column=0,row=3,sticky=NE)
priolabel.config(foreground=fgcolor)
prioContent = Label(mainframe,text=priotext,wraplength=textwidth,bg=backgroundcolor,relief=SUNKEN,borderwidth=1)
prioContent.grid(column=1,row=3,sticky=W)
prioContent.config(foreground=fgcolor)
robinlabel = Label(mainframe,text="Round Robin",bg=backgroundcolor,borderwidth=1)
robinlabel.grid(column=0,row=4,sticky=NE)
robinlabel.config(foreground=fgcolor)
robinContent = Label(mainframe,text=roundtext,wraplength=textwidth,bg=backgroundcolor,relief=SUNKEN,borderwidth=1)
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
