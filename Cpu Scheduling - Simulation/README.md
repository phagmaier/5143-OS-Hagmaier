# Cpu Scheduling
Parker Hagmaier 05/06/2022
In this project we attempted to simulate four types of CPU scheduling algorithms. Those five algorithms are shortest job first, first come first serve, 
shortest remaining job, and round robin, and priority. Round robin gives each instruction a designated amount of cpu time and after that time is up it is 
added back into the ready queue if it has not completed. Shortest job first gives prioirty to the job that has the least amount of CPU time. Shortest
remaining job gives prefrence to the job that has the least amount of cpu time remaining to complete. first come first serve runs whatever instruction
is first loaded prioirty. Prioirty gives prioirty to whatever job has the highest prioirty and that job gets acess to the CPU first. Some of these algorithms 
like prioirty can create starvation meaning a job with a low prioirty can wait a theoretically infinite amount of time to use the CPU if it has the lowest 
prioirty of any job and each new job has a higher prioirty. To prevent this the longer a job spends in the prioirty queue it will incure a small increment 
to its prioirty (in our similation a increment of .25 was given for each clock tick spent in priority). CPU time is decremented by one for each clock tick
and a instruction can move from one queue to another on every clock tick but an instruction can only move or be run on the CPU/IO once during each clock tick.
There are also several queues in our simulation the New,Ready,Waiting, and terminated. When it is time for an instrction to be loaded it is passed to the new 
queue then ready, cpu, IO and then back to the CPU for termination. These loops can happen severla times depending on how many CPU instructions are required
to finish the instruction. A instruction also only enters the New Queue once and every instruction must end after a CPU execution. During round robin
a instruction may also move from the cpu back to the ready queue if it does not complete in the alloted time given. 

## Files
|   #   | File                | Description                                                                               |
| :---: | --------------------| ------------------------------------------------------------------------------------------|
|   1   | Main.py             | Main driver of my project that launches simulation.                                       |
|   2   | cpu.py              | Decrements a jobs required CPU time                                                       |
|   3   | new.py              | Holds instructions as soon as they are loaded into the simulation                         |
|   4   |ParkerCPuViz.py      | Visulizes instructions that are in cpu shows job number inside CPU                        |
|   5   | progBar.py          | Visualizes the amount of instructions terminated compared to total number of instructions |
|   6   | ready.py            | A glorified list where instructions wait to be loaded into the CPU                        |
|   7   | terminated.py       | A glorified list that stores instructions after all CPU and IO requirments are satisfied  |
|   8   | waiting.py          | A glorified list that stores instructions waiting to enter an I/O devise                  |
|   9   | parkerIoViz.py      | A Rich table that dynamically updates and visualized jobs inside the I/O                  |
|   10  | createJobs.py       | Takes the json file containing all the jobs and converts it to job objects                |
|   6   | generateInput.py    |Creates an input file that will create random jobs                                         |
|   6   | IoClass.py          | Decrements time needed on IO from the job class                                           |
|   6   | jobs.py             | Stores all the information about the job                                                  |

# How to Run
run python3 main.py in the terminal. Must have rich installed 
