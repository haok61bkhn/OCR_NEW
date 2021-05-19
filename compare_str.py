import numpy as np
def compare_str(s1,s2):
    n1=len(s1)
    n2=len(s2)
    f=np.zeros((n1+1,n2+1))
    f[0][0]=0
    if(s1[0]!=s2[0]):
        f[1][1]=1
    f[0][1]=1
    f[1][0]=1
    for i in range(0,n1):
        for j in range(0,n2):
            if(s1[i]==s2[j]):
                f[i+1][j+1]=f[i][j]
            else:
                f[i+1][j+1]=min(f[i][j],f[i+1][j],f[i][j+1])+1
    return f[-1][-1]
