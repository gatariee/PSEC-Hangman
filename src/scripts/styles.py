class Styles:
    ANSI_COLORS = {
        "red": "\033[91m",
        "green": "\033[92m",
        "bold": "\033[1m",
        "reset": "\033[00m"
    }
    def pr_red(self, s):
        return f"{self.ANSI_COLORS['red']}{s}{self.ANSI_COLORS['reset']}"
    def pr_green(self, s):
        return f"{self.ANSI_COLORS['green']}{s}{self.ANSI_COLORS['reset']}"
    def pr_bold(self, s):
        return f"{self.ANSI_COLORS['bold']}{s}{self.ANSI_COLORS['reset']}"
