import time
def a():
    F = 15000000000
    di = 2000000
    us = 30000000
    ulist = [300000, 700000, 2000000]
    nlist = [10, 100, 1000]
    print("u\t\t\tN\t\tF/us\t\tF/di\tNF/(us+sum(ui))\t\tfinal")
    for u in ulist:
        for n in nlist:
            r1 = F/us
            r2 = F/di
            r3 = n*F/(us+n*u)
            r4 = max(r1,r2,r3)
            print("%5d\t%5d\t%10.1f\t%8.1f\t%8.1f\t\t%10.1f"%(u,n,r1,r2,r3,r4))

    print("u\t\t\tN\t\tNF/us\t\tF/di\t\t\tfinal")
    for u in ulist:
        for n in nlist:
            r1 = n*F / us
            r2 = F / di
            r4 = max(r1, r2)
            print("%5d\t%5d\t\t%8.1f\t%8.1f\t%10.1f" % (u, n, r1, r2, r4))
if __name__ == "__main__":

    print(a())