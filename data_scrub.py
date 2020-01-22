from datetime import date
from string import ascii_letters, digits
from itertools import filterfalse, tee


class Record(object):
    # TODO break down batch number into component parts as shown below
    fields = (
            ('name', 20),
            ('dob', 6),
            ('gender', 1),
            ('< >', 22),
            #('batch_number', 10),
            ('batch_date', 5),
            ('batch_sponsor', 2),
            ('batch_agency', 3),
            ('<0>', 2),
            ('< >', 5),
            ('cid', 9),
            ('delivery_method', 1),
            ('< >', 4),
            )
    sponsoring_agency = 35 # DDD's sponsor code

    def __init__(self, name='', dob=date(1970,1,1), gender='M', completion_date=date(1970,1,1), cid=''):
        self.name = name
        self.dob = dob.strftime('%m%d%y')
        self.gender = gender
        self.cid = str(cid)
        self.delivery_method = 'C'
        self.completion_date = completion_date
        #                     YMMDD
        #                     |  sponsoring agency code (35)
        #                     |  |  delivery agency code (101)
        #self.batch_number = '%5s%2s%3s'%(completion_date.strftime('%y%m%d')[1:], self.sponsoring_agency, 101)
        self.batch_date = completion_date.strftime('%y%m%d')[1:]
        self.batch_sponsor = '%2s'%self.sponsoring_agency
        self.batch_agency = '%3s'%101
        self.record = ''
        self.failure_reason = ''
        self.passed = False
    def __repr__(self):
        return ''.join([(name[1]*width if name[0] == '<' else getattr(self,name)).ljust(width)[0:width]
                        for name,width in self.fields])
    def short_repr(self):
        return ' '.join([getattr(self,name).ljust(width)[0:width] 
                        for name,width in self.fields if name[0] != '<']) + ' ' + self.failure_reason
    def reconstruct(self):
        self.record = str(self).strip()
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
        self.failure_reason = ''

        if len(self.record) != 76: # should be 80 but source data is already stripped of the last 4 spaces
            self.passed = False
            self.failure_reason = 'Whole record is too short.'
        # Person's name rules
        if not all(letter in ascii_letters+',.\'- ' for letter in self.name):
            self.passed = False
            self.failure_reason = 'Student name has strange characters.'
        elif self.name.count(',') >= 3:
            self.passed = False
            self.failure_reason = 'Student name has too many parts.'
        # CID : License Number rules
        elif len(self.cid) < 9:
            self.passed = False
            self.failure_reason = 'CID is too short.'
        elif self.cid.startswith(tuple(ascii_letters)):
            self.passed = False
            self.failure_reason = 'CID starts with a letter.'
        elif self.cid.endswith(tuple(ascii_letters)):
            self.passed = False
            self.failure_reason = 'CID ends with a letter.'
        elif not all(digit in digits for digit in self.cid): 
            self.passed = False
            self.failure_reason = 'CID not all numbers.'
        elif not all(digit in digits for digit in self.batch_date):
            self.passed = False
            self.failure_reason = 'Batch Date not all numbers.'
        elif not (all(digit in digits for digit in self.batch_agency[1:]) and (self.batch_agency[0] in digits or self.batch_agency[0] in ['A', 'B', 'C'])) :
            self.passed = False
            self.failure_reason = 'Batch Agency not all numbers or doesn\'t start with A or B.'
        elif self.batch_sponsor != '35':
            self.passed = False
            self.failure_reason = 'Batch Sponsor should be 35.'
        elif not all(digit in digits for digit in self.dob):
            self.passed = False
            self.failure_reason = 'Date of Birth not all numbers.'
        elif self.gender not in ('M', 'F'):
            self.passed = False
            self.failure_reason = 'Gender not M or F'

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
    rec1, rec2 = tee(records)
    seen_cids = set()
    dupe_cids = set()

    for r in rec1:
        if r.cid in seen_cids:
            dupe_cids.add(r.cid)
        else:
            seen_cids.add(r.cid)
    
    return partition(lambda r: r.cid not in dupe_cids, rec2)

def check_records(records):
    bad, good = partition(lambda r: r.check(), records)
    dupes, uniqs = deduplicate(good)
    dupes = sorted(dupes, key=lambda r: r.cid)
    return list(uniqs), list(bad), list(dupes)

def read_records(filename):
    return check_records(data_file_reader(filename))
def write_records(filename, records):
    with open(filename, 'w') as f:
        for r in records:
            print(r, file=f)

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
    u,b,d = read_records('SAMPLE DATA.txt')
    print(str(len(list(u))), str(len(list(b))), str(len(list(d))))

