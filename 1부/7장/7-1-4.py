def divide(a, b):
    return a / b
try:
    c = divide(5, "af")
except TypeError as e:
    print('에러: ', e.args[0])
except Exception:
    print('음~ 무슨 에러인지 모르겠어요!!')