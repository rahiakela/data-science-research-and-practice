l1 = [3, 6, 9, 12, 15, 18, 21]
l2 = [4, 8, 12, 16, 20, 24, 28]

l3 = [num for num in l1 if num % 2 == 0]
print(l3)

l4 = []
# for i in [*l1, *l2]:
for i in l1 + l2:
    if i % 2 == 0:
        l4.append(i)
print(l4)
# print(l1[1::2])
# print(l2[0::2])
## l3 = [6,12,18,4,12,20,28]

l3 = list()
l3.extend(l1[1::2])
l3.extend(l2[0::2])
# print(l3)

