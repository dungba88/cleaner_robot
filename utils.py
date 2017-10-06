def cos(direction):
    """naive implementation of cos"""
    return int(abs(2 - direction) - 1)

def sin(direction):
    """naive implementation of cos"""
    return int(1 - abs(direction - 1))
