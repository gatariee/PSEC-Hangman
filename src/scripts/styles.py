class Styles:
    def pr_red(self): 
        return("\033[91m{}\033[00m" .format(self))
    def pr_green(self): 
        return("\033[92m{}\033[00m" .format(self))
    def pr_bold(self):
        return("\033[1m{}\033[00m" .format(self))
