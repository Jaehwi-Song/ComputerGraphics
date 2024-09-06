import numpy as np

# A
M = np.arange(2,27)
print(M)
print()

# B
M = M.reshape(5,5)
print(M)
print()

# C
M[1:4, 1:4] = 0
print(M)
print()

# D
M = M @ M
print(M)
print()

# E
v = M[0, :]
print(np.sqrt(np.sum(v**2)))
print()