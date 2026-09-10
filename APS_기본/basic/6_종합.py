# 6단계. 종합 — 열린 가게 중 가장 가까운 곳을 골라 방향과 걸리는 시간 구하기
import math

places = [(30, 40), (60, 80), None, (90, 20), (10, 90), (34, 37)]

# 1) 내 위치
me = places[0]

# 2) 목적지 = 열린 가게 중 가장 가까운 가게
best_i = -1
best_dist = 99999
for i in range(1, 6):
    if places[i] is None:
        continue
    d = math.sqrt((places[i][0] - me[0]) ** 2 + (places[i][1] - me[1]) ** 2)
    if d < best_dist:
        best_dist = d
        best_i = i
goal = places[best_i]

# 3) 두 튜플로 방향
dx = goal[0] - me[0]
dy = goal[1] - me[1]
angle = math.degrees(math.atan2(dx, dy))
if angle < 0:
    angle += 360

# 4) 거리로 걸리는 시간 (1분에 5씩 이동한다고 가정)
minutes = best_dist / 5

print("내 위치:", me)
print("목적지:", goal)
print("방향:", round(angle, 2), "도")     # 126.87
print("걸리는 시간:", round(minutes, 1), "분")

# ✏️ 연습: 목적지를 "가장 가까운 가게" 대신 "열린 가게 중 번호가 가장 작은 가게" 로 바꿔 보세요
