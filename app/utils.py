def removekey_oop(d, key):
    r = dict(d)
    del r[key]
    return r


def calculate_results_summary(mean, mn):
    if (mn and mn <= .15):
        return 10 if mean <= .15 else 8 

    return 0

