def foo(x):
    assert type(x) == int, "Input value must be integer"
    return x * 10

ret = foo("a")
print(ret)