def linear(t):
    return t


def easeInQuad(t):
    return t * t


def easeOutQuad(t):
    return 1 - (1 - t) * (1 - t)


def easeInOutQuad(t):
    if t < 0.5:
        return 2 * t * t
    return 1 - pow(-2 * t + 2, 2) / 2


def easeInCubic(t):
    return t * t * t


def easeOutCubic(t):
    return 1 - pow(1 - t, 3)


def easeInOutCubic(t):
    if t < 0.5:
        return 4 * t * t * t
    return 1 - pow(-2 * t + 2, 3) / 2
