import unittest
from mystery import mystery


class TestMystery(unittest.TestCase):
    '''
        i)   case 1: n = 1, v = 1
        ii)  case 2: n= 2, v = 23 (Note: 23 is derived as 1 + 22)
        iii) case 3: n= 3, v = 356 (Note: 356 is derived as 1+22+333)
        iv)  case 4: n= 4, v = 4800 (Note: 4800 is derived as 1+22+333+4444)
    '''

    def test_one(self):
        self.assertEqual(1, mystery(1))

    def test_two(self):
        self.assertEqual(23, mystery(2))

    def test_three(self):
        self.assertEqual(356, mystery(3))

    def test_four(self):
        self.assertEqual(4800, mystery(4))


if __name__ == '__main__':
    unittest.main(verbosity=2)
