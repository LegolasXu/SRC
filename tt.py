mid = 0
x = int(input("x>"))
y = int(input("y>"))
while True:
    if x > y:
        mid = y
        if x/mid == int(x/mid):
            print(mid)
            break
        else:
            mid = mid - 1
    if x == y:
        mid = x
        print(mid)
        break
    if x < y:
        mid = x
        if y/mid == int(y/mid):
            print(mid)
            break
        else:
            mid -= 1
    
    
