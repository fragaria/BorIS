

# https://stackoverflow.com/a/35795334/2047472
def median(array):
    """Calculate median of the given list.
    """
    # TODO: use statistics.median in Python 3
    array = sorted(array)
    half, odd = divmod(len(array), 2)
    if odd:
        return array[half]
    return (array[half - 1] + array[half]) / 2.0

