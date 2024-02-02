import random
import time
import pygame


class TagGame:
    def __init__(self, n, cell, screen, delay):
        self.n = n
        self.sell = cell
        self.screen = screen
        self.a = [[(i * n + j + 1) % n**2 for j in range(n)] for i in range(n)]
        self.font = pygame.font.Font(pygame.font.match_font('texgyrebonum'), 40)
        self.void = [n - 1, n - 1]
        self.locker = [[0] * self.n for _ in range(self.n)]
        self.vec = {'left': (0, -1), 'right': (0, 1), 'down': (1, 0), 'up': (-1, 0)}
        self.side = {(0, -1): 'left', (0, 1): 'right', (1, 0): 'down', (-1, 0): 'up'}
        self.delay = delay

        self.shuffle()

    def show(self):
        self.screen.fill((200, 180, 160))

        for i in range(self.n):
            for j in range(self.n):
                if not self.a[i][j]:
                    continue

                A = self.sell
                pygame.draw.rect(self.screen, (0, 0, 0), (j * A + 1, i * A + 1, A - 2, A - 2), border_radius=10)
                pygame.draw.rect(self.screen, (180, 160, 140), (j * A + 2, i * A + 2, A - 4, A - 4), border_radius=10)
                text_surface = self.font.render(str(self.a[i][j]), True, (0, 0, 0))
                self.screen.blit(text_surface, (j * A + 13 * (3 - len(str(self.a[i][j]))), i * A + 10))

        pygame.display.flip()

    def step(self, to):
        v = self.vec[to.lower()]

        if 0 <= self.void[0] + v[0] < self.n and 0 <= self.void[1] + v[1] < self.n:
            vx, vy = self.void = [self.void[0] + v[0], self.void[1] + v[1]]
            self.a[vx][vy], self.a[vx - v[0]][vy - v[1]] = self.a[vx - v[0]][vy - v[1]], self.a[vx][vy]

    def shuffle(self):
        for i in range(self.n ** 5):
            self.step(random.choice(['left', 'right', 'down', 'up']))
        while self.void[0] != self.n - 1:
            self.step('down')
        while self.void[1] != self.n - 1:
            self.step('right')

    def solution(self):
        k = 1
        while k < self.n ** 2 - self.n * 2:
            to = [(k - 1) // self.n, (k - 1) % self.n]

            if k % self.n == self.n - 1:
                self.go_with_push(k, k+1, to, [to[0], to[1] + 1])
                k += 2
                continue

            self.go_to(k, to)
            self.locker[to[0]][to[1]] = 1
            k += 1

        k = self.n ** 2 - self.n * 2 + 1
        for i in range(self.n - 2):
            self.go_with_push(k + i, k + i + self.n, [self.n - 2, i], [self.n - 1, i])

        self.go_to(self.n ** 2 - 1, [self.n - 1, self.n - 2])
        self.go_to(self.n ** 2 - self.n, [self.n - 2, self.n - 1])

        self.locker = [[0] * self.n for _ in range(self.n)]

    def go_with_push(self, k1, k2, to1, to2):
        buf = [to2[0] + 1, to2[1]] if k1 + 1 == k2 else [to2[0], to2[1] + 1]

        self.go_to(k2, [to2[0] + 2, to2[1]] if k1 + 1 == k2 else [to2[0], to2[1] + 2])

        self.go_to(k1, to2)
        self.locker[to2[0]][to2[1]] = 1

        self.go_to(k2, buf)
        self.locker[buf[0]][buf[1]] = 1

        self.go_to(k1, to1)
        self.locker[to1[0]][to1[1]] = 1

        self.go_to(k2, to2)
        self.locker[to2[0]][to2[1]] = 1

        self.locker[buf[0]][buf[1]] = 0

    def go_to(self, k, to):
        xk, yk = [(i, self.a[i].index(k)) for i in range(self.n) if k in self.a[i]][0]

        while [xk, yk] != to:
            s0 = self.way([xk, yk], to)[0]
            self.locker[xk][yk] = 1
            for p in self.way([self.void[0], self.void[1]], [xk + s0[0], yk + s0[1]]):
                self.step(self.side[p])
                self.show()
                time.sleep(self.delay)

            self.locker[xk][yk] = 0
            self.step(self.side[(-s0[0], -s0[1])])
            self.show()
            time.sleep(self.delay)
            xk, yk = xk + s0[0], yk + s0[1]

    def way(self, p1, p2):
        m = [[self.n**2] * self.n for _ in range(self.n)]
        m[p2[0]][p2[1]] = 0

        for _ in range(self.n**2):
            if m[p1[0]][p1[1]] != self.n**2:
                break
            for i in range(self.n):
                for j in range(self.n):
                    if self.locker[i][j] and p1 != [i, j] and p2 != [i, j]:
                        continue
                    for v in self.vec.values():
                        if 0 <= i + v[0] < self.n and 0 <= j + v[1] < self.n:
                            m[i][j] = min(m[i][j], m[i + v[0]][j + v[1]] + 1)

        if m[p1[0]][p1[1]] == self.n ** 2:
            print('Way is not found')
            input()
            return []

        pos, w = p1, []
        while pos != p2:
            for v in self.side:
                if 0 <= pos[0] + v[0] < self.n and 0 <= pos[1] + v[1] < self.n:
                    if m[pos[0] + v[0]][pos[1] + v[1]] == m[pos[0]][pos[1]] - 1:
                        pos = [pos[0] + v[0], pos[1] + v[1]]
                        w.append(v)

        return w

