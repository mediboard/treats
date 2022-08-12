def removekey_oop(d, key):
    r = dict(d)
    del r[key]
    return r


def calculate_results_summary(mean, mn):
    if (mn <= .15):
        return 'strong' if mean <= .15 else 'mixed'

    return 'weak'

