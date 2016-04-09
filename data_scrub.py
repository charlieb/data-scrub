from datetime import date
from string import ascii_letters
from itertools import filterfalse, tee


class Record(object):
    fields = (
            ('name', 20),
            ('dob', 6),
            ('gender', 1),
            ('< >', 22),
            ('batch_number', 10),
            ('<0>', 2),
            ('< >', 5),
            ('cid', 9),
            ('delivery_method', 1),
            ('< >', 4),
            )

    def __init__(self, name='', dob=date(1970,1,1), gender='M', completion_date=date(1970,1,1), cid=''):
        self.name = name
        self.dob = dob.strftime('%m%d%y')
        self.gender = gender
        self.cid = str(cid)
        self.delivery_method = 'C'
        #                    YMMDD
        #                    |  sponsoring agency code (35)
        #                    |  |  delivery agency code (101)
        self.batch_number = '%5s%2s%3s'%(completion_date.strftime('%y%m%d')[1:], 35, 101)
        self.record = ''
        self.failure_reason = ''
        self.passed = False
    def __repr__(self):
        return ''.join([(name[1]*width if name[0] == '<' else getattr(self,name)).ljust(width) for name,width in self.fields])
    def short_repr(self):
        return ' '.join([getattr(self,name).ljust(width) for name,width in self.fields if name[0] != '<'])
    def read(self, string):
        string = string.strip()
        self.record = string
        pos = 0
        for name,width in self.fields:
            if name[0] != '<':
                setattr(self, name, string[pos:pos + width])
            pos += width
    def check(self):
        self.passed = True

        if len(self.record) != 76: # should be 80 but source data is already stripped of the last 4 spaces
            self.passed = False
            self.failure_reason += 'Whole record is too short.'
        # Person's name rules
        if not all(letter in ascii_letters+',.\'- ' for letter in self.name):
            self.passed = False
            self.failure_reason += ' Student name has strange characters.'

        # CID : License Number rules
        if len(self.cid) < 9:
            self.passed = False
            self.failure_reason += 'CID (license number) is too short.'
        if self.cid.startswith(tuple(ascii_letters)):
            self.passed = False
            self.failure_reason += ' CID (license number) starts with a letter.'
        if self.cid.endswith(tuple(ascii_letters)):
            self.passed = False
            self.failure_reason += ' CID (license number) ends with a letter.'


        return self.passed


def data_file_reader(filename):
    with open(filename, 'r') as f:
        for line in f:
            r = Record()
            r.read(line)
            yield(r)
        
# Utility Functions
def partition(pred, iterable):
    'Use a predicate to partition entries into false entries and true entries'
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)

def deduplicate(records):
    seen_cids = set()
    dupe_cids = set()

    for r in records:
        if r.cid in seen_cids:
            dupe_cids.add(r.cid)
    return partition(lambda r: r.cid in dupe_cids, records)

if __name__ == '__main__':
    r = Record(name = 'Charlie Burrows',
            dob = date(1980,1,26),
            gender = 'M',
            completion_date = date(2015,4,15),
            cid = 123456789)
    print('0123456789'*9)
    string = str(r)
    print(r)
    print(string)
    r2 = Record()
    r2.read(string)
    print(r2.short_repr())
    bad, good = partition(lambda r: r.check(), data_file_reader('SAMPLE DATA.txt'))
    dupes, uniqs = deduplicate(good)
    dupes = sorted(dupes, key=lambda r: r.cid)
        
