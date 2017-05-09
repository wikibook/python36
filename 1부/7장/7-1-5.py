def divide(a, b):
    return a / b

try:
    c = divide(5, 0)
except (ZeroDivisionError, OverflowError, FloatingPointError):
    print('수치 연산 관련 에러입니다.')
except TypeError:
    print('모든 인자는 숫자여야 합니다.')
except Exception:
    print('음~ 무슨 에러인지 모르겠어요!!')