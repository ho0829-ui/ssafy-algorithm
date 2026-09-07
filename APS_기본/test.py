arr = [2,5,6,1,4,3,7,9,8]
# 코드
# 중복있는지 없는지 보기

# 하나씩 보기
# 저장한 숫자중에 지금 보는 숫자가 있는지 확인
# 내가 본 숫자 저장
check = []
for i in range(len(arr)):
    # arr[i]
    # check안에 arr[i]가 있는지 없는지 검사
    if arr[i] in check:
        print("중복있음")
        break
    else:
        check.append(arr[i])

print("끝!")

