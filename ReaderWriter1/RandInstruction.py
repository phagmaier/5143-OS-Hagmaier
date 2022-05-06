from pprint import isreadable
from random import shuffle
import json
import random
from datetime import datetime

"""
class:                  RandInstructions
"""
class RandInstructions:
    """
    name:                   __init__
    parameters:             self, **kwargs
    returns:                N/A
    purpose:                
    """
    def __init__(self, **kwargs):
        """
        I want to generate instructions that are basically a single double or
        triple instruction.
        Where:
            1 = (2 reads, 1 op, 1 write)
            2 = (4 reads, 2 ops, 2 writes)
            3 = (6 reads, 3 ops, 3 writes)
        So I generate a list like [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3]
        which weighs more towards a single length instruction. When shuffled
        it looks like: [2, 3, 1, 1, 1, 3, 1, 2, 1, 1, 1, 2]. Now every time
        I generate an instruction, shuffle the list and choose the first value
        to determine instruction size.
        """
        # Build my list to determine instruction length
        shortInst = [1] * 7
        self.instLength = shortInst

        # get a seed from kwargs or use system time
        # this allows us to generate same output if necessary
        self.seed = kwargs.get("seed", datetime.now().timestamp())
        print(self.seed)
        random.seed(self.seed)

        
        # get the **kwargs
        self.localInst = kwargs.get("localInst", False)
        self.readerThread = kwargs.get("readerThread", False)
        self.outFile = kwargs.get("outFile", "writer1.json")
        self.memLocation = kwargs.get("memLocation", (100, 255, 5))
        self.operations = kwargs.get("operations", ["ADD", "SUB", "MUL", "DIV"])
        self.genAmount = kwargs.get("genAmount", 100)
        self.memBlocks = kwargs.get("memBlocks", ["A", "B", "C"])
        self.registers = kwargs.get("registers", ["R1", "R2"])
        self.retFormat = kwargs.get("retFormat", "json")  # or 'str'


        # build list to randomly choose memory addresses within proper range
        start, stop, step = self.memLocation
        self.memaddress = [x for x in range(start, stop, step)]

        # init vars that hold generated instructions
        self.InstrString = ""
        self.listInstructions = []

        # shuffle all appropriate lists
        self.shuffleLists()
        # generate the intructions
        self.generateInstructions()

    """
    name:                   shuffleOps
    parameters:             self
    returns:                N/A
    purpose:                shuffle the lists to create random instructions
    """
    def shuffleLists(self):
        """Shuffles all lists that need shuffling."""
        shuffle(self.instLength)
        shuffle(self.operations)
        shuffle(self.registers)
        shuffle(self.memBlocks)
        shuffle(self.memaddress)

    """
    name:                   generateInstructions
    parameters:             self, num
    return:                 a json file
    purpose:                generates random instructions as well as write those values to a json file
    """
    def generateInstructions(self, num=None):

        # if no num passed in, use default value in constructor
        if not num:
            num = self.genAmount

        for _ in range(num):
            strInst = ""
            listInst = []
            # loop through the list of instructions
            for _ in range(self.instLength[0]):
                self.shuffleLists()

                ops = self.operations[0]
                r1, r2 = self.registers[:2]
                # if we want to lock down memory blocks and not have access to every memory block
                if self.localInst:
                        memBlock1 = memBlock2 = self.memBlocks[0]
                # if we want to not lock down any memory block
                else:
                        memBlock1, memBlock2 = self.memBlocks[:2]

                memAddr1, memAddr2 = self.memaddress[:2]

                # add the type of thread memory block, memory address, and value in the memory location
                strInst += f"READ {memBlock1}{memAddr1} {r1}\n"
                strInst += f"READ {memBlock2}{memAddr2} {r2}\n"
                if not self.readerThread:
                    strInst += f"{ops} {r1} {r2}\n"
                    strInst += f"WRITE {r1} {memBlock2}{memAddr1}\n"

                listInst.append(f"READ {memBlock1}{memAddr1} {r1}")
                listInst.append(f"READ {memBlock2}{memAddr2} {r2}")
                if not self.readerThread:
                    listInst.append(f"{ops} {r1} {r2}")
                    listInst.append(f"WRITE {r1} {memBlock1}{memAddr1}")

            self.InstrString += strInst
            self.listInstructions.append(listInst)

        if self.retFormat == "json":
            with open(self.outFile, "w") as f:
                json.dump(self.listInstructions, f, indent=4)
            return json.dumps(self.listInstructions, indent=4)

    """
    name:                   getJson
    parameters:             self
    return:                 json file
    purpose:                return a json file
    """
    def getJson(self):
        return json.dumps(self.listInstructions, indent=4)

    """
    name:                   getInstrString
    parameters:             self
    return:                 InstrString
    purpose:                returns the objects instruction strings
    """
    def getInstrString(self):
        return self.InstrString

    """
    name:                   getList
    parameters:             self
    return:                 listInstructions
    purpose:                returns the objects list of instructions
    """
    def getList(self):
        return self.listInstructions

if __name__ == "__main__":

    ri = RandInstructions(localInst=False)

    print(ri.getJson())
