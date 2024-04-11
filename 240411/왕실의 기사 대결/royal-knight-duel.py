import sys
from collections import deque

# sys.stdin = open("input.txt")

L, N, Q = list(map(int, sys.stdin.readline().split()))
# 2(벽) 으로 padding
arr = [[2] * (L+2)] + [[2] + list(map(int, sys.stdin.readline().split())) + [2] for _ in range(L)] + [[2] * (L+2)]

knights = {}
init_k = [0] * (N+1)  # 초기 체력 저장
for index in range(1, N+1):
    r, c, h, w, k = list(map(int, sys.stdin.readline().split()))
    knights[index] = [r, c, h, w, k]
    init_k[index] += k
orders = {}
for index in range(1, Q+1):
    i, d = list(map(int, sys.stdin.readline().split()))
    orders[index] = [i, d]

# 방향 (위, 오른, 아래, 왼)
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]


def move(index, direction):
    q = deque()
    q.append(index)
    damage = [0] * (N+1)
    push_set = set() # 움직여야하는 기사들 저장
    push_set.add(index)
    # 기사 연쇄적으로 이동
    while q:
        cur = q.popleft()
        ci, cj, ch, cw, ck = knights[cur]
        ni, nj = ci + di[direction], cj + dj[direction]
        # 벽 존재할시 이동 불가 (아무 일도 x)
        for i in range(ni, ni + ch):
            for j in range(nj, nj + cw):
                if arr[i][j] == 2:
                    return
                elif arr[i][j] == 1:
                    damage[cur] += 1
        for knight in knights:
            if knight in push_set:
                continue   # 이미 포함된경우
            # if ni <= ti + th - 1 and ti <= ni + h - 1 and nj <= tj + tw - 1 and tj <= nj + w - 1:
            ki, kj, kh, kw, kk = knights[knight]
            # 현재 기사 시작점이 타켓 기사의 밑변보다 높음  # 타겟 기사의 시작점이 현재 기사의 밑변 보다 높음  # 현재 기사의 시작점이 타겟 기사의 오른쪽 변보다 왼쪽, 타겟 기사의 시작점이 현재 기사의 오른쪽 변보다 왼쪽
            # --> 서로 겹친다
            if ni <= ki + kh - 1 and ki <= ni + ch - 1 and nj <= kj + kw - 1 and kj <= nj + cw - 1:
                push_set.add(knight)
                q.append(knight)
    damage[index] = 0  # 처음 명령받은 기사에 대한 데미지는 0으로 초기화

    # 데미지 처리 및 이동
    for push in push_set:
        si, sj, sh, sw, sk = knights[push]
        if sk <= damage[push]:
            knights.pop(push)  # 제거
        else:
            knights[push] = [si + di[direction], sj + dj[direction], sh, sw, sk - damage[push]]

for o in orders:
    index, direction = orders[o]  # 현재 왕의 지시 (움직일 기사, 방향)
    if index in knights:
        move(index, direction)

answer = 0
for key, value in knights.items():
    answer += init_k[key] - value[-1]
print(answer)