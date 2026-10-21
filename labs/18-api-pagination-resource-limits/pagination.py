DATA=list(range(40))
def page(offset,limit):
    if type(offset) is not int or type(limit) is not int: raise ValueError("type")
    if offset<0 or not 1<=limit<=10: raise ValueError("range")
    return DATA[offset:offset+limit]
if __name__=="__main__":
    print(page(0,5))
    for args in [(0,999),(-1,2)]:
        try:page(*args)
        except ValueError as e:print("rejected",e)
