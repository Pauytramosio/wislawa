import lists

#%% char methods
def isalpha(char: str) -> bool: return char in lists.alpha
def isdigit(char: str) -> bool: return char in lists.digits
def isalnum(char: str) -> bool: return char in lists.alphanumeric
def isspace(char: str) -> bool: return char in lists.whitespaces