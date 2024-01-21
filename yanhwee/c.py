from collections import deque
from functools import partial, reduce
from itertools import chain, dropwhile
from operator import itemgetter, lt
from typing import TypeVar, Iterable, Tuple, Union

Time = float
Input = TypeVar('Input')
State = TypeVar('State')
TimedInput = Tuple[Time, Input]
TimedState = Tuple[Time, State]

# Getters for TimedInput & TimedState
time = itemgetter(0)
val = itemgetter(1)

# Interface
def update(state: State, input: Input) -> State:
    return (input, state)

# Utilities
def compose(*fs):
    compose2 = lambda f, g: lambda *args: f(g(*args))
    return reduce(compose2, fs)

# Timeline
def make_timeline(*args, **kwargs):
    return deque(*args, **kwargs)

def rollback_retrieve_state(tys: deque[TimedState], t: Time) -> TimedState:
    return next(dropwhile(
        compose(
            partial(lt, t),
            time),
        reversed(tys)))

def rollback_pop_inputs(txs: deque[TimedInput], t: Time) -> deque[TimedInput]:
    re_txs = deque()
    while txs and t < time(txs[-1]):
        re_txs.append(txs.pop())
    return iter(re_txs)

def play(y, xs):
    return reduce(update, xs, y)

# Server Step
def server_step_input(
        tx: Tuple[Time,Input],
        txs: deque[Tuple[Time,Input]],
        tys: deque[Tuple[Time,State]]):
    
    t = time(tx)
    
    # rollback
    ro_y = val(rollback_retrieve_state(tys, t))
    ro_txs = rollback_pop_inputs(txs, t)

    # replay
    re_txs = list(chain([tx], ro_txs))
    re_xs = map(val, re_txs)
    n_y = play(ro_y, re_xs)
    n_ty = (time(re_txs[-1]), n_y)

    # remember
    txs.extend(re_txs)
    tys.append(n_ty)

    return n_ty

def server_step(ty: TimedState, txs: Iterable[TimedInput]):
    mem_txs = make_timeline()
    mem_tys = make_timeline([ty])

    for tx in txs:
        yield server_step_input(tx, mem_txs, mem_tys)

# Client Step
def client_step_input(
        tx: Tuple[Time,Input],
        txs: deque[Tuple[Time,Input]],
        tys: deque[Tuple[Time,State]]):
    
    # rollback 1
    ro_y = val(tys[-1])

    # replay 1
    n_y = update(ro_y, val(tx))
    n_ty = (time(tx), n_y)

    # remember 1
    txs.append(tx)
    tys.append(n_ty)

    return n_ty

def client_step_state(
        ty: Tuple[Time,State],
        txs: deque[Tuple[Time,Input]],
        tys: deque[Tuple[Time,State]]):
    
    t = time(ty)
    y = val(ty)
    
    # rollback
    ro_txs = rollback_pop_inputs(txs, t)

    # replay
    re_xs = list(map(val, ro_txs))
    n_y = play(y, re_xs)
    n_ty = (time(re_xs[-1]), n_y)

    # remember
    tys.append(n_ty)

    return n_ty

def client_step(
        ty: TimedState,
        tzs: Iterable[Union[TimedInput, TimedState]]):
    mem_txs = make_timeline()
    mem_tys = make_timeline([ty])

    for tz in tzs:
        client_step = (
            client_step_input
            if type(tz) is TimedInput else
            client_step_state)
        
        yield client_step(tz, mem_txs, mem_tys)