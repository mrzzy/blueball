from c import *
from pprint import pprint

if __name__ == '__main__':
    s0 = (0, 'z0')
    a1 = (1, 'a1')
    b1 = (1, 'b1')
    a3 = (3, 'a3')
    b4 = (4, 'b4')

    txs = [a1,b1,b4,a3]
    pprint(list(server_step(s0, txs)))