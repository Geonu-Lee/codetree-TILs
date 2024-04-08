import sys

N, M, K = list(map(int, sys.stdin.readline().split()))
arr = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]
users = [list(map(int, sys.stdin.readline().split())) for _ in range(M)]
exit_i, exit_j = list(map(int, sys.stdin.readline().split()))
exit_i, exit_j = exit_i - 1, exit_j - 1

arr[exit_i][exit_j] = -11
for index in range(len(users)):
    i, j = users[index]
    arr[i-1][j-1] -= 1

answer = 0
count = M

def get_distance(x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)

def find_square(arr, exit_i, exit_j):
    m = N
    for i in range(N):
        for j in range(N):
            if -11 < arr[i][j] < 0:
                m = min(m, max(abs(i-exit_i), abs(j-exit_j)))
    for si in range(N - m):
        for sj in range(N - m):
            if si <= exit_i <= si + m and sj <= exit_j <= sj + m:
                for i in range(si, si + m + 1):
                    for j in range(sj, sj + m + 1):
                        if -11 < arr[i][j] < 0:
                            return si, sj, m+1
def find_exit(arr):
    for i in range(N):
        for j in range(N):
            if arr[i][j] == -11:
                return i, j
def rotation(arr, si, sj, length):
    partial_arr = []
    for i in range(si, si + length):
        partial_arr.append(arr[i][sj:sj + length])
    new_90 = [[0] * length for _ in range(length)]
    for i in range(length):
        for j in range(length):
            if partial_arr[i][j] > 0:
                partial_arr[i][j] -= 1
            new_90[j][length - i - 1] = partial_arr[i][j]
    for i in range(len(new_90)):
        arr[i + si][sj:sj + length] = new_90[i]
    return arr


for t in range(K):
    narr = [x[:] for x in arr]  # copy
    for ci in range(N):
        for cj in range(N):
            if -11 < arr[ci][cj] < 0:  # 사람일때
                distance = get_distance(exit_i, exit_j, ci, cj)
                # 상하좌우
                for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    ni, nj = ci + di, cj + dj
                    if 0 <= ni < N and 0 <= nj < N and arr[ni][nj] <= 0 and distance > get_distance(exit_i, exit_j, ni, nj):
                        answer += arr[ci][cj]
                        narr[ci][cj] -= arr[ci][cj]
                        if arr[ni][nj] == -11:
                            count += arr[ci][cj]
                        else:
                            narr[ni][nj] += arr[ci][cj]
                        break
    arr = narr
    if count == 0:  # 모두 탈출
        break

    # square 찾기
    si, sj, length = find_square(arr, exit_i, exit_j)
    # 회전
    arr = rotation(arr, si, sj, length)

    exit_i, exit_j = find_exit(arr)

print(-answer)
print(exit_i + 1, exit_j + 1)