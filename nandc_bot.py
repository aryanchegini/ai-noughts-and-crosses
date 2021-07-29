# ARYAN CHEGINI 2021
# noughts and crosses game where you play against the computer
# the computer has logic to determine whether it can make a winning move or prevent one from the opponent and can
# also plan ahead and make smart moves in order to give itself a chance to win

import random
import os
import time


# the computer class used to initiate the computers name
class Computer:
    def __init__(self, bot_wp):
        self.bot_name = "b.o.b"
        self.wp = bot_wp

    def __repr__(self):
        return self.bot_name


# the player class used to initiate the player's name
class Player:
    def __init__(self, player_name, weapon):
        self.name = player_name
        self.wp = weapon

    def __repr__(self):
        return self.name


class NoughtsAndCrosses:
    # creating instance variables
    def __init__(self):
        self.grid = {
            "TL": " ", "TM": " ", "TR": " ",
            "ML": " ", "MM": " ", "MR": " ",
            "BL": " ", "BM": " ", "BR": " "
        }
        self.choices = ["x", "o"]
        self.playing = True
        self.player_choices = {"player1weapon": None, "bot_weapon": None}
        self.player1name = None
        self.bot_name = None
        # storing all the different possible ways there are to win
        self.ways_to_win = {
            "row1": ["TL", "TM", "TR"],
            "row2": ["ML", "MM", "MR"],
            "row3": ["BL", "BM", "BR"],
            "column1": ["TL", "ML", "BL"],
            "column2": ["TM", "MM", "BM"],
            "column3": ["TR", "MR", "BR"],
            "diagonal1": ["TL", "MM", "BR"],
            "diagonal2": ["TR", "MM", "BL"]
        }
        self.remaining_sections = ["TL", "TM", "TR", "ML", "MM", "MR", "BL", "BM", "BR"]
        self.mapping = {"x": None, "o": None}
        self.registered = False

    def print_grid(self):
        output = f"""
{self.grid["TL"]}|{self.grid["TM"]}|{self.grid["TR"]}
-+-+-
{self.grid["ML"]}|{self.grid["MM"]}|{self.grid["MR"]}
-+-+-
{self.grid["BL"]}|{self.grid["BM"]}|{self.grid["BR"]}
        """
        print(output)

    def intro(self):
        begin = False
        print("""
Welcome!
In this game, you play against the infamous b.o.b, the robot whos terrible at noughts and crosses!🥲

When asked to enter a section, please name and abbreviate the desired section correctly. For example, when naming your section
always refer to the row first (top (t), middle (m), bottom (b)), then the column (left (l), middle(m), right(r)).

When abbreviating, please use the letters provided next to the rows and columns above.

Have a great time thrashing our b.o.b at it's favourite game.
        

To get started, hit enter!
        """)
        while not begin:
            decision = str(input(">>>"))
            if decision == "":
                begin = True
            

            

    def computer(self):
        print("computing...")
        time.sleep(2)

        # lists all possible moves it can make to either win the game or prevent the opponent from winning
        win_moves = []
        defend_moves = []
        smart_move = []

        # mapping the values on the game grid to all the possible ways it can win 
        hashing = {
            "row1": {"TL": " ", "TM": " ", "TR": " "},
            "row2": {"ML": " ", "MM": " ", "MR": " "},
            "row3": {"BL": " ", "BM": " ", "BR": " "},
            "column1": {"TL": " ", "ML": " ", "BL": " "},
            "column2": {"TM": " ", "MM": " ", "BM": " "},
            "column3": {"TR": " ", "MR": " ", "BR": " "},
            "diagonal1": {"TL": " ", "MM": " ", "BR": " "},
            "diagonal2": {"TR": " ", "MM": " ", "BL": " "}
        }

        for way in self.ways_to_win:
            for sections in self.ways_to_win[way]:
                hashing[way][sections] = self.grid.get(sections)

        # self check
        # checking to see if it can make any winning moves
        for way in self.ways_to_win:
            count = 0
            empty = 0
            open_move = []
            for sections in self.ways_to_win[way]:
                if hashing[way][sections] == self.player_choices["bot_weapon"]:
                    count += 1
                if hashing[way][sections] == " ":
                    empty += 1
                    open_move.append(sections)
                if count == 2 and empty == 1:
                    # storing any winning moves into a list
                    win_moves.append(open_move[0])
                if count == 1 and empty == 2:
                    # storing a smart move
                    for item in open_move:
                        smart_move.append(item)

        # opp check
        # checking to see if the opponent can make any winning moves
        for way in self.ways_to_win:
            count = 0
            empty = 0
            open_move = []
            for sections in self.ways_to_win[way]:
                if hashing[way][sections] == self.player_choices["player1weapon"]:
                    count += 1
                if hashing[way][sections] == " ":
                    empty += 1
                    open_move.append(sections)
                if count == 2 and empty == 1:
                    # storing any opponent-winning moves into a list
                    defend_moves.append(open_move[0])
                if count == 1 and empty == 2:
                    # storing a smart move
                    for item in open_move:
                        smart_move.append(item)

        move = None
        # a winning move outweighs preventing the opponent from winning
        if len(win_moves) == 1:
            move = random.choice(win_moves)
        # however if there are no winning moves then it will prevent the opp from winning IF the opponent can make any
        elif len(win_moves) == 0 and len(defend_moves) > 0:
            move = random.choice(defend_moves)
        # if no one can make any winning moves, it selects a random move from al the remaining sections on the main grid
        elif len(win_moves) == 0 and len(defend_moves) and len(smart_move) > 0:
            move = random.choice(smart_move)
        else:
            move = random.choice(self.remaining_sections)

        self.grid[move] = self.player_choices["bot_weapon"]
        self.remaining_sections.remove(move)

    def check_intervals(self):
        if self.playing:
            counter = 0
            for section in self.grid:
                if self.grid[section] == " ":
                    pass
                else:
                    counter += 1
            for way in self.ways_to_win:
                x = 0
                o = 0
                for sections in self.ways_to_win[way]:
                    if self.grid[sections] == "x":
                        x += 1
                    elif self.grid[sections] == "o":
                        o += 1

                if x == 3:
                    print(f"{self.mapping.get('x')} has won")
                    self.playing = False
                    break
                elif o == 3:
                    print(f"{self.mapping.get('o')} has won")
                    self.playing = False
                    break
                else:
                    if counter == 9:
                        print("It's a tie")
                        self.playing = False
                        break
                    elif counter < 9:
                        pass

    def enter_selection(self):
        p1input = False
        bot_input = False
        self.check_intervals()

        # asking for player 1's input
        if self.playing:
            self.print_grid()
            while not p1input:
                player1input = str(input(f"{self.player1name}, input section to enter ur weapon: ")).upper()
                if player1input in self.remaining_sections:
                    self.grid[player1input] = self.player_choices["player1weapon"]
                    self.remaining_sections.remove(player1input)
                    self.check_intervals()
                    p1input = True
                else:
                    os.system("clear")
                    print("enter a correct or empty section")
                    self.print_grid()

        elif not self.playing:
            self.check_intervals()

        # asking for computer's input
        if self.playing:
            while not bot_input:
                self.print_grid()
                os.system("clear")
                self.computer()
                self.check_intervals()
                bot_input = True

        elif not self.playing:
            self.check_intervals()

    def registration(self):
        while not self.registered:
            player1 = Player(str(input("p1 enter name: ")), str(input("x or o: ")).lower())
            if player1.wp == "x":
                bot = Computer("o")
                self.player_choices["player1weapon"] = player1.wp
                self.player_choices["bot_weapon"] = bot.wp
                self.mapping[player1.wp] = player1.name
                self.mapping[bot.wp] = bot.bot_name
                self.player1name = player1.name
                self.bot_name = bot.bot_name
                self.registered = True

            elif player1.wp == "o":
                bot = Computer("x")
                self.player_choices["player1weapon"] = player1.wp
                self.player_choices["bot_weapon"] = bot.wp
                self.mapping[player1.wp] = player1.name
                self.mapping[bot.wp] = bot.bot_name
                self.player1name = player1.name
                self.bot_name = bot.bot_name
                self.registered = True
            else:
                print("please select either x or o")

    def play(self):
        # game loop
        while self.playing:
            self.intro()
            self.registration()
            self.enter_selection()

        else:
            self.print_grid()
            print("GAME FINISHED")


g1 = NoughtsAndCrosses()
g1.play()
