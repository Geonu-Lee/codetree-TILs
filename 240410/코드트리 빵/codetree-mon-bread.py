import sys
from collections import deque

# sys.stdin=open("input.txt")

N, M = list(map(int, sys.stdin.readline().split()))
arr = [[1] * (N+2)] + [[1] + list(map(int, sys.stdin.readline().split())) + [1] for _ in range(N)] + [[1] * (N+2)]
store = [list(map(int, sys.stdin.readline().split())) for _ in range(M)]
store = [[0, 0]] + store
basecamp = set()
for i in range(1, N+1):
    for j in range(1, N+1):
        if arr[i][j] == 1:
            basecamp.add((i, j))
            arr[i][j] = 0

def find(si, sj, dests):
    q = deque()
    v = [[0] * (N+2) for _ in range(N+2)]  # 위에서 arr 를 벽으로 둘러쌓은 형태로 만들기

    q.append((si, sj))
    v[si][sj] = 1
    dest_list = []
    while q:
        nq = deque()
        for ci, cj in q:
            if (ci, cj) in dests:
                dest_list.append((ci, cj))
            else:
                for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    ni, nj = ci + di, cj + dj
                    if v[ni][nj] == 0 and arr[ni][nj] == 0:
                        nq.append((ni, nj))
                        v[ni][nj] = 1
        if len(dest_list) != 0:
            dest_list.sort()
            return dest_list[0]
        q = nq

def solution():
    q = deque()
    time = 1
    arrive = [0] * (M+1)
    stop_list = []
    while time == 1 or q:
        # 편의점으로 1 칸 이동
        nq = deque()
        for ci, cj, m in q:
            if arrive[m] == 0:
                # 상 하 좌 우
                dests = {(ci - 1, cj), (ci + 1, cj), (ci, cj - 1), (ci, cj + 1)}
                ni, nj = find(store[m][0], store[m][1], dests)
                if [ni, nj] == store[m]:  # 원하는 편의점 도착
                    arrive[m] = time  # 도착시간 처리
                    stop_list.append((ni, nj))
                else:
                    nq.append((ni, nj, m))
        q = nq

        # 편의점 도착 처리
        if len(stop_list) != 0:
            for ti, tj in stop_list:
                arr[ti][tj] = 1

        # 베이스캠프로 이동
        if time <= M:
            si, sj = store[time]
            ei, ej = find(si, sj, basecamp)
            basecamp.remove((ei, ej))
            q.append((ei, ej, time)) # 시작점 추가
            arr[ei][ej] = 1  # 이동 불가

        time += 1

    return arrive

arrive = solution()
print(max(arrive))