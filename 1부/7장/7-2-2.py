def RaiseErrorFunc():
    raise NameError("NameError의 인자")

def PropagateError():
    try:
        RaiseErrorFunc()
    except:
        print("에러 전달 이전에 먼저 이 메시지가 출력됩니다.")
        raise

PropagateError()