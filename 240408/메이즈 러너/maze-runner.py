import sys

N, M, K = list(map(int, sys.stdin.readline().split()))
miro_map = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]
users = [list(map(int, sys.stdin.readline().split())) for _ in range(M)]
exit_i, exit_j = list(map(int, sys.stdin.readline().split()))
exit_i, exit_j = exit_i - 1, exit_j - 1

for index in range(len(users)):
    i, j = users[index]
    users[index] = [i-1, j-1]
    miro_map[i-1][j-1] = -2   # user 위치 miro map 에 저장
users = [[-1, -1]] + users  # index 1 부터 하기 위해서

# 참가자 탈출 여부
# user_exit = [1] * (M+1)   # 1 - 미탈출
# user_exit[0] = 0

# 참가자 이동 거리 초기화
answer = 0

# 출구 위치 표시 (-1)
miro_map[exit_i][exit_j] = -1

# 거리 측정
def get_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def get_square(arr, users, exit_i, exit_j):
    min_value = N  # 변의 최소 길이
    for index in range(1, M+1):
        i, j = users[index]
        if not i == -1:
            min_value = min(min_value, max(abs(i-exit_i), abs(j-exit_j)))
    for si in range(N-min_value):
        for sj in range(N-min_value):
            if si <= exit_i <= si + min_value and sj <= exit_j <= sj + min_value:
                for i in range(si, si+min_value+1):
                    for j in range(sj, sj+min_value+1):
                        if arr[i][j] == -2:
                            return si, sj, min_value+1
def rotation(arr, si, sj, L):
    partial_arr = []
    for i in range(si, si + L):
        partial_arr.append(arr[i][sj:sj+L])
    new_90 = [[0] * L for _ in range(L)]
    for i in range(L):
        for j in range(L):
            if partial_arr[i][j] > 0:
                partial_arr[i][j] -= 1
                partial_arr[i][j] = max(0, partial_arr[i][j])
            new_90[j][L-i-1] = partial_arr[i][j]
    # for i in range(si, si + L):
    #     arr[i][sj:sj+L] = new_90[i]
    for i in range(len(new_90)):
        arr[i + si][sj:sj + L] = new_90[i]
    return miro_map

def find_exit(arr):
    for i in range(N):
        for j in range(N):
            if arr[i][j] == -1:
                return i, j

def find_users(miro_map):
    users = [[-1] * 2 for _ in range(M + 1)]
    index = 1
    for i in range(N):
        for j in range(N):
            if miro_map[i][j] // (-2) > 0:
                users[index] = [i, j]
                index += 1
    return users
# K 초 반복
for turn in range(1, K+1):
    # 참가자가 모두 탈출했을 시 break
    check = 0
    for user in users:
        if user[-1] == -1:
            pass
        else:
            check += 1
    if check == 0:
        break
    # 참가자 이동 여부 판단
    user_move = [[0] * 2 for _ in range(M + 1)]
    # 참가자 찾기
    for index in range(1, M+1):
        ui, uj = users[index]
        if ui == -1:
            continue
        # 기존 위치에서 출구까지의 거리 측정
        min_distance = get_distance(ui, uj, exit_i, exit_j)
        # 상하좌우 판단
        min_list = []
        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ni, nj = ui + di, uj + dj
            if 0 <= ni < N and 0 <= nj < N and miro_map[ni][nj] <= 0:
                distance = get_distance(ni, nj, exit_i, exit_j)
                # 움직였을 때 기존 거리보다 가까우면 리스트 생성
                if min_distance > distance:
                    min_distance = distance
                    min_list = [(ni, nj, di, dj)]
                elif min_distance == distance: # 같으면 리스트에 추가
                    min_list.append((ni, nj, di, dj))
        # 리스트 가장 앞에 있는 것을 기준으로 이동 (없을 경우엔 이동 x)
        if len(min_list) == 0:
            continue
        ni, nj, di, dj = min_list[0]
        user_move[index] = [di, dj]

    # 참가자 동시 이동
    for index in range(1, M+1):
        # 기존 위치 삭제
        ui, uj = users[index]
        if ui == -1:
            continue
        count = miro_map[ui][uj] // (-2) # 기존에 있던 위치에서 참가자 수 확인
        miro_map[ui][uj] = 0
        di, dj = user_move[index]
        ni, nj = ui + di, uj + dj
        # 참가자 이동 거리 처리
        if not abs(di-dj) == 0:
            answer += count
        # 출구 도착시
        if miro_map[ni][nj] == -1:
            # user_exit[index] = 0
            users[index] = [-1, -1]
            continue
        users[index] = [ni, nj]  # user 정보 업데이트
        miro_map[ni][nj] += -2  # 이동한 위치에 user 저장

    # 출구와 참가자를 포함한 정사각형 설계
    si, sj, L = get_square(miro_map, users, exit_i, exit_j)

    # 정사각형 추출, 90도 회전, 벽 내구도 1 감소
    miro_map = rotation(miro_map, si, sj, L)

    exit_i, exit_j = find_exit(miro_map)
    users = find_users(miro_map)
print(answer)
print(exit_i+1, exit_j+1)