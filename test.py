




class test():
    def __init__(self,x):
        self.x = x
    def copy(self):
        tt=test(self.x)
        return tt

n = test(8)
u = n.copy()
u.x-=1
print(n.x)
print(u.x)
