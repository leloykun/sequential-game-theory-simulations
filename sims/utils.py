def to_ordinal(n):
    return str(n) + ("th" if 4 <= n % 100 <= 20 else {
        1: "st",
        2: "nd",
        3: "rd"
    }.get(n % 10, "th"))


def process(params):
    if isinstance(params, str):
        params = params.split()
    assert type(params) in [list, tuple]
    return list(map(int, params))
