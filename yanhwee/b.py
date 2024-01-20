from collections import deque
from operator import itemgetter
from typing import Generic, List, Tuple, Union


Time = float
Input = Generic['Input']
State = Generic['State']

def update(state: State, input: Input) -> State:
    pass

# def step(
#         tz: Union[Tuple[Time,Input],Tuple[Time,State]],
#         txs: deque[Tuple[Time,Input]],
#         tys: deque[Tuple[Time,State]]):
#     time = itemgetter(0)
#     val = itemgetter(1)

# def step(
#         tx: Tuple[Time,Input],
#         txs: deque[Tuple[Time,Input]],
#         tys: deque[Tuple[Time,State]]):
#     pass

def step_state(
        ty: Tuple[Time,State],
        txs: deque[Tuple[Time,Input]],
        tys: deque[Tuple[Time,State]]):
    time = itemgetter(0)
    val = itemgetter(1)
    
    # rollback state
    ro_ty = ...

    # rollback inputs
    re_txs = ...

    # replay
    ...

    # append inputs (not needed)

    # append states (yes needed)

    return n_ty

def step(
        tx: Tuple[Time,Input],
        txs: deque[Tuple[Time,Input]],
        tys: deque[Tuple[Time,State]]):
    
    # replay 1 input
    n_y = update(tys[-1], tx)
    
    # append inputs
    ...

    # append states
    ...