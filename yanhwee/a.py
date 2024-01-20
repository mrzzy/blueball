from collections import deque
from functools import partial, reduce
from itertools import dropwhile
from operator import itemgetter, lt
from typing import Generic, Tuple

Time = float
Input = Generic['Input']
State = Generic['State']

def update(state: State, input: Input) -> State:
    pass

def compose(*fs):
    compose2 = lambda f, g: lambda *args: f(g(*args))
    return reduce(compose2, fs)

def step(
        tx: Tuple[Time,Input],
        txs: deque[Tuple[Time,Input]],
        tys: deque[Tuple[Time,State]]):
    time = itemgetter(0)
    val = itemgetter(1)

    # rollback state
    ro_ty = next(dropwhile(
        compose(
            partial(lt, time(tx)),
            time),
        reversed(tys)))

    # rollback inputs
    re_txs = deque([tx])
    while time(tx) < time(txs[-1]):
        re_txs.append(txs.pop())
    
    # replay
    n_y = reduce(update, val(ro_ty), map(val, re_txs))
    n_ty = (time(re_txs[-1]), n_y)

    # append inputs
    txs.extend(re_txs)

    # append states
    tys.append(n_ty)

    return n_ty

def steps(txs):
    mem_txs = deque()
    mem_tys = deque()

    for tx in txs:
        yield step(tx, mem_txs, mem_tys)