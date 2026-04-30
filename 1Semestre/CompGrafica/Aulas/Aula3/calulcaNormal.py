def calcula(a,b,c):
    A = b[0]-a[0], b[1] - a[1], b[2]- a[2]
    B = c[0]-a[0], c[1] - a[1], c[2]- a[2]

    nx = (A[1] * B[2]) - (A[2] * B[1])
    ny = (A[2] * B[0]) - (A[0] * B[2])
    nz = (A[0] * B[1]) - (A[1] * B[0])

    comp = math.sqrt(nx**2 + ny**2 + nz**2)
    vx = nx / comp
    vy = ny / comp
    vz = nz / comp
    return (vx, vy, vz)

import math
A = (0.0,  1.0,  0.0)
B = (1.0, -1.0, -1.0)
C= (-1.0, -1.0, -1.0)
print (calcula(A,B,C))
# resultado (0.0, 0.4472135954999579, -0.8944271909999159)