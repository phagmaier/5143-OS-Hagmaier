import rich
from rich import print
from rich.columns import Columns
from rich import box
from rich import panel
from rich.panel import Panel
from rich.align import Align
from rich.layout import Layout
from rich.live import Live
from rich.console import Console
from rich.table import Table
class Prog_Bar:
    def __init__(self, total):
        self.total = total
        self.prog = 0
        self.percent = 0.0
        self.bar = "┃" * int(self.percent) + '-' * (100 - int(self.percent))
    def update(self, prog):
        self.prog += prog
        self.percent = 100 * (self.prog / float(self.total))
        self.bar = "┃" * int(self.percent) + '-' * (100 - int(self.percent))
    def __rich__(self):
        return Panel(f"[green]┃{self.bar}┃ {self.percent:.2f}%")