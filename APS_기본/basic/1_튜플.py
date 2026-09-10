# 1단계. 튜플 하나 = 지도 위 한 지점의 위치 (x, y)

point = (30, 40)

print(point)        # (30, 40)
print(point[0])     # 30  ← x
print(point[1])     # 40  ← y

# 언패킹: 튜플을 변수 두 개로 한 번에 풀기
x, y = point
print("x =", x)
print("y =", y)

# ✏️ 연습: 아래 지점의 x 와 y 를 출력해 보세요
point2 = (72, 15)


