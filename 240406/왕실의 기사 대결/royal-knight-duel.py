import sys

L, N, Q = map(int, sys.stdin.readline().split())
arr = [[2] + list(map(int, sys.stdin.readline().split())) + [2] for _ in range(L)]  # 둘레 벽처리
arr = [[2] * (L+2)] + arr + [[2] * (L+2)]
arr_knight = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]
arr_order = [list(map(int, sys.stdin.readline().split())) for _ in range(Q)]
init_k = [0] * (N+1)
knights = {}

for i, knight in enumerate(arr_knight):
    knights[i+1] = knight
    init_k[i+1] = knight[-1]

di = [-1, 0, 1, 0]
dj = [0, 1, 0,-1]


def push_knights(start, direction):
    q = []
    push_set = set()
    damage = [0] * (N+1)
    q.append(start)
    push_set.add(start)

    while q:
        cur = q.pop(0)
        ci, cj, h, w, k = knights[cur]
        ni, nj = ci + di[direction], cj + dj[direction]
        for i in range(ni, ni+h):
            for j in range(nj, nj+w):
                if arr[i][j] == 2:
                    return
                if arr[i][j] == 1:
                    damage[cur] += 1
        for index in knights:
            if index in push_set:
                continue
            ti, tj, th, tw, tk = knights[index]
            if ni <= ti + th - 1 and ti <= ni + h - 1 and nj <= tj + w - 1 and tj <= nj + w - 1:
                q.append(index)
                push_set.add(index)
    damage[start] = 0

    # 데미지 및 이동 처리
    for index in push_set:
        si, sj, h, w, k = knights[index]

        if k <= damage[index]:
            knights.pop(index)
        else:
            ni, nj = si + di[direction], sj + dj[direction]
            knights[index] = [ni, nj, h, w, k - damage[index]]

for order in arr_order:
    index, direction = order
    if index in knights:
        push_knights(index, direction)

# 정답 처리
answer = 0
for i in knights:
    answer += init_k[i] - knights[i][-1]
print(answer)