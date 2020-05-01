# extracts the msg count from msg that follows the protocol. If there is not int in the msg it raises an error
def getCountFromMsg(word):
    start = word.find('-')
    end = word.find('=')
    try:
        count = int(word[start + 1:end])
        # if there is no int at between '-' and '=' then raise an error
    except TypeError:
        raise TypeError
    except ValueError:
        raise ValueError
    return count
