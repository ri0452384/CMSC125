"""
CMSC 125 Lab3: Malloc simulator v 1.0 by Rayven N. Ingles
   All wrongs reversed 2017
--------------------------------------------------------------------------------
JOB LIST
Job Stream #    Time    Job Size
1                  5       5760
2                  4       4190
3                  8       3290
4                  2       2030
5                  2       2550
6                  6       6990
7                  8       8940
8                 10        740
9                  7       3930
10                 6       6890
11                 5       6580
12                 8       3820
13                 9       9140
14                10        420
15                10        220
16                 7       7540
17                 3       3210
18                 1       1380
19                 9       9850
20                 3       3610
21                 7       7540
22                 2       2710
23                 8       8390
24                 5       5950
25                10        760
MEMORY LIST
Memory Block Size
1       9500
2       7000
3       4500
4       8500
5       3000
6       9000
7       1000
8       5500
9       1500
10       500
At one large batch-processing computer installation, the management wants to decide what storage
placement strategy will yield the best possible performance. The installation runs a large real storage
computer under fixed partition multiprogramming. Each user program runs in a single group of
contiguous storage locations. Users state their storage requirements and time units for CPU usage on
their Job Control Card (it used to, and still does work this way, although cards are not used nowadays).
The OS allocates to each user the appropriate partition and starts up the user's job. The job remains in
memory until completion. A total of 50,000 memory locations are available, divided into fixed blocks
as indicated in the table above.
a)Write an event-driven simulation to help you decide which storage placement strategy should be
used at this installation. Your program would use the job stream and memory partitioning as
indicated. Run the program until all jobs have been executed with the memory as is (in order by
address). This will give you the first-fit type performance results.
b) Do the same as (a), but this time implement the worst-fit placement scheme.
c) Sort the memory partitions by size and run the program a second time; this will give you the
best-fit performance results. For all parts (a), (b) and (c) you are investigating the performance
of the system using a typical job stream by measuring:
1. Throughput (how many jobs are processed per given time unit)
2. Storage utilization (percentage of partitions never used, percentage of partitions heavily
used, etc.)
3. Waiting queue length
4. Waiting time in queue
5. Internal fragmentation
d)Look at the results from the first-fit, worst-fit and best-fit. Explain what the results indicate
about the performance of the system for this job mix and memory organization. Is one method
of partitioning better than the other? Why or why not? Could you recommend one method over
the other based on your sample run? Would this hold in all cases? Write some conclusions and
recommendations.
"""
from tkinter import *
from tkinter import messagebox

class Memblock:
    size=0
    times_used=0
    current_job=None
    in_use=False
    largest_fragmentation=0
    def __init__(self,idNumber,size):
        self.id = idNumber
        self.size = size
        self.current_job=None

    def __repr__(self):
        return "Mem %s: %sKB remaining" % (self.id,self.size)

    def __copy__(self):
        return Memblock(self.id,self.size)

class Job:
    wtime=0
    def __init__(self, idNumber, time,  size):
        self.id = idNumber
        self.time = time
        self.size = size
    def __repr__(self):
        return "Job%s: %sKB %sms remaining" % (self.id,self.size,self.time)

    def __copy__(self):
        return Job(self.id,self.time,self.size)


def initialize_jobs():
    global waiting
    # for j in waiting:
    #     j.__init__()
    job1 = Job(1, 5, 5760)
    job2 = Job(2, 4, 4190)
    job3 = Job(3, 8, 3290)
    job4 = Job(4, 2, 2030)
    job5 = Job(5, 2, 2550)
    job6 = Job(6, 6, 6990)
    job7 = Job(7, 8, 8940)
    job8 = Job(8, 10, 740)
    job9 = Job(9, 7, 3930)
    job10 = Job(10, 6, 6890)
    job11 = Job(11, 5, 6580)
    job12 = Job(12, 8, 3820)
    job13 = Job(13, 9, 9140)
    job14 = Job(14, 10, 420)
    job15 = Job(15, 10, 220)
    job16 = Job(16, 7, 7540)
    job17 = Job(17, 3, 3210)
    job18 = Job(18, 1, 1380)
    job19 = Job(19, 9, 9850)
    job20 = Job(20, 3, 3610)
    job21 = Job(21, 7, 7540)
    job22 = Job(22, 2, 2710)
    job23 = Job(23, 8, 8390)
    job24 = Job(24, 5, 5950)
    job25 = Job(25, 10, 760)
    waiting = [job1,job2,job3,job4,job5,job6,job7,job8,job9,job10,job11,job12,job13,job14,job15,job16,job17,job18,job19,
               job20,job21,job22,job23,job24,job25]

#initialize globals
waiting =[]
memories=[]
done = []
t = -1
mem1= Memblock(1, 9500)
mem2= Memblock(2, 7000)
mem3= Memblock(3, 4500)
mem4= Memblock(4, 8500)
mem5= Memblock(5, 3000)
mem6= Memblock(6, 9000)
mem7= Memblock(7, 1000)
mem8= Memblock(8, 5500)
mem9= Memblock(9, 1500)
mem10= Memblock(10,500)
memories = mem1,mem2,mem3,mem4,mem5,mem6,mem7,mem8,mem9,mem10
started=FALSE
timer_id = None
total_internal_fragmentation=0

#text for the Help menu
def showhelp():
    messagebox.showinfo(title="Malloc Simulator Help",message='Select the desired algorithm between First-Fit, Best-Fit, or Worst-Fit. Then, it will simulate memory allocation of the preset jobs.')

def clock():
    global waiting
    global memories
    global t
    global timer_id
    global done
    global total_internal_fragmentation
    usecounter = 0
    total_internal_fragmentation = 0
    #start of segment to update all labels of each memory locations and their current jobs
    for i in range(0,len(memories)):
        memlabels[i].config(text=memories[i].__repr__())
        joblabels[i].config(text=memories[i].current_job.__repr__())
        countlabels[i].config(text="%s\t|\t\t%s" % (memories[i].times_used,memories[i].largest_fragmentation))
        total_internal_fragmentation +=memories[i].largest_fragmentation
    wait_text = ""
    for i in waiting:
        wait_text += i.__repr__()+"\n"
    waitlist.config(text=wait_text)
    done_text=""
    for p in done:
        done_text += "Job %s, wait: %sms \n" % (p.id.__repr__(),(p.wtime+1).__repr__())
    jobs_done.config(text=done_text)
    total_fragmentation.config(text="Total:\t\t%s"%total_internal_fragmentation)
    #end of label update segment
    for mem in memories:
        if mem.current_job !=None:
            mem.current_job.time -=1
            #if current job has completed execution, frees up the mem slot
            if mem.current_job.time ==0:
                mem.size += mem.current_job.size
                done.append(mem.current_job)
                mem.current_job = None
                mem.times_used +=1
                mem.in_use = False
        if mem.in_use:
            usecounter +=1
        if usecounter <= 10:
            for j in waiting:
                if j.size < mem.size and mem.in_use==False:
                    #print("allocating",j," to ",mem)
                    j.wtime = t
                    mem.current_job=j
                    mem.size -= j.size
                    mem.largest_fragmentation = max(mem.size,mem.largest_fragmentation)
                    waiting.remove(j)
                    mem.in_use = True
    t+=1
    timelabel.config(text="%sms"%t,font='times 25')
    timer_id = root.after(1000,clock)

def simulate_first_fit():
    global memories
    if timer_id != None:
       root.after_cancel(timer_id)
    initialize_jobs()
    memories = sorted(memories,key=lambda x:x.id,reverse=False)
    for m in memories:
        m.times_used = 0
        m.largest_fragmentation=0
    global t
    t= -1
    global done
    done = []
    fitlabel.config(text="First Fit")
    clock()

def simulate_best_fit():
    if timer_id != None:
       root.after_cancel(timer_id)
    initialize_jobs()
    global memories
    global t
    t= -1
    global done
    done = []
    fitlabel.config(text="Best Fit")
    #sort the mem partitions in ascending order
    memories = sorted(memories,key=lambda x:x.size,reverse=False)
    for m in memories:
        m.times_used = 0
        m.largest_fragmentation=0
    clock()

def simulate_worst_fit():
    if timer_id != None:
       root.after_cancel(timer_id)
    initialize_jobs()
    global memories
    global t
    t= -1
    global done
    done = []
    fitlabel.config(text="Worst Fit")
    #sort the mem partitions in descending order
    memories = sorted(memories,key=lambda x:x.size,reverse=True)
    for m in memories:
        m.times_used = 0
        m.largest_fragmentation=0
    clock()

"""
main window code goes  here
"""
root = Tk()
root.minsize(width=325, height=100)

#left frame here
mainframe = Frame(root, bg='#2B2B2B')
mainframe.pack()

menu = Menu(root, tearoff=False)
root.title("Memory Allocation simulator v1.0")
root.config(menu=menu)

#labels here:
#initialize the label that shows the timer
timelabel=Label(mainframe,justify='left')
timelabel.grid(row=0,column=0)
timelabel.config(text = "not started")
#label that shows either "First Fit", "Best Fit", or "Worst Fit"
fitlabel = Label(mainframe,justify='left', text= "Click File > Help for instructions",font='times 15')
fitlabel.grid(row=0,column=1)
#label for mem1
label1 = Label(mainframe, text=mem1.__repr__())
label1.grid(row=1,column=0)
job1 = Label(mainframe,text="None")
job1.grid(row=1,column=1)
count1 = Label(mainframe,text=mem1.times_used)
count1.grid(row=1,column=2)
#label for mem2
label2 = Label(mainframe, text=mem2.__repr__())
label2.grid(row=2,column=0)
job2 = Label(mainframe,text="None")
job2.grid(row=2,column=1)
count2 = Label(mainframe,text=mem1.times_used)
count2.grid(row=2,column=2)
#label for mem3
label3 = Label(mainframe, text=mem3.__repr__())
label3.grid(row=3,column=0)
job3 = Label(mainframe,text="None")
job3.grid(row=3,column=1)
count3 = Label(mainframe,text=mem1.times_used)
count3.grid(row=3,column=2)
#label for mem4
label4 = Label(mainframe, text=mem4.__repr__())
label4.grid(row=4,column=0)
job4 = Label(mainframe,text="None")
job4.grid(row=4,column=1)
count4 = Label(mainframe,text=mem1.times_used)
count4.grid(row=4,column=2)
#label for mem5
label5 = Label(mainframe, text=mem5.__repr__())
label5.grid(row=5,column=0)
job5 = Label(mainframe,text="None")
job5.grid(row=5,column=1)
count5 = Label(mainframe,text=mem1.times_used)
count5.grid(row=5,column=2)
#label for mem6
label6 = Label(mainframe, text=mem6.__repr__())
label6.grid(row=6,column=0)
job6 = Label(mainframe,text="None")
job6.grid(row=6,column=1)
count6 = Label(mainframe,text=mem1.times_used)
count6.grid(row=6,column=2)
#label for mem7
label7 = Label(mainframe, text=mem7.__repr__())
label7.grid(row=7,column=0)
job7 = Label(mainframe,text="None")
job7.grid(row=7,column=1)
count7 = Label(mainframe,text=mem1.times_used)
count7.grid(row=7,column=2)
#label for mem8
label8 = Label(mainframe, text=mem8.__repr__())
label8.grid(row=8,column=0)
job8 = Label(mainframe,text="None")
job8.grid(row=8,column=1)
count8 = Label(mainframe,text=mem1.times_used)
count8.grid(row=8,column=2)
#label for mem9
label9 = Label(mainframe, text=mem9.__repr__())
label9.grid(row=9,column=0)
job9 = Label(mainframe,text="None")
job9.grid(row=9,column=1)
count9 = Label(mainframe,text=mem1.times_used)
count9.grid(row=9,column=2)
#label for mem10
label10 = Label(mainframe, text=mem10.__repr__())
label10.grid(row=10,column=0)
job10 = Label(mainframe,text="None")
job10.grid(row=10,column=1)
count10 = Label(mainframe,text=mem1.times_used)
count10.grid(row=10,column=2)
"""place all of the labels on a list for easier update"""
countlabels=[count1,count2,count3,count4,count5,count6,count7,count8,count9,count10]
memlabels = [label1,label2,label3,label4,label5,label6,label7,label8,label9,label10]
joblabels = [job1,job2,job3,job4,job5,job6,job7,job8,job9,job10]
"""column header for the count and largest fragmentation"""
uselabel=Label(mainframe,text="# of times used | largest internal fragmentation")
uselabel.grid(row=0,column=2)
"""label that shows all the jobs which are waiting"""
waitlabel = Label(mainframe,text="Jobs not allocated:")
waitlabel.grid(row=11,column=0)
waitlist = Label(mainframe,text=waiting,justify='left')
waitlist.grid(row=12,column=0)
"""label that shows all jobs done"""
job_done_label = Label(mainframe,text="Jobs Completed: ")
job_done_label.grid(row=11,column=1)
jobs_done = Label(mainframe,text="None")
jobs_done.grid(row=12,column=1)
"""label that shows the total for largest internal fragmentation"""
total_fragmentation = Label(mainframe,text = "Total:\t\t%s"%total_internal_fragmentation)
total_fragmentation.grid(row=11,column=2)
"""
submenu code goes here
"""
filemenu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="First Fit",command=simulate_first_fit)
filemenu.add_command(label="Best Fit",command=simulate_best_fit)
filemenu.add_command(label="Worst Fit",command=simulate_worst_fit)
filemenu.add_command(label="Help",command=showhelp)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

"""
bottombar code goes here
"""
bottombar = Frame(root,bg="white")
bottombar.pack(side=BOTTOM, fill=X)

root.mainloop()
