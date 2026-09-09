# 스택을 구현해봅시다
# 진짜는아니고...파이썬 리스트 활용해서..
class Stack:
    def __init__(self, N):
        self.s = [None] * N #진짜 요소들이 저장될 배열
        self.top = -1   #초기값은 -1
        self.length = N
    # 스택이 할 수 있는 기능..
    def push(self,value):
        # top 1증가 시키고
        # 그 위치에 value 넣기
        if not self.is_full():
            self.top += 1
            self.s[self.top] = value
        else:
            print('스택이 가득 찼습니다.')

    def pop(self):
        if not self.is_empty():
            value = self.s[self.top]
            self.top -= 1
            return value
        else:
            print('스택이 비었습니다.')

    # 가득 찼는지 확인...
    def is_full(self):
        if self.top == self.length-1:
            return True
        return False

    def is_empty(self):
        if self.top == -1:
            return True
        return False



stack = Stack(5)

stack.push(3)
stack.push(5)
stack.push(4)
stack.push(2)
stack.push(1)
stack.push(1)
stack.push(1)
stack.push(1)


print(stack.pop())
print(stack.pop())
print(stack.pop())
print(stack.pop())
print(stack.pop())



