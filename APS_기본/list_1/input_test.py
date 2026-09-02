str_num1 = '1 2 3 4 5'   #숫자들 사이에 띄어쓰기 포함
a = str_num1.split()    # ['1','2','3','4','5']
b = list(map(int,a))  # 각 요소에 int 적용
print(b)    # [1, 2, 3, 4, 5]
# data = list(map(int,input().split()))
str_num2 = '12345'
# a = str_num2    # ['12345']
# map(함수,덩어리)  : 덩어리의 각 요소에 함수 적용해라
b = list(map(int,str_num2))  # 각 요소에 int 적용
print(b)
# 1 2 3 4 5   >>> map(int,input().split())
# 12345 >>>> map(int,input())