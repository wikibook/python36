def divide(a, b):
    return a / b

try:
    c = divide(5, 2)
except ZeroDivisionError:
    print('두 번째 인자는 0이어서는 안 됩니다.')
except TypeError:
    print('모든 인자는 숫자여야 합니다.')
except:
    print('ZeroDivisionError, TypeError를 제외한 다른 에러')
else:
    print('Result: {0}'.format(c))
finally:
    print('항상 finally 블록은 수행됩니다.')