a = [0]*100


L = 25
L1 = L2 = 10
Lc = L - 2* L1

def idea1():

    filter_trap = [1]*L1 + [0] * Lc + [-1] * L2
    filter_ = []
    for _ in range(10):
        a.insert(0,0)
        b = [filter_trap[i] * a[i] for i in range(len(filter_trap))]
        filter_.insert(0,(sum(b) * .1))

    for _ in range(40):
        a.insert(0,1)
        b = [filter_trap[i] * a[i] for i in range(len(filter_trap))]
        filter_.insert(0,(sum(b) * .1))

    for _ in range(40):
        a.insert(0,4)
        b = [filter_trap[i] * a[i] for i in range(len(filter_trap))]
        filter_.insert(0, (sum(b) * .1))

    print(filter_)


def idea3():

    filter_trap1 = [1]*L1 
    filter_trap2 = [-1] * L2
    filter_ = []

    for _ in range(10):
        a.insert(0,0)
        b = [filter_trap1[i] * a[i] for i in range(len(filter_trap1))]
        c = [filter_trap2[i] * a[i+ Lc + L1] for i in range(len(filter_trap2))]
        filter_.insert(0, (sum(b)  + sum(c))* .1 )



    for _ in range(40):
        a.insert(0,1)
        b = [filter_trap1[i] * a[i] for i in range(len(filter_trap1))]
        c = [filter_trap2[i] * a[i+ Lc + L1] for i in range(len(filter_trap2))]
        filter_.insert(0, (sum(b)  + sum(c))* .1 )





    for _ in range(40):
        a.insert(0,4)
        b = [filter_trap1[i] * a[i] for i in range(len(filter_trap1))]
        c = [filter_trap2[i] * a[i+ Lc + L1] for i in range(len(filter_trap2))]
        filter_.insert(0, (sum(b)  + sum(c))* .1 )




    print(filter_)

idea3()