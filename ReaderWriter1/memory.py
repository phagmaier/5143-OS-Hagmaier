from rich import print
import json
import random
from random import shuffle

"""
name:                   randInstruction
parameters:             N/A
return:                 inst
purpose:                generate random instructions, and add those to a string
"""
def randInstruction():

    # creating seperate lists of operations, memBlocks, and memAddresses
    ops = ["ADD", "SUB", "MUL", "DIV"]
    registers = ["R1", "R2"]
    memBlocks = ["A", "B", "C"]
    memAddr = [x for x in range(100, 255, 5)]

    # shuffle all of the lists so we will get random indexes
    shuffle(ops)
    shuffle(registers)
    shuffle(memBlocks)
    shuffle(memAddr)


    operation = ops[0]
    r1, r2 = registers[:2]
    memBlock1, memBlock2 = memBlocks[:2]
    memAddress1, memAddress2 = memAddr[:2]

    inst = ""
    inst += f"READ {memBlock1}{memAddress1} {r1}\n"
    inst += f"READ {memBlock2}{memAddress2} {r2}\n"
    inst += f"{operation} {r1} {r2}\n"
    inst += f"WRITE {r1} {memBlock1}{memAddress1}\n"
    return inst

"""
name:                   createMem
parameters:             N/A
return:                 N/A
purpose:                creates our memory for our simulation
"""
def createMem():
    mem = {}
    for section in range(3):
        section = str(chr(section + 65))
        mem[section] = {}
        for i in range(100, 255, 5):
            mem[section][i] = None

    with open("memory.json", "w") as f:
        json.dump(mem, f, indent=2)


if __name__ == "__main__":
    for i in range(10):
        print(randInstruction())
