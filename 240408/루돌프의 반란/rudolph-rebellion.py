import sys

N, M, P, C, D = map(int, sys.stdin.readline().split())
ri, rj = map(int, sys.stdin.readline().split())  # 루돌프 위치
ri, rj = ri - 1, rj - 1
santa_list = [list(map(int, sys.stdin.readline().split())) for _ in range(P)]

game_map = [[0] * N for _ in range(N)]
game_map[ri][rj] = -1  # 루돌프 위치 map 에 저장 -1

santa = [[0] * 2 for _ in range(P + 1)]
for s in santa_list:
    n, i, j = s
    game_map[i - 1][j - 1] = n  # map 에 산타 저장 (위치, index)
    santa[n] = [i - 1, j - 1]

score = [0] * (P + 1)
wakeup = [1] * (P + 1)
alive = [1] * (P + 1)
alive[0] = 0


def get_distance(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2

def move_santa(index, si, sj, di, dj, move):
    q = [(index, si, sj, move)]

    while q:
        cur_index, ci, cj, move = q.pop(0)
        ni, nj = ci + di * move, cj + dj * move
        if 0 <= ni < N and 0 <= nj < N:
            if game_map[ni][nj] == 0:
                game_map[ni][nj] = cur_index
                santa[cur_index] = [ni, nj]
                return
            else:
                q.append((game_map[ni][nj], ni, nj, 1))
                game_map[ni][nj] = cur_index
                santa[cur_index] = [ni, nj]
        else:
            alive[cur_index] = 0
            return


for turn in range(1, M + 1):  # M 번의 turn
    if sum(alive) == 0:
        break

    # 거리를 기준으로 산타 선정 후보 찾기
    min_value = 2 * N ** 2
    for index in range(1, P + 1):
        if alive[index] == 0:  # 탈락 산타
            continue
        si, sj = santa[index]
        distance = get_distance(si, sj, ri, rj)
        if min_value > distance:
            min_value = distance
            min_list = [(si, sj, index)]
        elif min_value == distance:
            min_list.append((si, sj, index))
    min_list.sort(reverse=True)

    # 돌진 산타 선정
    si, sj, min_index = min_list[0]

    # 루돌프 움직이기
    rdi, rdj = 0, 0
    if ri < si:
        rdi = 1
    elif ri > si:
        rdi = -1
    if rj < sj:
        rdj = 1
    elif rj > sj:
        rdj = -1

    game_map[ri][rj] = 0
    ri, rj = ri + rdi, rj + rdj
    game_map[ri][rj] = -1

    # 움직인 루돌프가 산타와 충돌했을떄
    if (ri, rj) == (si, sj):
        score[min_index] += C
        wakeup[min_index] = turn + 2
        move_santa(min_index, si, sj, rdi, rdj, C)

    # 산타 움직임
    for index in range(1, P + 1):
        if alive[index] == 0:
            continue
        if wakeup[index] > turn:
            continue

        si, sj = santa[index]
        min_distance = get_distance(ri, rj, si, sj)
        temp = []
        for di, dj in ((-1, 0), (0, 1), (1, 0), (0, -1)):  # 상우하좌
            ni, nj = si + di, sj + dj
            distance = get_distance(ri, rj, ni, nj)
            if 0 <= ni < N and 0 <= nj < N and game_map[ni][nj] <= 0 and min_distance > distance:
                min_distance = distance
                temp.append((ni, nj, di, dj))
        if len(temp) == 0:
            continue  # 해당 산타는 움직일 필요 없음
        ni, nj, di, dj = temp[-1]  # 가장 짧은 친구
        game_map[si][sj] = 0
        # 이동했는데 충돌한다면
        if (ri, rj) == (ni, nj):
            score[index] += D
            wakeup[index] = turn + 2
            move_santa(index, ni, nj, -di, -dj, D)
        else:
            game_map[ni][nj] = index
            santa[index] = [ni, nj]

    for index in range(1, P + 1):  # 살아있는 산타 보너스 점스
        if alive[index] == 1:
            score[index] += 1
print(*score[1:])