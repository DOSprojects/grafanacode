# test_funcs.py
# V0.5.1 LDO 12/11/2022: initial version
'''
    test funcs:
    generate all dashboards

    https://stackoverflow.com/questions/67569802/how-to-create-a-random-json-dictionary-with-a-fixed-outer-structure-for-unit-tes
'''

#******************************************************************************
# EXTERNAL MODULE REFERENCES
#******************************************************************************
import sys
import json
import datetime
import unittest
from hypothesis import example, given, settings, strategies as st

sys.path.insert(0, '/prj/dev_pc/grafana/grc_module')
import grafanacode as grc

JUSTNUM   = list(map(chr, range(48, 57)))
ALFALOWER = list(map(chr, range(97, 122)))
ALFAUPPER = list(map(chr, range(65, 90)))
ALFAONLY  = ALFALOWER + ALFAUPPER
ALFANUM   = JUSTNUM + ALFAONLY

@st.composite
def f_str(draw):
    """
    Build a random string.
    """
    data = draw(
        st.text(ALFANUM, min_size=5, max_size=10)
        )
    return data

@st.composite
def f_strtimestamps(draw):
    """
    Build a random timestamp.
    """
    data =  str(draw(
        st.datetimes(
            min_value=datetime.datetime(year=2020, month=1, day=1),
            max_value=datetime.datetime(year=2100, month=12, day=31),
        )
    ))
    return data

@st.composite
def f_randlist(draw):
    """
    Build a random list.
    """
    data = draw(
        st.recursive(
            st.booleans() | st.floats() | st.text(ALFANUM, min_size=3, max_size=6), st.lists,
            max_leaves=10,
        )
    )
    return data

@st.composite
def f_nesteddict1(draw):
    """
    Build a random nested dictionary structure which is then used as JSON to mask two fixed "token" keys.
    """
    data = draw(
        st.dictionaries(
            keys=st.text(ALFANUM, min_size=5, max_size=10),
            values=st.none() | st.booleans() | st.integers() | st.floats() | st.text(ALFANUM) | f_randlist() | st.emails() |
                               st.dictionaries(st.text(ALFANUM), st.none() | st.booleans() | st.integers() | st.floats() | st.text(ALFANUM)),
            min_size=0,
            max_size=10,
        )
    )
    return data

@st.composite
def f_nesteddict2(draw):
    data = draw(
        st.fixed_dictionaries({
            'id'        : st.integers(min_value=1),
            'kind'      : st.text(ALFAUPPER, min_size=1),
            'payload'   : f_nesteddict1prep(),
            'timestamp' : f_strtimestamps(),
        })
    )
    return data

@st.composite
def f_nesteddict3(draw):
    """
    Build a random nested dictionary structure.
    """
    data = draw(
        st.dictionaries(
            keys=st.text(ALFALOWER, min_size=1, max_size=1),
            values=st.recursive(
                st.text(ALFALOWER, min_size=1, max_size=1),
                lambda children: st.dictionaries(st.text(ALFALOWER, min_size=1, max_size=1), children) | st.lists(children),
                max_leaves=15,
            ),
            min_size=1,
            max_size=5,
     ))
    return data

@st.composite
def f_nesteddict4(draw):
    """
    Build a random nested dictionary structure.
    """
    data = draw(
        st.dictionaries(
            keys=st.text(ALFAONLY, min_size=1, max_size=1),
            values=st.recursive(
                st.text(ALFAONLY, min_size=1, max_size=1),
                lambda children: st.dictionaries(st.text(ALFAONLY, min_size=1, max_size=1), children) | st.lists(children),
                max_leaves=3,
            ),
            min_size=1,
            max_size=3,
     ))
    return data

@st.composite
def f_nesteddictf(draw):
    d1 = {'z': {'a':1, 'b':2, 'c':3, 'asa':[12,3,4],'d':{'da':11, 'db':12,}}}
    d2 = {'zz':33, 'z': {'a':101, 'asa':13, 'e':102, 'd':{'dc':111, 'de':112}}}

    dictMerge(d1, d2)
    print(d1)


def test2():
    height = 23
    gridpos = PropGridPos(1,2,3,height)
    res = {
        'height': height,
        'gridPos': gridpos,
        }
    print(res)
    dictResolve(res)
    print(res)


class clsItem:
    """
    Demo class item.
    """
    def __init__(self, a=1):
        self.a = a

class TestFuncs(unittest.TestCase):
    """
    Tests for the funcs part.
    """
    
    def test(self):
        destdict  = {
            0: None,
            1: True,
            2: '',
            3: 1,
            4: 'a',
            10: [],
            11: ['a'],
            12: ['a', 'b'],
            50: {},
            51: {'a': 'old1'},
            52: {'a': 'old1', 'b': 'old2'},
            53: {'a': 'old1', 'b': 'old2', 'c': {'a': 'old11', 'b': 'old12'}, 'd': 'old3'},
            54: {'a': 'old1', 'b': 'old2', 'c': {'aa': 'old11', 'ab': 'old12'}, 'd': 'old3'},
        }
        adddict = {
            0: None,
            1: True,
            2: '',
            3: 1,
            4: 'a',
            10: [],
            11: ['a'],
            12: ['a', 'b'],
            13: ['c'],
            14: ['c', 'b'],
            15: ['c', '<clsItem>'],
            50: {},
            51: {'a': 'new1'},
            52: {'a': 'new1', 'b': 'new2'},
            53: {'c': 'new1'},
            54: {'a': 'new1', 'c': 'new3'},
            55: {'a': 'new1', 'c': {'a': 'new11'}},
            56: {'a': 'new1', 'c': {'aa': 'new11'}},
            57: {'a': 'new1', 'c': {'a': '<clsItem>'}, 'd': 'new2'},
            90: '<clsItem>',
            91: '<clsItem>',
        }
        resdict = {
            0: {
                0: None,
                1: True,
                2: '',
                3: 1,
                4: 'a',
                10: [],
                11: ['a'],
                12: ['a', 'b'],
                13: ['c'],
                14: ['c', 'b'],
                15: ['c', '<clsItem>'],
                50: {},
                51: {'a': 'new1'},
                52: {'a': 'new1', 'b': 'new2'},
                53: {'c': 'new1'},
                54: {'a': 'new1', 'c': 'new3'},
                55: {'a': 'new1', 'c': {'a': 'new11'}},
                56: {'a': 'new1', 'c': {'aa': 'new11'}},
                57: {'a': 'new1', 'c': {'a': '<clsItem>'}, 'd': 'new2'},
                90: '<clsItem>',
                91: '<clsItem>',
            },
            1: {
                0: True,
                1: True,
                2: '',
                3: 1,
                4: 'a',
                10: [],
                11: ['a'],
                12: ['a', 'b'],
                13: ['c'],
                14: ['c', 'b'],
                15: ['c', '<clsItem>'],
                50: {},
                51: {'a': 'new1'},
                52: {'a': 'new1', 'b': 'new2'},
                53: {'c': 'new1'},
                54: {'a': 'new1', 'c': 'new3'},
                55: {'a': 'new1', 'c': {'a': 'new11'}},
                56: {'a': 'new1', 'c': {'aa': 'new11'}},
                57: {'a': 'new1', 'c': {'a': '<clsItem>'}, 'd': 'new2'},
                90: '<clsItem>',
                91: '<clsItem>',
            },
            2: {
                0: '',
                1: True,
                2: '',
                3: 1,
                4: 'a',
                10: [],
                11: ['a'],
                12: ['a', 'b'],
                13: ['c'],
                14: ['c', 'b'],
                15: ['c', '<clsItem>'],
                50: {},
                51: {'a': 'new1'},
                52: {'a': 'new1', 'b': 'new2'},
                53: {'c': 'new1'},
                54: {'a': 'new1', 'c': 'new3'},
                55: {'a': 'new1', 'c': {'a': 'new11'}},
                56: {'a': 'new1', 'c': {'aa': 'new11'}},
                57: {'a': 'new1', 'c': {'a': '<clsItem>'}, 'd': 'new2'},
                90: '<clsItem>',
                91: '<clsItem>',
            },
            3: {
                0: 1,
                1: True,
                2: '',
                3: 1,
                4: 'a',
                10: [],
                11: ['a'],
                12: ['a', 'b'],
                13: ['c'],
                14: ['c', 'b'],
                15: ['c', '<clsItem>'],
                50: {},
                51: {'a': 'new1'},
                52: {'a': 'new1', 'b': 'new2'},
                53: {'c': 'new1'},
                54: {'a': 'new1', 'c': 'new3'},
                55: {'a': 'new1', 'c': {'a': 'new11'}},
                56: {'a': 'new1', 'c': {'aa': 'new11'}},
                57: {'a': 'new1', 'c': {'a': '<clsItem>'}, 'd': 'new2'},
                90: '<clsItem>',
                91: '<clsItem>',
            },
            4: {
                0: 'a',
                1: True,
                2: '',
                3: 1,
                4: 'a',
                10: [],
                11: ['a'],
                12: ['a', 'b'],
                13: ['c'],
                14: ['c', 'b'],
                15: ['c', '<clsItem>'],
                50: {},
                51: {'a': 'new1'},
                52: {'a': 'new1', 'b': 'new2'},
                53: {'c': 'new1'},
                54: {'a': 'new1', 'c': 'new3'},
                55: {'a': 'new1', 'c': {'a': 'new11'}},
                56: {'a': 'new1', 'c': {'aa': 'new11'}},
                57: {'a': 'new1', 'c': {'a': '<clsItem>'}, 'd': 'new2'},
                90: '<clsItem>',
                91: '<clsItem>',
            },
            10: {
                0: [],
                1: [True],
                2: [''],
                3: [1],
                4: ['a'],
                10: [],
                11: ['a'],
                12: ['a', 'b'],
                13: ['c'],
                14: ['c', 'b'],
                15: ['c', '<clsItem>'],
                50: [{}],
                51: [{'a': 'new1'}],
                52: [{'a': 'new1', 'b': 'new2'}],
                53: [{'c': 'new1'}],
                54: [{'a': 'new1', 'c': 'new3'}],
                55: [{'a': 'new1', 'c': {'a': 'new11'}}],
                56: [{'a': 'new1', 'c': {'aa': 'new11'}}],
                57: [{'a': 'new1', 'c': {'a': '<clsItem>'}, 'd': 'new2'}],
                90: ['<clsItem>'],
                91: ['<clsItem>'],
            },
            11: {
                0: ['a'],
                1: ['a', True],
                2: ['a', ''],
                3: ['a', 1],
                4: ['a', 'a'],
                10: ['a'],
                11: ['a', 'a'],
                12: ['a', 'a', 'b'],
                13: ['a', 'c'],
                14: ['a', 'c', 'b'],
                15: ['a', 'c', '<clsItem>'],
                50: ['a', {}],
                51: ['a', {'a': 'new1'}],
                52: ['a', {'a': 'new1', 'b': 'new2'}],
                53: ['a', {'c': 'new1'}],
                54: ['a', {'a': 'new1', 'c': 'new3'}],
                55: ['a', {'a': 'new1', 'c': {'a': 'new11'}}],
                56: ['a', {'a': 'new1', 'c': {'aa': 'new11'}}],
                57: ['a', {'a': 'new1', 'c': {'a': '<clsItem>'}, 'd': 'new2'}],
                90: ['a', '<clsItem>'],
                91: ['a', '<clsItem>'],
            },
            12: {
                0: ['a', 'b'],
                1: ['a', 'b', True],
                2: ['a', 'b', ''],
                3: ['a', 'b', 1],
                4: ['a', 'b', 'a'],
                10: ['a', 'b'],
                11: ['a', 'b', 'a'],
                12: ['a', 'b', 'a', 'b'],
                13: ['a', 'b', 'c'],
                14: ['a', 'b', 'c', 'b'],
                15: ['a', 'b', 'c', '<clsItem>'],
                50: ['a', 'b', {}],
                51: ['a', 'b', {'a': 'new1'}],
                52: ['a', 'b', {'a': 'new1', 'b': 'new2'}],
                53: ['a', 'b', {'c': 'new1'}],
                54: ['a', 'b', {'a': 'new1', 'c': 'new3'}],
                55: ['a', 'b', {'a': 'new1', 'c': {'a': 'new11'}}],
                56: ['a', 'b', {'a': 'new1', 'c': {'aa': 'new11'}}],
                57: ['a', 'b', {'a': 'new1', 'c': {'a': '<clsItem>'}, 'd': 'new2'}],
                90: ['a', 'b', '<clsItem>'],
                91: ['a', 'b', '<clsItem>'],
            },
            50: {
                0: {},
                1: True,
                2: '',
                3: 1,
                4: 'a',
                10: [],
                11: ['a'],
                12: ['a', 'b'],
                13: ['c'],
                14: ['c', 'b'],
                15: ['c', '<clsItem>'],
                50: {},
                51: {'a': 'new1'},
                52: {'a': 'new1', 'b': 'new2'},
                53: {'c': 'new1'},
                54: {'a': 'new1', 'c': 'new3'},
                55: {'a': 'new1', 'c': {'a': 'new11'}},
                56: {'a': 'new1', 'c': {'aa': 'new11'}},
                57: {'a': 'new1', 'c': {'a': '<clsItem>'}, 'd': 'new2'},
                90: '<clsItem>',
                91: '<clsItem>',
            },
            51: {
                0: {'a': 'old1'},
                1: True,
                2: '',
                3: 1,
                4: 'a',
                10: [],
                11: ['a'],
                12: ['a', 'b'],
                13: ['c'],
                14: ['c', 'b'],
                15: ['c', '<clsItem>'],
                50: {'a': 'old1'},
                51: {'a': 'new1'},
                52: {'a': 'new1', 'b': 'new2'},
                53: {'a': 'old1', 'c': 'new1'},
                54: {'a': 'new1', 'c': 'new3'},
                55: {'a': 'new1', 'c': {'a': 'new11'}},
                56: {'a': 'new1', 'c': {'aa': 'new11'}},
                57: {'a': 'new1', 'c': {'a': '<clsItem>'}, 'd': 'new2'},
                90: '<clsItem>',
                91: '<clsItem>',
            },
            52: {
                0: {'a': 'old1', 'b': 'old2'},
                1: True,
                2: '',
                3: 1,
                4: 'a',
                10: [],
                11: ['a'],
                12: ['a', 'b'],
                13: ['c'],
                14: ['c', 'b'],
                15: ['c', '<clsItem>'],
                50: {'a': 'old1', 'b': 'old2'},
                51: {'a': 'new1', 'b': 'old2'},
                52: {'a': 'new1', 'b': 'new2'},
                53: {'a': 'old1', 'b': 'old2', 'c': 'new1'},
                54: {'a': 'new1', 'b': 'old2', 'c': 'new3'},
                55: {'a': 'new1', 'b': 'old2', 'c': {'a': 'new11'}},
                56: {'a': 'new1', 'b': 'old2', 'c': {'aa': 'new11'}},
                57: {'a': 'new1', 'b': 'old2', 'c': {'a': '<clsItem>'}, 'd': 'new2'},
                90: '<clsItem>',
                91: '<clsItem>',
            },
            53: {
                0: {'a': 'old1', 'b': 'old2', 'c': {'a': 'old11', 'b': 'old12'}, 'd': 'old3'},
                1: True,
                2: '',
                3: 1,
                4: 'a',
                10: [],
                11: ['a'],
                12: ['a', 'b'],
                13: ['c'],
                14: ['c', 'b'],
                15: ['c', '<clsItem>'],
                50: {'a': 'old1', 'b': 'old2', 'c': {'a': 'old11', 'b': 'old12'}, 'd': 'old3'},
                51: {'a': 'new1', 'b': 'old2', 'c': {'a': 'old11', 'b': 'old12'}, 'd': 'old3'},
                52: {'a': 'new1', 'b': 'new2', 'c': {'a': 'old11', 'b': 'old12'}, 'd': 'old3'},
                53: {'a': 'old1', 'b': 'old2', 'c': 'new1', 'd': 'old3'},
                54: {'a': 'new1', 'b': 'old2', 'c': 'new3', 'd': 'old3'},
                55: {'a': 'new1', 'b': 'old2', 'c': {'a': 'new11', 'b': 'old12'}, 'd': 'old3'},
                56: {'a': 'new1', 'b': 'old2', 'c': {'a': 'old11', 'b': 'old12', 'aa': 'new11'}, 'd': 'old3'},
                57: {'a': 'new1', 'b': 'old2', 'c': {'a': '<clsItem>', 'b': 'old12'}, 'd': 'new2'},
                90: '<clsItem>',
                91: '<clsItem>',
            },
            54: {
                0: {'a': 'old1', 'b': 'old2', 'c': {'aa': 'old11', 'ab': 'old12'}, 'd': 'old3'},
                1: True,
                2: '',
                3: 1,
                4: 'a',
                10: [],
                11: ['a'],
                12: ['a', 'b'],
                13: ['c'],
                14: ['c', 'b'],
                15: ['c', '<clsItem>'],
                50: {'a': 'old1', 'b': 'old2', 'c': {'aa': 'old11', 'ab': 'old12'}, 'd': 'old3'},
                51: {'a': 'new1', 'b': 'old2', 'c': {'aa': 'old11', 'ab': 'old12'}, 'd': 'old3'},
                52: {'a': 'new1', 'b': 'new2', 'c': {'aa': 'old11', 'ab': 'old12'}, 'd': 'old3'},
                53: {'a': 'old1', 'b': 'old2', 'c': 'new1', 'd': 'old3'},
                54: {'a': 'new1', 'b': 'old2', 'c': 'new3', 'd': 'old3'},
                55: {'a': 'new1', 'b': 'old2', 'c': {'aa': 'old11', 'ab': 'old12', 'a': 'new11'}, 'd': 'old3'},
                56: {'a': 'new1', 'b': 'old2', 'c': {'aa': 'new11', 'ab': 'old12'}, 'd': 'old3'},
                57: {'a': 'new1', 'b': 'old2', 'c': {'aa': 'old11', 'ab': 'old12', 'a': '<clsItem>'}, 'd': 'new2'},
                90: '<clsItem>',
                91: '<clsItem>',
            },
        }
        # generate the results
        '''
        for destkey, destitem in destdict.items():
            print(f"\x7b{destkey}: {")
            for addkey, additem in adddict.items():
                #print(destitem, ' -- + -- ', additem)
                #print(' -> ',  deepMerge(destitem, additem))
                print(f"{addkey}: {deepMerge(destitem, additem)},")
            print(f"\x7d")
        '''
        # check with result dict
        for destkey, destitem in destdict.items():
            for addkey, additem in adddict.items():
                self.assertEqual(deepMerge(destitem, additem), resdict[destkey][addkey], 'error')


    @settings(max_examples=100)
    @given(tstdata1=f_nesteddict3(), tstdata2=f_nesteddict4())
    def test_filterByProperty1(self, tstdata1, tstdata2):
        orig = tstdata1.copy()
        print('in: ', tstdata1)
        #print(json.dumps(tstdata1, indent=4, sort_keys=True))
        grc.deepMerge(tstdata1, tstdata2)
        print('res: ', tstdata1)
        #print(json.dumps(tstdata1, indent=4, sort_keys=True))
        pass
        #result = cutJsonItem(tstdata1, keylist, default='KEYERROR'):
        #self.assertEqual(orig, tstdata1)

    #@settings(max_examples=50)
    #@given(tstdata=f_nesteddict2())
    #def test_filterByProperty2(self, tstdata):
    #    print('data: ', tstdata)
    #    #print(json.dumps(tstdata, indent=4, sort_keys=True))
    #    pass



'''
    @example(lst1={}, lst2={}, value=1)
    def test_filterByProperty1(self, lst1, lst2, value):
        outlist = grc.filterByProperty(lst1, lst2, value)
        print(inlist)
        print(outlist)
        self.assertEqual(outlist, checklist)
    @given(
        st.dictionaries(
            keys=st.characters(),
            values=st.from_type(type).flatmap(st.from_type).filter(lambda x: not isinstance(x, (type(None), bool))),
            min_size=2, max_size=5),
        st.dictionaries(
            keys=st.text(min_size=1, max_size=10),
            values=st.from_type(type).flatmap(st.from_type).filter(lambda x: not isinstance(x, (type(None), bool))),
            min_size=2, max_size=5))
    @example({}, {})
    def test_filterByProperty(self, lst1, lst2):
        inlist = {**lst1, **lst2}
        propertyname = 'a'
        value = 1
        checklist = lst1
        outlist = grc.filterByProperty(inlist, propertyname, value)
        print(inlist)
        print(outlist)
        self.assertEqual(outlist, checklist)

    @given(st.integers(), st.integers())
    def test_ints_are_commutative(self, x, y):
        assert x + y == y + x


    @given(x=st.integers(), y=st.integers())
    def test_ints_cancel(self, x, y):
        assert (x + y) - y == x


    @given(st.lists(st.integers()))
    def test_reversing_twice_gives_same_list(self, xs):
        # This will generate lists of arbitrary length (usually between 0 and
        # 100 elements) whose elements are integers.
        ys = list(xs)
        ys.reverse()
        ys.reverse()
        assert xs == ys


    @given(st.tuples(st.booleans(), st.text()))
    def test_look_tuples_work_too(self, t):
        # A tuple is generated as the one you provided, with the corresponding
        # types in those positions.
        assert len(t) == 2
        assert isinstance(t[0], bool)
        assert isinstance(t[1], str)
'''

#******************************************************************************
# MAIN
#******************************************************************************
if __name__ == '__main__':
    unittest.main()
