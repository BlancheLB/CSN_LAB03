import random

def random_permutation(x,n):
    m=n
    while(m>=2):
        i=random.randint(1,m)
        temp=x[i]
        x[i]=x[m]
        x[m]=temp
        m=m-1
    return x

    
