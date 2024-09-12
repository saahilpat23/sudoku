import pygame
pygame.font.init()

# Initialize the window and font
Window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("SUDOKU GAME by Saahil Patel")

# Grid size and default grid
diff = 500 / 9
value = 0
defaultgrid = [
    [0, 0, 4, 0, 6, 0, 0, 0, 5],
    [7, 8, 0, 4, 0, 0, 0, 2, 0],
    [0, 0, 2, 6, 0, 1, 0, 7, 8],
    [6, 1, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 7, 5, 4, 0, 0, 6, 1],
    [0, 0, 1, 7, 5, 0, 9, 3, 0],
    [0, 7, 0, 3, 0, 0, 0, 1, 0],
    [0, 4, 0, 2, 0, 6, 0, 0, 7],
    [0, 2, 0, 0, 0, 7, 4, 0, 0],
]

font = pygame.font.SysFont("comicsans", 40)
font1 = pygame.font.SysFont("comicsans", 20)

##Convert pixel coordinates to grid coordinates.
def cord(pos):
    global x, z
    x = pos[0] // diff
    z = pos[1] // diff

##Highlight the currently selected cell in the Sudoku grid.
def highlightbox():
    pygame.draw.line(Window, (0, 0, 0), (x * diff - 3, z * diff), (x * diff + diff + 3, z * diff), 7)
    pygame.draw.line(Window, (0, 0, 0), (x * diff - 3, (z + 1) * diff), (x * diff + diff + 3, (z + 1) * diff), 7)
    pygame.draw.line(Window, (0, 0, 0), (x * diff, z * diff - 3), (x * diff, z * diff + diff + 3), 7)
    pygame.draw.line(Window, (0, 0, 0), ((x + 1) * diff, z * diff - 3), ((x + 1) * diff, z * diff + diff + 3), 7)

#Draw the grid lines on the window.
def drawlines():
    for i in range(10):
        thickness = 7 if i % 3 == 0 else 1
        pygame.draw.line(Window, (0, 0, 0), (0, i * diff), (500, i * diff), thickness)
        pygame.draw.line(Window, (0, 0, 0), (i * diff, 0), (i * diff, 500), thickness)

##Render and display the value in the selected cell.
def fillvalue(value):
    text1 = font.render(str(value), 1, (0, 0, 0))
    Window.blit(text1, (x * diff + 15, z * diff + 15))

##Display an error message at the bottom of the window.
def raiseerror(message):
    text1 = font1.render(message, 1, (255, 0, 0))
    Window.blit(text1, (20, 570))

##Check if placing a value in the specified cell is valid according to Sudoku rules.
def validvalue(m, k, l, value):
    # Check row and column
    for it in range(9):
        if m[k][it] == value or m[it][l] == value:
            return False
    # Check 3x3 grid
    it, jt = k // 3, l // 3
    for i in range(it * 3, it * 3 + 3):
        for j in range(jt * 3, jt * 3 + 3):
            if m[i][j] == value:
                return False
    return True

  
##Solve the Sudoku grid using a backtracking algorithm.

def solvegame(grid, i, j):
    while grid[i][j] != 0:
        if i < 8:
            i += 1
        elif i == 8 and j < 8:
            i = 0
            j += 1
        elif i == 8 and j == 8:
            return True
    pygame.event.pump()
    for it in range(1, 10):
        if validvalue(grid, i, j, it):
            grid[i][j] = it
            global x, z
            x = i
            z = j
            Window.fill((255, 255, 255))
            drawlines()
            highlightbox()
            pygame.display.update()
            pygame.time.delay(20)
            if solvegame(grid, i, j):
                return True
            else:
                grid[i][j] = 0
            Window.fill((255, 255, 255))
            drawlines()
            highlightbox()
            pygame.display.update()
            pygame.time.delay(50)
    return False

def gameresult():
    text1 = font1.render("Game is done!", 1, (0, 255, 0))
    Window.blit(text1, (20, 570))

# Initialize game state
x, z = 0, 0
flag, flag1, flag2 = True, False, False
rs, error = 0, 0

while flag:
    Window.fill((255, 182, 193))  # Clear the window with background color
    drawlines()  # Draw the grid lines

    # Draw the current state of the Sudoku grid
    for i in range(9):
        for j in range(9):
            if defaultgrid[i][j] != 0:
                fillvalue(defaultgrid[i][j])

    highlightbox()  # Highlight the selected box

    if rs == 1:
        gameresult()  # Display the result if solved
    elif error == 1:
        raiseerror("No solution exists!")  # Display error message if unsolvable

    pygame.display.update()  # Update the display

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = True
            pos = pygame.mouse.get_pos()
            cord(pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x = max(x - 1, 0)
                flag1 = True
            if event.key == pygame.K_RIGHT:
                x = min(x + 1, 8)
                flag1 = True
            if event.key == pygame.K_UP:
                z = max(z - 1, 0)
                flag1 = True
            if event.key == pygame.K_DOWN:
                z = min(z + 1, 8)
                flag1 = True
            if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                value = event.key - pygame.K_0
            if event.key == pygame.K_RETURN:
                flag2 = True
            if event.key == pygame.K_r:
                rs = 0
                error = 0
                flag2 = False
                defaultgrid = [[0] * 9 for _ in range(9)]
            if event.key == pygame.K_d:
                rs = 0
                error = 0
                flag2 = False
                defaultgrid = [
                    [0, 0, 4, 0, 6, 0, 0, 0, 5],
                    [7, 8, 0, 4, 0, 0, 0, 2, 0],
                    [0, 0, 2, 6, 0, 1, 0, 7, 8],
                    [6, 1, 0, 0, 7, 5, 0, 0, 9],
                    [0, 0, 7, 5, 4, 0, 0, 6, 1],
                    [0, 0, 1, 7, 5, 0, 9, 3, 0],
                    [0, 7, 0, 3, 0, 0, 0, 1, 0],
                    [0, 4, 0, 2, 0, 6, 0, 0, 7],
                    [0, 2, 0, 0, 0, 7, 4, 0, 0],
                ]

    if flag2:
        if solvegame(defaultgrid, 0, 0):
            rs = 1
        else:
            error = 1
        flag2 = False

    if value != 0:
        if validvalue(defaultgrid, x, z, value):
            defaultgrid[x][z] = value
            flag1 = False
        else:
            defaultgrid[x][z] = 0
            raiseerror("Invalid value! Try again.")  # Corrected string literal

pygame.quit()