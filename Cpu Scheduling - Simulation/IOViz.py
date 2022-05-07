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
import json
import sys,os


class IO_table:
    def __init__(self):
      self.io_info = []
      
    def build_table(self, ios):
      self.io_info = ioList
      
      for i in range(ios):
        table = Table(title="IO")
        table.add_column("Clock Tick", style="cyan1", no_wrap=True)
        table.add_column("IO #", style="cyan", no_wrap=True)
        table.add_column("Task", no_wrap=True)

        #table.add_row(str(['clock']),str(['device']), ['task'])
        
      return table

    def __rich__(self) -> Panel:

      return Panel(self.build_table())