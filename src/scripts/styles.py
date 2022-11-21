class Styles:
    @staticmethod
    def pr_red(s): 
        return("\033[91m{}\033[00m" .format(s))
    @staticmethod
    def pr_green(s): 
        return("\033[92m{}\033[00m" .format(s))
    @staticmethod
    def pr_bold(s):
        return("\033[1m{}\033[00m" .format(s))
