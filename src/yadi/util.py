import itertools


### From doc of itertools

def find(iterable, default=None, pred=None):
    '''
    Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item
    for which pred(item) is true.
    '''
    # find([a,b,c], x) --> a or b or c or x
    # find([a,b], x, f) --> a if f(a) else b if f(b) else x
    return next(filter(pred, iterable), default)


### From SRFI-1

def list_index(iterable, default=None, pred=None):
    '''
    Return left-most index in list satisfying `pred`.

    This is a lambda version of `List.index`.
    '''
    # list_index(['a', 'b', 'c'], None, lambda s: s == 'b')
    # => 1
    # list_index(['a', 'b', 'c'], 100, lambda s: s == 'x')
    # => 100
    return find(zip(itertools.count(start=0, step=1), iterable), default=(default,), pred=lambda x: pred(x[1]))[0]
