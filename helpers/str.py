"""

Replace md file chars in strings

"""

FORBIDDEN_CHARS = ["*","`","#","_",">"]

def conv(str):
    nstr = ""
    for c in str:
        if c in FORBIDDEN_CHARS:
            nstr += "@"
        else:
            nstr += c
    return nstr