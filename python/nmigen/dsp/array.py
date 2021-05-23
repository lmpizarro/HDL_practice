a = [1, 2,3]

b = 4

y = a [0]
for i,e in enumerate(a):
    if i > 0:
        a[i-1] = e
a[i] = b

print(y)
print(a)