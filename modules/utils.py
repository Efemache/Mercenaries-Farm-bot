from copy import deepcopy


def update(d, u):
    """Return dictionary updated with values u

    Args:
        d (dict): base dictionary to start with
        u (dict): dictionary with new values

    Returns:
        dict: dictionary with updated values
    """
    r = deepcopy(d)
    for k, v in r.items():
        if type(v) is dict:
            for _k, _v in v.items():
                if _k in u:
                    r[k][_k] = u[_k]
        elif k in u:
            r[k] = u[k]
    return r
