import sys

sys.stdin = open("input.txt")

N, M, K = list(map(int, sys.stdin.readline().split()))
arr = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]
gun = [[[] * N for _ in range(N)] for _ in range(N)]

# 그리드별로 gun 정보 저장
for i in range(N):
    for j in range(N):
        if arr[i][j] > 0:
            gun[i][j].append(arr[i][j])

# 상 우 하 좌
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

opp = {0:2, 2:0, 1:3, 3:1}
arr = [[0] * N for _ in range(N)]  # 플레이어 위치 저장을 위해
players = {}
for m in range(1, M+1):
    i, j, d, p = list(map(int, sys.stdin.readline().split()))
    players[m] = [i-1, j-1, d, p, 0, 0]  # i, j, 방향, 파워, gun, score
    arr[i-1][j-1] = m

def leave(index):
    ci, cj, cd, cp, cg, cs = players[index]
    for turn in range(4):
        ni, nj = ci + di[(cd+k) % 4], cj + dj[(cd+k) % 4]
        if 0 <= ni < N and 0 <= nj < N and arr[ni][nj] == 0:
            if len(gun[ni][nj]) != 0:
                cg = max(gun[ni][nj])
                gun[ni][nj].remove(cg)
            arr[ni][nj] = index
            players[index] = [ni, nj, (cd+k) % 4, cp, cg, cs]

            return



for k in range(K):    # K turn 진행
    for index in players:   # 각 player 마다 순차적으로 진행
        # 현재 플레이어 추출 및 진행방향으로 한칸 이동
        ci, cj, cd, cp, cg, cs = players[index]
        ni, nj = ci + di[cd], cj + dj[cd]
        if ni < 0 or ni >= N or nj < 0 or nj >= N:  # 범위 밖 -> 반대방향
            cd = opp[cd]
            ni, nj = ci + di[cd], cj + dj[cd]
        arr[ci][cj] = 0   # 이동한 자리 비우기

        # 상대방이 없는 경우 (총 줍기)
        if arr[ni][nj] == 0:
            if len(gun[ni][nj]) != 0:
                gun_mx = max(gun[ni][nj])
                if cg < gun_mx:
                    if cg > 0:
                        gun[ni][nj].append(cg)
                    cg = gun_mx
                    gun[ni][nj].append(gun_mx)
            arr[ni][nj] = index
            players[index] = [ni, nj, cd, cp, cg, cs]

        # 상대방이 있는 경우 (대결)
        else:
            enemy = arr[ni][nj]
            ei, ej, ed, ep, eg, es = players[enemy]
            # 내가 이긴 경우
            if (cp + cg) > (ep + eg) or ((cp + cg) == (ep + eg) and cp > ep):
                cs += ((cp + cg) - (ep + eg))
                leave(enemy)

                if cg < eg:
                    if cg > 0:
                        gun[ni][nj].append(cg)
                    cg = eg
                else:
                    if eg > 0:
                        gun[ni][nj].append(eg)
                arr[ni][nj] = index
                players[index] = [ni, nj, cd, cp, cg, cs]
            # 상대방이 이긴 경우
            else:
                es += ((ep + eg) - (cp + cg))
                leave(index)
                if eg < cg:
                    if eg > 0:
                        gun[ni][nj].append(eg)
                    eg = cg
                else:
                    if cg > 0:
                        gun[ni][nj].append(cg)
                arr[ni][nj] = enemy
                players[enemy] = [ni, nj, ed, ep, eg, es]
# 각 플레이어 점수 출력
for _, value in players.items():
    print(value[5], end=" ")