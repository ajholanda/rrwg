"""Log facility.

"""
FNAME = 'rrwg.log'
logf = open(FNAME, 'w')
def write(content):
    """Write the content to log file.

    """
    logf.write('{}\n'.format(content))
    logf.flush()
