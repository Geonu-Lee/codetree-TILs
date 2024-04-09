import sys
from collections import deque

N, M, K = list(map(int, sys.stdin.readline().split()))
arr = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]
turn_list = [[0] * M for _ in range(N)]

def bfs(si, sj, ei, ej):
    q = deque()
    v = [[[] for _ in range(M)] for _ in range(N)]
    q.append((si, sj))
    v[si][sj] = (si, sj)
    damage = arr[si][sj]

    while q:
        ci, cj = q.popleft()
        if (ci, cj) == (ei, ej):  # 공격 대상자에 도착
            arr[ei][ej] = max(0, arr[ei][ej] - damage)
            while True:
                ci, cj = v[ci][cj]
                if (ci, cj) == (si, sj):
                    return True
                arr[ci][cj] = max(0, arr[ci][cj] - damage//2)
                fight_set.add((ci, cj))
        # 우하좌상
        for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            ni, nj = (ci + di) % N, (cj + dj) % M
            if len(v[ni][nj]) == 0 and arr[ni][nj] > 0:
                q.append((ni, nj))
                v[ni][nj] = (ci, cj)
    return False

def bomb(si, sj, ei, ej):
    damage = arr[si][sj]
    arr[ei][ej] = max(0, arr[ei][ej] - damage)
    dis = [-1, 0, 0, 1, -1, 1, 1, -1]
    djs = [0, -1, 1, 0, -1, 1, -1, 1]
    for di, dj in zip(dis, djs):
        ni, nj = (ei + di) % N, (ej + dj) % M
        if (ni, nj) != (si, sj):
            arr[ni][nj] = max(0, arr[ni][nj] - damage // 2)
            fight_set.add((ni, nj))

for turn in range(1, K+1):
    # 공격자 선정
    mn, mx, si, sj = 5001, 0, -1, -1  # 초기화
    for i in range(N):
        for j in range(M):
            if arr[i][j] == 0: continue
            if arr[i][j] < mn or (arr[i][j] == mn and turn_list[i][j] > mx) or \
              (arr[i][j] == mn and turn_list[i][j] == mx and si + sj < i + j) or \
              (arr[i][j] == mn and turn_list[i][j] == mx and si + sj == i + j and sj < j):
                mn, mx, si, sj = arr[i][j], turn_list[i][j], i, j
    # 공격 대상자 선정
    mx, mn, ei, ej = 0, 1001, N, M
    for i in range(N):
        for j in range(M):
            if arr[i][j] == 0 : continue
            if arr[i][j] > mx or (arr[i][j] == mx and turn_list[i][j] < mn) or \
              (arr[i][j] == mx and turn_list[i][j] == mn and ei + ej > i + j) or \
              (arr[i][j] == mx and turn_list[i][j] == mn and ei + ej == i + j and ej > j):
                mx, mn, ei, ej = arr[i][j], turn_list[i][j], i, j

    # 공격자 핸디캡
    arr[si][sj] += (N+M)
    turn_list[si][sj] = turn
    fight_set = set()
    fight_set.add((si, sj))
    fight_set.add((ei, ej))

    # 레이저 공격
    if not bfs(si, sj, ei, ej):
        bomb(si, sj, ei, ej)  # 레이저 경로가 없을 때

    # 포탑 정비
    for i in range(N):
        for j in range(M):
            if arr[i][j] > 0 and (i, j) not in fight_set:
                arr[i][j] += 1

    count = N*M   # 전체 수
    for lst in arr:
        count -= lst.count(0)   # 포탑 부셔진거 카운트
    if count <= 1:   # 포탑이 1 이하일때 탈출
        break
print(max(map(max, arr)))