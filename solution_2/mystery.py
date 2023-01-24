def mystery(n: int) -> int:
    '''
        n = 1, m = 1
        n = 2, m = 22
        n = 3, m = 333
        n = 4, m = 4444
    '''
    def helper(m: int) -> int:
        str_m = str(m)
        return int(str_m * m)

    '''
        i)   case 1: n = 1, v = 1
        ii)  case 2: n = 2, v = 23 (Note: 23 is derived as 1 + 22)
        iii) case 3: n = 3, v = 356 (Note: 356 is derived as 1+22+333)
        iv)  case 4: n = 4, v = 4800 (Note: 4800 is derived as 1+22+333+4444)
    '''
    v = 0
    for i in range(1, n+1):
        v += helper(i)

    return v
