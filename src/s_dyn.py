import angr

class DynamicSec():
    def __init__(self, bin_path):
        self.proj = angr.Project(bin_path)
        self.entry = self.proj.entry
        self.state = self.proj.factory.entry_state()
