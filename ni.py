yan = list(map(int, input().split('.')))
ip1 = list(map(int, input().split('.')))
ip2 = list(map(int, input().split('.')))
a=[i > 255 or i < 0 for i in yan + ip1 + ip2]
print(a)
print(sum(a))
if sum(a):
    print(1)