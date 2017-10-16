"""
CMSC 125 Lab3 v 1.0 by Rayven N. Ingles
   All wrongs reversed 2017
"""
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
"""
problem definition:

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
class Memblock:
    id=0
    size=0
    current_job=None
    is_free=True
    def __init__(self,idNumber,size):
        self.id = idNumber
        self.size = size
        self.current_job=None

    def __repr__(self):
        return "Mem block %s: %sKB" % (self.id,self.size)

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
    for j in waiting:
        j.__init__()
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
t = 0
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
freelist = [Memblock]
initialize_jobs()
started=FALSE

#text for the Help menu
def showhelp():
    messagebox.showinfo('help file goes here')

def clock():
    global started
    global freelist
    global waiting
    global memories
    global t


    #all memory slots are free during start
    for m in memories:
        freelist.append(m.__copy__())
    r=len(waiting)-1
    s=len(freelist) -1
    is_empty = False
    while(len(waiting) > 0 and is_empty == False):
        for i in range(0,r):
            for j in range(0,s):
                if(waiting[i].size < freelist[j].size and freelist[j].is_free):
                    print(freelist[j],waiting[i])
                    allocate = waiting.pop(i)
                    r-=1
                    freelist[j].current_job = allocate
                    freelist[j].size -= freelist[j].current_job.size
                    freelist[j].is_free = False
                    print(allocate)
                    allocate = None
                if(j >=9):
                    j=0;

    t+=1
    timelabel.config(text=t,font='times 25')
    for f in freelist:
        if f.is_free != False:
            f.current_job.time -= 1
        if f.current_job.time <=0:
            print('*')
            f.current_job=None    #run to completion, memory is then returned to the free list
            f.is_free = True

    for j in range(0,len(waiting)):
        waiting[j].wtime += 1
    root.after(1000,clock)

def simulate_first_fit():
    started = TRUE
    clock()

def simulate_best_fit():
    global started
    clock()
    print(t)
    started = TRUE

def simulate_worst_fit():
    global started
    clock()
    print(t)
    started = TRUE

"""
main window code goes  here
"""
root = Tk()
started = FALSE
root.minsize(width=325, height=100)

#left frame here
mainframe = Frame(root, bg='#2B2B2B')
mainframe.pack()

menu = Menu(root, tearoff=False)
root.title("Lab 3 v1.0")
root.config(menu=menu)

#labels here:

timelabel=Label(mainframe,justify='left')
timelabel.grid(row=0,column=0)
timelabel.config(text = "not started")


label1 = Label(mainframe, text=mem1.__repr__())
label1.grid(row=1,column=0)
label2 = Label(mainframe, text=mem2.__repr__())
label2.grid(row=2,column=0)
label3 = Label(mainframe, text=mem3.__repr__())
label3.grid(row=3,column=0)
label4 = Label(mainframe, text=mem4.__repr__())
label4.grid(row=4,column=0)
label5 = Label(mainframe, text=mem5.__repr__())
label5.grid(row=5,column=0)
label6 = Label(mainframe, text=mem6.__repr__())
label6.grid(row=6,column=0)
label7 = Label(mainframe, text=mem7.__repr__())
label7.grid(row=7,column=0)
label8 = Label(mainframe, text=mem8.__repr__())
label8.grid(row=8,column=0)
label9 = Label(mainframe, text=mem9.__repr__())
label9.grid(row=9,column=0)
label10 = Label(mainframe, text=mem10.__repr__())
label10.grid(row=10,column=0)

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