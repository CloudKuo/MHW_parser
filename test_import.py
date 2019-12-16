import to_import

def g(y=1):
    return y**2


def f(x, **dk):
    return x * g(**dk)


if __name__ == "__main__":
    a = to_import.test()
    print(a.p)
    a.countab(4, 3)
    to_import.just_print("dadsd")
    print(f(10, y=2))