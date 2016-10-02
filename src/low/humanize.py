# coding=utf-8
def humanize(nbytes):
    """
    Converts an int: bytes as human-friendly str, expressed in 1024 multiples
    :param nbytes: bytes to convert to str
    :return: str: human-friendly amount of bytes
    """
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    if nbytes == 0:
        return '0 B'
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])
