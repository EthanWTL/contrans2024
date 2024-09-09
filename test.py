import copy


orig = [[1, 2, 3], [4, 5, 6]]
not_copy = orig
s_copy = orig.copy()
d_copy = copy.deepcopy(orig)


orig[1][1] = 3
not_copy[0][0] = 2
s_copy[0][2] = 10
d_copy[1][2] = 15

print(orig)
print(not_copy)
print(s_copy)
print(d_copy)


