# Reader Writer 1
Using the python concurrency mechanism that best fits the job, implement a reader / writer framework that will keep a shared memory section safe so that readers will get accurate data and writers won't conflict with each other. This is the first part of our concurrency project in which we protect a critical section of local code. Next project will involve protecting a similar critical section of code via network requests.

The reader/writer problem is a classic which is still very much relevant in todays architecture, especially with database and file servers being so prevalent. The problem is as follows:

Any processes can read from the shared resource, even while others are reading.

Any process may write to the shared resource.

No process may access the shared resource for either reading or writing while another process is in the act of writing to it.

Note: The term "process" is interchangeable with "thread".

This project is not very hard, so don't overthink it. We will expand on this project for our next one, adding the ability to synchronize events over the network. For now, we are only locking the "shared memory" to ensure data integrity.

Reader
Wants to read from shared memory.
Makes no changes.
Writer
Wants to edit one or more shared memory values.
Needs to obtain access before this happens.
The writer will execute a small set of instructions and then write the result to shared memory.
Example
An example readerWriter implementation can be found here in this folder. This is a basic example, and it actually works. The issue is that its shared memory is a single global variable making it not to hard to manage.

One issue this example does not show is that there needs to be multiple instances of readers and writers. In fact, there should be at least a 5 to 1 reader to writer ratio.

Your program should specify with command line params how many writers should be created.
Each writer will execute randomly generated instructions that will ultimately change shared memory.
I would make it so no instruction uses values over 9, keeping the final values relatively small and manageable.
Instructions
The type of instructions that will be executed are listed below:

['MOV','ADD','SUB','MUL','DIV','SET','READ','WRITE']
A list of examples where R1 and R2 are registers. There can be more than 2 registers, but that is not really a factor for this program. It will be relevant next program.

'MOV': MOV R1 R2 Copy value from register R2 to register R1
'ADD': ADD R1 R2 Add values in R1 and R2, storing result in R1.
'SUB': SUB R1 R2 Subtract value in R2 from R1, storing result in R1.
'MUL': MUL R1 R2 Multiply values in R1 and R2, storing result in R1.
'DIV': DIV R1 R2 Divide value in R2 with R1, storing result in R1.
'SET': SET R2 7 Load 7 into R2.
'READ': READ R2 A100 Read memory location A100 into R2.
'WRITE': WRITE R1 B100 Write contents of A into memory location B100.
Generate instructions
Generate a list of over N instructions (minimum in the hundreds) using the guidelines above, giving regards to our memory constraints below. This means:

Each file should generate instructions depending on whether it is a reader or a writer.
Have the ability to generate instructions that only read or write to 1 section of memory (A,B,C) but the default should be reading and writing to all of the three sections.
Readers only READ memory locations.
Writers have to READ memory locations in order to execute instructions.

One instruction is equivalent to:

2 reads
operation

Shared Memory
There are three components: A, B, C with addresses from 100-250 inclusive.
When implementing your locking mechanisms to this shared memory space, you can initially assume that the entire space (A,B,C) can all be locked at once.
But, some implementations will need to lock (A) (B) and (C) separately.
When your program begins load memory.json to "load" the memory.
When your program finishes write your memory back to memory.json.
Experiment / Requirements
Configure each run using command line parameters (sys.argv)
Readers / Writers
Assume W writers, where: 1 < W < 20 (between 1 and 20 writers).
Assume R = 5 * W (5 times the number of readers than writers).
Files
Generate N files of m random instructions, where N == W and m > 100 (Same number of input files than there are writers where each file has minimum of 100 instructions).
Memory
Remember you need to have ability to generate instructions that stay within a single memory block!
Each run will consist of executing 1 files worth of instructions and performing the lock on shared memory as follows:
Lock all of the memory blocks (A,B,C)
Lock only the necessary component (A), (B), (C) as needed. This does mean we might need to obtain more than one lock per instruction as it may be locked by another process.
1 write

## Files
|   #   | File                | Description                                                                            |
| :---: | --------------------| ---------------------------------------------------------------------------------------|
|   1   | Main.py             | Main driver of my project that launches simulation.                                    |
|   2   | memory.json         | This file represents our memory.                                                       |
|   3   | memory.py           | generate random instructions, and add those to a string                                |
|   4   |RandInstructions.py  | Generate random instruction files                                                      |
|   5   | Rich_Layout.py      | Creates the reader and writer visualizations                                           |
|   6   | RWlock.py           | Locks down protected memory and makes sure two writers don't write same memory sections|

How to run readerWriter2:
Reader writer two must be run in main after installing rich. To run program run python3 main.py
All these files must also be in the same directory
