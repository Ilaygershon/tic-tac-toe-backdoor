import random
import flask_server
import pygame
import threading

class GameDraw:
    def __init__(self, screen):
        self.screen = screen

    def line(self, start, end, color=(0, 0, 0), width=5):
        pygame.draw.line(self.screen, color, start, end, width)

    def x(self, center):
        x, y = center
        self.line((x-103, y-103), (x+103, y+103), color=(255, 0, 0), width=10)
        self.line((x-103, y+103), (x+103, y-103), color=(255, 0, 0), width=10)


    def circle(self, center):
        pygame.draw.circle(self.screen, (0, 0, 255), center, 103, 10)

    def text(self,text, size=200, color=(0,0,0), place=(200, 400)):
        font = pygame.font.Font(None, size)
        text = font.render(text, True, color)
        self.screen.blit(text, place)
        pygame.display.update()

class GameSim:
    def __init__(self, screen):
        self.screen = screen
        self.draw = GameDraw(self.screen)

    def start_screen(self):
        self.draw.line((100, 366), (900, 366))
        self.draw.line((100, 632), (900, 632))
        self.draw.line((366, 100), (366, 900))
        self.draw.line((632, 100), (632, 900))


    def check_press(self, coordinates, positions):
        width, height = 266, 266
        mouse_x, mouse_y = coordinates
        count = 2
        for y in range(100, 900, 266):
            count -= 1
            for x in range(100, 900, 266):
                if (x <= mouse_x <= x + width) and (y <= mouse_y <= y + height):
                    self.index = count
                count += 1
        try:
            if self.index not in positions:
                self.place_x(self.index)
                return self.index
            else:
                self.place_x(None)
                return None
        except:
            self.place_x(None)
            return None

    def place_x(self, index):
        count = 1
        for y in range(233, 900, 266):
            for x in range(233, 900, 266):
                if count == index:
                    self.draw.x((x, y))
                    return
                count += 1

class Opponent:
    def __init__(self, screen, positions, win_slot, x_position, circle_position):
        self.screen = screen
        self.draw = GameDraw(self.screen)
        self.x_position = x_position
        self.positions = positions
        self.win_slot = win_slot
        self.circle_position = circle_position

    def find(self):
        for line in self.win_slot:
            count = 0
            for position in self.x_position:
                if position in line:
                    count += 1
            if count >= 2:
                for position in line:
                    if position not in self.positions:
                        self.place_circle(position)
                        self.win_slot.remove(line)
                        return self.win_slot, True, position
                break
        return self.win_slot, False, 0

    def one_circle(self, line):
        for position in line:
            if position not in self.positions:
                self.place_circle(position)
                position = position
                return position
        return 10

    def two_circle(self, line):
        for position in line:
            if position not in self.positions:
                self.place_circle(position)
                position = position
                return position, True
        return 10, False

    def other(self):
        position = random.choice(self.positions)
        while position in self.positions:
            position = random.randint(1, 9)
        self.place_circle(position)

        for win in self.win_slot:
            if self.x_position[0] in win and position in win:
                self.win_slot.remove(win)
        return position


    def sim(self):
        counts = {}
        if self.circle_position:
            for line in self.win_slot:
                count = 0
                for position in self.circle_position:
                    if position in line:
                        count += 1
                counts[count] = line

            sorted_dict = dict(sorted(counts.items(), reverse=True))
            biggest_count = next(iter(sorted_dict))
            line = sorted_dict[biggest_count]
            return biggest_count, line

        else:
            return 0, 0

    def place_circle(self, index):
        count = 1
        for y in range(233, 900, 266):
            for x in range(233, 900, 266):
                if count == index:
                    self.draw.circle((x, y))
                    return
                count += 1

class Winner:
    def __init__(self, screen, positions, win_slot):
        self.screen = screen
        self.draw = GameDraw(self.screen)
        self.win_slot = win_slot

    def x_winner(self, x_position):
        for line in self.win_slot:
            count = 0
            for placement in x_position:
                if placement in line:
                    count += 1
            if count >= 3:
                return True
        return False

    def circle_winner(self, circle_position):
        for line in self.win_slot:
            count = 0
            for placement in circle_position:
                if placement in line:
                    count += 1
            if count >= 3:
                return True
        return False

    def check_winner(self, x_position, circle_position):
        x = self.x_winner(x_position)
        circle = self.circle_winner(circle_position)
        if x:
            pygame.display.update()
            pygame.time.delay(1000)

            self.screen.fill((255, 255, 255))
            self.draw.text(f"You Won!")
            return True
        if circle:
            pygame.display.update()
            pygame.time.delay(1000)

            self.screen.fill((255, 255, 255))
            self.draw.text(f"You lost")
            return True
        return False

def opponent_handler(screen, positions, win_slot, x_positon, circle_position):
    opponent = Opponent(screen, sorted(positions), win_slot, x_positon, circle_position)
    count, line = opponent.sim()
    pygame.display.update()
    pygame.time.delay(500)
    check = False
    if count == 2:
        position, check = opponent.two_circle(line)
    if not check:
        if count == 0:
            position = opponent.other()
        else:
            win_slot, check, position = opponent.find()
            if not check:
                position = opponent.one_circle(line)
                if position == 10:
                    position = opponent.other()

    circle_position.append(position)
    positions.append(position)
    return win_slot, position, circle_position

def main():
    threading.Thread(target=flask_server.main).start()
    pygame.init()
    white = (255, 255, 255)

    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Hello Pygame")
    draw = GameDraw(screen)

    screen.fill(white)
    game_sim = GameSim(screen)
    game_sim.start_screen()
    circle_position = []
    win_slot = [[1, 5, 9], [3, 5, 7], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 2, 3], [4, 5, 6], [7, 8, 9]]

    positions = []
    x_position = []
    running = True
    while running:
        try:
            game_sim = GameSim(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    index = game_sim.check_press(mouse_pos, positions)
                    if not index:
                        continue
                    x_position.append(index)
                    x_position = list(set(x_position))
                    positions += x_position
                    positions = list(set(positions))
                    winner = Winner(screen, positions, win_slot)
                    check = winner.check_winner(x_position, circle_position)
                    if check:
                        pygame.time.delay(2000)
                        main()
                    if len(positions) < 9:
                        win_slot, new_position, circle_position = opponent_handler(screen, positions, win_slot, x_position, circle_position)
                        positions.append(new_position)
                        check = winner.check_winner(x_position, circle_position)
                        if check:
                            pygame.time.delay(2000)
                            main()
                    else:
                        pygame.display.update()
                        pygame.time.delay(1000)
                        screen.fill(white)
                        draw.text(f"tee", place=(400, 400))
                        pygame.time.delay(2000)
                        main()



            pygame.display.update()
        except:
            pass
    pygame.quit()

if __name__ == '__main__':
    main()