# returns the count in a string formatted as a msg defined in the protocol
def getCountFromMsg(word):
    start = word.find('-')
    end = word.find('=')
    try:
        count = int(word[start + 1:end])
        # if there is no int at between '-' and '=' then return -1
    except TypeError:
        raise TypeError
    except ValueError:
        raise ValueError
    return count
