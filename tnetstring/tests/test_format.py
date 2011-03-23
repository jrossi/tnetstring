
import sys
import unittest
import random


import tnetstring


FORMAT_EXAMPLES = {
    '0:}': {},
    '0:]': [],
    '51:5:hello,39:11:12345678901#4:this,4:true!0:~4:\x00\x00\x00\x00,]}':
            {'hello': [12345678901, 'this', True, None, '\x00\x00\x00\x00']},
    '5:12345#': 12345,
    '12:this is cool,': "this is cool",
    '0:,': "",
    '0:~': None,
    '4:true!': True,
    '5:false!': False,
    '10:\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00,': "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
    '24:5:12345#5:67890#5:xxxxx,]': [12345, 67890, 'xxxxx'],
    '243:238:233:228:223:218:213:208:203:198:193:188:183:178:173:168:163:158:153:148:143:138:133:128:123:118:113:108:103:99:95:91:87:83:79:75:71:67:63:59:55:51:47:43:39:35:31:27:23:19:15:11:hello-there,]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]': [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[["hello-there"]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
}


def get_random_object(random=random,depth=0):
    """Generate a random serializable object."""
    #  The probability of generating a scalar value
    #  increases as the depth increases, to ensure we bottom out.
    if random.randint(depth,10) <= 3:
        what = random.randint(0,1)
        if what == 0:
            n = random.randint(0,10)
            return list(get_random_object(random,depth+1) for _ in xrange(n))
        if what == 1:
            n = random.randint(0,10)
            d = {}
            for _ in xrange(n):
               k = get_random_object(random,10) # large depth == scalar value
               d[k] = get_random_object(random,depth+1)
            return d
    else:
        what = random.randint(0,5)
        if what == 0:
            return None
        if what == 1:
            return True
        if what == 2:
            return False
        if what == 3:
            return random.randint(0,sys.maxint)
        if what == 4:
            return random.randint(0,sys.maxint)#*1.0/random.randint(0,sys.maxint)
        if what == 5:
            n = random.randint(0,200)
            return "".join(chr(random.randint(0,255)) for _ in xrange(n))

class Test_Format(unittest.TestCase):

    def test_roundtrip_format_examples(self):
        for data, expect in FORMAT_EXAMPLES.items():
            self.assertEqual(expect,tnetstring.loads(data))
            self.assertEqual(expect,tnetstring.loads(tnetstring.dumps(expect)))

    def test_roundtrip_format_random(self):
        for _ in xrange(100):
            v = get_random_object()
            self.assertEqual(v,tnetstring.loads(tnetstring.dumps(v)))
