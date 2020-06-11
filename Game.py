import pygame
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit
import sys
import time
import sqlite3


class RegWindow(QWidget):
    def __init__(self):
        super(RegWindow, self).__init__()
        self.title = "Space rush"
        self.top = 250
        self.left = 105
        self.width = 360
        self.height = 600
        self.MyUI()
    def MyUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        global input_nick
        input_nick = QLineEdit(self)
        input_nick.setPlaceholderText("Enter your nickname")
        input_nick.setGeometry(self.left, self.top, 150, 20)

        btn = QPushButton("Choose nickname", self)
        btn.setStyleSheet("Background-color:white")
        btn.setGeometry(128, 280, 100, 30)

        btn.clicked.connect(self.on_Click)
        self.setStyleSheet("background-color:lightyellow")
        self.show()

    @pyqtSlot()
    def on_Click(self):
        global playing_times_text
        user_nick = input_nick.text()
        regs = True
        i = 0
        pygame.font.init()
        user_font = pygame.font.SysFont('SHOWG.TTF', 25)
        user_text = user_font.render(user_nick, True, (255, 255, 255))


        # Registration window
        while regs:
            def register():
                cursor.execute("INSERT INTO users (nick, playing_times) VALUES (?, ?)", (user_nick, 0))
                conn.commit()
                print("You have registered successfully")

            conn = sqlite3.connect("Players.db")
            cursor = conn.cursor()

            cursor.execute("CREATE TABLE IF NOT EXISTS users (nick TEXT, playing_times INTEGER)")
            cursor.execute("SELECT * FROM users")
            user = cursor.fetchall()

            if user is not None:
                while i < len(user):
                    if user[i][0] == user_nick:
                        print("Welcome inside")
                        cursor.execute("UPDATE users SET playing_times = playing_times + 1 WHERE nick = :nick", {'nick': user_nick})
                        regs = False
                        playing_times = user[i][1]
                        break
                    else:
                        i += 1
                else:
                    print("If you have no account, it will be registered now")
                    register()
                    playing_times = user[i-1][1]
            print(user)
            playing_times_text = user_font.render("Times played: "+str(playing_times), True, (255, 255, 255))
            conn.commit()
            conn.close()
        self.hide()

        # Initializing
        pygame.init()
        screen_size = [360, 600]

        screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption('Space Rush')
        icon = pygame.image.load('spaceship_icon.png')
        pygame.display.set_icon(icon)

        background = pygame.image.load('Background.png')
        spaceship = pygame.image.load('spaceship.png')
        rocket = pygame.image.load('bullet.png')
        rocket_horizontal = pygame.image.load('bullet_horizontal.png')
        win = pygame.image.load('win.png')
        lose = pygame.image.load('lose.png')
        lose = pygame.transform.scale(lose, (334, 183))
        planet_one = pygame.image.load('one.png')
        planet_two = pygame.image.load('two.png')
        planet_three = pygame.image.load('three.png')
        planets = [planet_one, planet_two, planet_three]
        # Adding rockets amount to the list with changes of they coordinates
        x = 305
        y = 530
        rocket_horizontal_place = [[x, y]]
        for i in rocket_horizontal_place:
            y += 4
            rocket_horizontal_place.append([x, y])
            if y == 566:
                break

        rocket_place = [175, 500]
        text_rocket_place = [275, 552]
        planet_place = [145, 40]
        spaceship_place = [153, 500]
        move_direction = 'right'
        fired = False
        p = 0
        i = 0

        rockets = ['10']
        for r in rockets:
            if len(rockets) == 10:
                break
            r = int(r) - 1
            rockets.append(str(r))

        fps = pygame.time.Clock()
        font = pygame.font.Font('SHOWG.ttf', 30)
        lifes = True
        # Game window
        while lifes:
            pygame.event.get()
            screen.blit(background, [0, 0])
            # Rendering rocket amount
            text = font.render(rockets[0], True, (255, 255, 255))
            screen.blit(text, text_rocket_place)
            # Rendering top-left counter
            screen.blit(user_text, [5, 5])
            screen.blit(playing_times_text, [5, 22])

            screen.blit(planets[p], planet_place)
            # Rendering 10 rockets
            while i <= len(rocket_horizontal_place) - 1:
                screen.blit(rocket_horizontal, rocket_horizontal_place[i])
                i += 1
            else:
                i = 0
            # Moving planets
            if move_direction == 'right':
                planet_place[0] += 1
                if planet_place[0] == 293:
                    move_direction = 'left'
            else:
                planet_place[0] -= 1
                if planet_place[0] == 0:
                    move_direction = 'right'

            screen.blit(rocket, rocket_place)
            screen.blit(spaceship, spaceship_place)
            # Declare events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    fired = True
                if event.type == pygame.QUIT:
                    exit()
            # Firing the rockets
            if fired:
                if p == 1:
                    rocket_place[1] -= 1
                if p == 2:
                    rocket_place[1] -= 0.5
                else:
                    rocket_place[1] -= 2
                if 100 > rocket_place[1] > 30 and 170 > planet_place[0] > 120:
                    p += 1
                    rocket_horizontal_place.pop(0)
                    rockets.pop(0)
                    rocket_place[1] = 500
                    if p == 3:
                        screen.blit(win, [0, 0])
                        screen.blit(spaceship, spaceship_place)
                        pygame.display.update()
                        time.sleep(10)
                        lifes = False
                    fired = False
                elif rocket_place[1] < -30:
                    rocket_horizontal_place.pop(0)
                    rockets.pop(0)
                    rocket_place[1] = 500
                    fired = False
            # Changing place of the rocket counter
            if len(rockets) < 10:
                text_rocket_place = [285, 552]
            # Changing rocket counters
            if len(rocket_horizontal_place) == 0:
                time.sleep(0.5)
                screen.blit(lose, [15, 220])
                screen.blit(spaceship, spaceship_place)
                pygame.display.update()
                time.sleep(5)
                lifes = False

            pygame.display.update()
            fps.tick(144)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = RegWindow()
    app.exec_()
