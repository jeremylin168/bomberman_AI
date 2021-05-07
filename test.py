




class test():
    def __init__(self,x):
        self.x = x
tt = 8
n = test(tt)
print(n.x)
u = n
n.x=4
print(u.x)
print(n.x)
print(tt)
print(int(1.9))
ss = 2
for i in range(ss):
    ss+=1
    print(i)
    if ss>=10:
        break