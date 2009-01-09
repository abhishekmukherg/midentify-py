"""
Get video information from a file using mplayer's midentify script
"""

from subprocess import Popen, PIPE
import re

MIDENTIFY_CMD = 'midentify'

PAIR_REGEX = re.compile(r"^(?P<key>[^=\n]+)=(?P<value>(\\\n|.)*)$", flags=re.MULTILINE)
UNESCAPE_REGEX = re.compile(r"\\(.)", flags=re.DOTALL)

class MidentifyFile(object):
    def __init__(self, information_string):
        self.keys = []
        for match in PAIR_REGEX.finditer(information_string):
            key = match.groupdict()['key']
            value = UNESCAPE_REGEX.sub(lambda m: m.groups()[0],
                    match.groupdict()['value'])
            key = key.lower().lstrip('id_')
            self.__dict__[key] = value
            self.keys.append(key)
    def __getitem__(self, key):
        return self.__dict__[key]
    def __iter__(self):
        for key in self.keys:
            yield (key, self[key])

def midentify(filename):
    """
    Returns a MidentifyFile object for the file at filename
    """
    output = Popen([MIDENTIFY_CMD, filename], stdout=PIPE).communicate()[0]
    return MidentifyFile(output)
