# 재귀 연습
# 피보나치로 재귀 연습하기
# 1 1 2 3 5 8 13 21 34....
# f(n) = f(n-1) + f(n-2)
# n 번째 피보나치 항을 반환하는 함수!

def fibo(n):
    # 피보나치의 1항과 2항은 계산 없이 구할 수 있음: base
    if n <= 2:
        return 1

    return fibo(n-1) + fibo(n-2)

print(fibo(6))