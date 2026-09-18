a = 13
b = bin(a)
c = oct(a)
d = hex(a)
print(b, c, d)
print(type(b))

# 다시 10진수로 b, c, d 값을 바꿔보자
print(int(b, 2))
print(int(c, 8))
print(int(d, 16))

# 10진수 17을 3진수로 바꾸기
a = 17
trans=""
while a!=0:
    rest=a%3
    trans+=str(rest)
    a//=3
answer=trans[::-1]
print(answer)

result=int(answer,3)
print(result)

print(13&9) # & empersand => AND
print(13|9) # | vertical bar => OR
print(13^9) # ^ caret => XOR
print(10<<2)
print(10>>2)