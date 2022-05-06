# Reader Writer 2
Parker Hagmaier, 05/06/2022:
This project attempts to simulate locking down shared memory and using our own locks.
The first two runs of the simulation show what occurs when we don't account for privliged instructions meaning
we are not protecting them or locking down memory to ensure each prioirty instruction is run in order. 
In these runs each block of instructions is treated the same regardless of whether a shared memory instruction 
is occuring. A shared memory operation in this project is defined as anything interacting with the P block of memory.
Since this  is only a simulation our memory is a Json file with A,B,C segments each with 31 blocks within each segment 
and then P whiich also has 31 blocks. Every other run of our simulation randomizes the sleep values inside the instructions
file so that on our third and fourth runs we can demonstrate that regardless of any sleeps our privliged instructions will be 
run in order. There are four states in this project load into cpu, run cpu, sleep, and terminate. Each of these operations
take a clock tick which in our simulation is defined as a count variable inside a while loop incrimenting. When the simulation is completed 
the user should notice that shared memory is not changing. Prioirty instructions are always a read of a shared memroy value into a register
and a write of that register bakc to that same segment of shared memory. This helps to show the signifcant difference in shared memory when run with
and without locks. 
## Files
|   #   | File                | Description                                                                   |
| :---: | --------------------| ------------------------------------------------------------------------------|
|   1   | Main.py             | Main driver of my project that launches simulation.                           |
|   2   | pcb.py              | Holds instructions each file. Maintains state when context switched           |
|   3   | lock.py             | Holds prioirty instruction number must be unlocked to run prioirty instruction|
|   4   |cpu.py               | Performs arithmatic operations runs and parses instructions.                  |
|   5   | memory.json         | This file represents our memory.                                              |
|   6   | term.py             | After a instruction block is completed it is stored in a list in the termqueue|
|   7   | buildInstructions.py| Creates instruction files that contain all regular and prioirty instructions  |

How to run readerWriter2:
Reader writer two must be run in main after installing rich. To run program run python3 main.py
All these files must also be in the same directory
