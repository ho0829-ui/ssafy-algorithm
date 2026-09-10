# 5단계. 튜플 두 개로 방향(각도) 구하기
#   나침반 방향: 북쪽 0°, 동쪽 90°, 남쪽 180°, 서쪽 270° (시계 방향)
#   → math.atan2(dx, dy)  ※ 인자 순서가 dx, dy 인 것에 주의
import math

me = (30, 40)
goal = (60, 80)

x1, y1 = me
x2, y2 = goal
dx = x2 - x1
dy = y2 - y1

angle = math.degrees(math.atan2(dx, dy))
if angle < 0:
    angle += 360        # 음수면 360 더해서 0~360 으로

print("방향:", angle)    # 36.87...  (북동쪽)

# 방향 확인용 예시 — 예상한 값과 같은지 보세요
tests = [
    ((0, 0), (0, 10)),    # 북 → 0
    ((0, 0), (10, 0)),    # 동 → 90
    ((0, 0), (0, -10)),   # 남 → 180
    ((0, 0), (-10, 0)),   # 서 → 270
]
for start, end in tests:
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    a = math.degrees(math.atan2(dx, dy))
    if a < 0:
        a += 360
    print(start, "→", end, ":", a)

# ✏️ 연습: (30, 40) 에서 (0, 10) 을 바라보는 방향을 계산해 보세요 (예상: 225, 남서쪽)


