from rich.console import Console
from rich.table import Table
from rich.live import Live
from datetime import datetime
from time import sleep
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
import random
import json
import sys,os

'''
Class to dynamically visualize CPU. Each column is its own CPU and 
each row shows what jobs instruction number is inside the CPU.
Could not find a way to assign a specific value to a specific section of a row so we hard coded what could happen 
depending on how many cpus are chosen we set a cap on cpus at seven because of this
'''

class CpuViz:
  def __init__(self, number):
    self.number = number
    self.instructions = []
  
  def update(self, instructions):
    self.instructions = instructions
#Don't we need if name == main in parkerMain
  def build_table(self):
    table = Table(title = "CPU[gold1]")
    for i in range(self.number):
      table.add_column("CPU[light_steel_blue1] " + str(i), justify="center", style="cyan", no_wrap=True)
    if self.number == 1:  
      table.add_row(str(self.instructions[0]))
    elif self.number == 2:
      table.add_row(str(self.instructions[0]), str(self.instructions[1]))
    elif self.number == 3:
      table.add_row(str(self.instructions[0]), str(self.instructions[1]),str(self.instructions[2]))
    elif self.number == 4:
      table.add_row(str(self.instructions[0]), str(self.instructions[1]),str(self.instructions[2]),str(self.instructions[3]))
    elif self.number == 5:
      table.add_row(str(self.instructions[0]), str(self.instructions[1]),str(self.instructions[2]),str(self.instructions[3]),str(self.instructions[4]))
    elif self.number == 6:
      table.add_row(str(self.instructions[0]), str(self.instructions[1]),str(self.instructions[2]),str(self.instructions[3]),str(self.instructions[4]), str(self.instructions[5]))
    elif self.number == 7:
      table.add_row(str(self.instructions[0]), str(self.instructions[1]),str(self.instructions[2]),str(self.instructions[3]),str(self.instructions[4]), str(self.instructions[5]),str(self.instructions[6]))
    return table

  def __rich__(self):
    return Panel(self.build_table())
