# Header Files
import cv2
import numpy as np

# -----------------------------------------------------------------------------------

# Classes
class Block():
    def __init__(self, i, j):
        self.value = None
        self.pos = (i, j)

    def setValue(self, value):
        self.value = value


# -----------------------------------------------------------------------------------

class GUI():
    def __init__(self, windowName):
        self.windowName = windowName
        self.width, self.height = 600, 600
        self.menuHeight = 100
        self.image = np.zeros((self.height + self.menuHeight, self.width, 3), np.uint8)
        self.turn = 1
        self.reset()

    # -----------------------------------------------------------------------------------
    # Reset Game
    def reset(self):
        self.blocks = []
        self.win = False
        self.change = True
        self.selected = False
        for i in range(10):
            row = []
            for j in range(10):
                row.append([Block(i, j), (j * (self.width // 10) + 3, i * (self.height // 10) + 3),
                            ((j + 1) * (self.width // 10) - 3, (i + 1) * (self.height // 10) - 3)])
            self.blocks.append(row)

    # -----------------------------------------------------------------------------------
    # Drawing GUI and Game Screen
    def draw(self):
        self.image = np.zeros((self.height + self.menuHeight, self.width, 3), np.uint8)
        for i in range(10):
            for j in range(10):
                start_point = self.blocks[i][j][1]
                end_point = self.blocks[i][j][2]
                cv2.rectangle(self.image, start_point, end_point, (255, 255, 255), -1)
                value = " " if self.blocks[i][j][0].value is None else self.blocks[i][j][0].value
                cv2.putText(self.image, value, (j * (self.width // 10) + 15, (i * self.height // 10) + 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        if self.checkWin():
            string = "Player {} Wins".format(self.turn)
        else:
            if self.checkDraw():
                string = "Match Draw!!"
            else:
                string = "Player {}'s Turn".format(self.turn)
        cv2.putText(self.image, string, (self.width // 2 - 70, self.height + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 255, 255), 1)
        cv2.putText(self.image, "R - Reset", (10, self.height + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
                    1)
        cv2.putText(self.image, "Esc - Exit", (10, self.height + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
                    1)

    # -----------------------------------------------------------------------------------
    # Game Play Functions
    def mainLoop(self):  # Game Loop till Esc (Close) button is pressed
        cv2.namedWindow(self.windowName)
        cv2.setMouseCallback(self.windowName, self.mouseCall)
        try:
            while True and cv2.getWindowProperty(self.windowName, 1) != -1:
                if self.change:
                    self.change = False
                    self.draw()
                    cv2.imshow(self.windowName, self.image)
                # Keyboard Hits
                key = cv2.waitKey(1)
                if key == 27:
                    break
                elif key == ord("r") or key == ord("R"):
                    self.reset()
            cv2.destroyAllWindows()
        except:
            print("Window is successfully closed")

    def checkWin(self):
        self.win = False
        # Check rows
        for i in range(10):
            for j in range(6):
                if (self.blocks[i][j][0].value is not None and
                        self.blocks[i][j][0].value == self.blocks[i][j + 1][0].value ==
                        self.blocks[i][j + 2][0].value == self.blocks[i][j + 3][0].value ==
                        self.blocks[i][j + 4][0].value):
                    self.win = True
                    return self.win
        # Check columns
        for i in range(6):
            for j in range(10):
                if (self.blocks[i][j][0].value is not None and
                        self.blocks[i][j][0].value == self.blocks[i + 1][j][0].value ==
                        self.blocks[i + 2][j][0].value == self.blocks[i + 3][j][0].value ==
                        self.blocks[i + 4][j][0].value):
                    self.win = True
                    return self.win
        # Check diagonals (top-left to bottom-right)
        for i in range(6):
            for j in range(6):
                if (self.blocks[i][j][0].value is not None and
                        self.blocks[i][j][0].value == self.blocks[i + 1][j + 1][0].value ==
                        self.blocks[i + 2][j + 2][0].value == self.blocks[i + 3][j + 3][0].value ==
                        self.blocks[i + 4][j + 4][0].value):
                    self.win = True
                    return self.win
        # Check diagonals (top-right to bottom-left)
        for i in range(6):
            for j in range(4, 10):
                if (self.blocks[i][j][0].value is not None and
                        self.blocks[i][j][0].value == self.blocks[i + 1][j - 1][0].value ==
                        self.blocks[i + 2][j - 2][0].value == self.blocks[i + 3][j - 3][0].value ==
                        self.blocks[i + 4][j - 4][0].value):
                    self.win = True
                    return self.win
        return self.win

    def checkDraw(self):
        for i in range(10):
            for j in range(10):
                if self.blocks[i][j][0].value is None:
                    return False
        return True

    # -----------------------------------------------------------------------------------
    # Mouse Click Functions - (For User Players)
    def mouseCall(self, event, posx, posy, flag, param):
        if event == cv2.EVENT_LBUTTONDOWN and not self.win:
            self.setBlockInPos(posx, posy)

    def setBlockInPos(self, x, y):
        for i in range(10):
            for j in range(10):
                if (self.blocks[i][j][0].value is None and
                        self.blocks[i][j][1][0] <= x <= self.blocks[i][j][2][0] and
                        self.blocks[i][j][1][1] <= y <= self.blocks[i][j][2][1]):
                    self.blocks[i][j][0].setValue("X" if self.turn == 1 else "O")
                    self.change = True
                    if self.checkWin() or self.checkDraw():
                        self.win = True
                    else:
                        self.turn = 2 if self.turn == 1 else 1


# -----------------------------------------------------------------------------------
# Main Function
def main():
    gui = GUI("Tic Tac Toe")
    gui.mainLoop()


if __name__ == "__main__":
    main()
