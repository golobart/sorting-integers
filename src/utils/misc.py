import os

def cleanup():
    try:
        os.remove(os.path.join("..", "log", "log.txt"))
    except FileNotFoundError:
        pass

    try:
        os.remove(os.path.join("..", "data", "pools", "slices", "end"))
    except FileNotFoundError:
        pass

    try:
        os.remove(os.path.join("..", "data", "pools", "consolidation", "end"))
    except FileNotFoundError:
        pass
