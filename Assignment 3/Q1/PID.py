import control

def step(lo, hi, step):
    result = []
    while lo < hi:
        result.append(lo)
        lo += step
    return result


def evaluate_transfer_fn(Kp, Ti, Td):
    G = Kp * control.TransferFunction([Ti*Td,Ti,1], [Ti, 0]) # compute G

    F = control.TransferFunction(1,[1,6,11,6,0]) # transfer function

    sys = control.feedback(control.series(G,F),1)

    t = step(0, 100, 0.01)

    sysinf = control.step_info(sys, t) # computes e(t)

    T,y = control.step_response(sys, t)

    # ise is (y-1) ^ 2
    return sum((y-1) **2)

