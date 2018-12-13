#import angr
import floss, vivisect

class DynamicSec():
    def __init__(self, bin_path):
        self.vw = vivisect.VivWorkspace()
        
