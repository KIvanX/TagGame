
import pygame
from TagGame import TagGame


N = 8
A = 80
pygame.init()
screen = pygame.display.set_mode((N * A, N * A))
pygame.display.set_caption(f"Пятнашки {N}X{N}")

tagGame = TagGame(N, A, screen, 0.01)

game = True
while game:
    tagGame.show()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                tagGame.step('RIGHT')

            if event.key == pygame.K_LEFT:
                tagGame.step('LEFT')

            if event.key == pygame.K_UP:
                tagGame.step('UP')

            if event.key == pygame.K_DOWN:
                tagGame.step('DOWN')

            if event.key == pygame.K_DELETE:
                tagGame.shuffle()

            if event.key == pygame.K_RETURN:
                tagGame.solution()

            if pygame.K_1 < event.key <= pygame.K_9:
                N = event.key - 48
                screen = pygame.display.set_mode((N * A, N * A))
                pygame.display.set_caption(f"Пятнашки {N}X{N}")
                tagGame = TagGame(N, A, screen, 0.01)

        if event.type == pygame.MOUSEBUTTONDOWN:
            y, x = pygame.mouse.get_pos()
            if tagGame.void[0] == x // A and y // A in [i for i in range(tagGame.void[1] + 1, N)]:
                for i in range(y // A - tagGame.void[1]):
                    tagGame.step('RIGHT')

            if tagGame.void[0] == x // A and y // A in [i for i in range(tagGame.void[1])]:
                for i in range(tagGame.void[1] - y // A):
                    tagGame.step('LEFT')

            if x // A in [i for i in range(tagGame.void[0] + 1, N)] and tagGame.void[1] == y // A:
                for i in range(x // A - tagGame.void[0]):
                    tagGame.step('DOWN')

            if x // A in [i for i in range(tagGame.void[0])] and tagGame.void[1] == y // A:
                for i in range(tagGame.void[0] - x // A):
                    tagGame.step('UP')
