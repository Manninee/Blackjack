# TIE-02100 Introduction to Programming
# Eetu Manninen, eetu.manninen@tuni.fi
#
# Blackjack:
# The objective is to beat the dealer in one of three ways:
# Get score of 21 with 2 or more cards
# Get higher score than dealer without exceeding 21
# Dealer's score exceed 21 and yours does not
#
# Face cards equal 10 points, ace equals 1 or 11 my program automatically
# decides which if score goes higher than 21. At the start of the game
# everybody gets two cards except the dealer. Players play their turns and
# after the final player has played his/her turn dealer gets its cards.
#
# How to use:
# At the start program defaults to one player. Player count can be change in
# the setting under "Players". Setting changes only take effect after new game
# is created. In the setting deck count can be also changed (deck count means
# how many same cards can be on the table at the same time).
# To start game press new game after you have selected player count and deck
# count, then  press start game.
# In the settings there is also stats which opens a new window and show stats
# about players, wins and losses
#
# How to play:
# To get more cards press "Hit"
# To end your turn press "Stand"
#
# My program is scalable because player count is changeable by changing the
# constant MAX_PLAYERS. The only thing that severely limits the player count
# is the _number_text list that is used for selection menus to present numbers
# with letters. If MAX_PLAYERS is set really high the the cards will run out
# and then MAX_NUMBER_OF_DECKS would also have to be raised to allow more of
# the same cards to be on the table at the same time.


from tkinter import *
import random


CARDS = {"clubs": ["ace_c.gif", "c2.gif", "c3.gif", "c4.gif", "c5.gif",
                   "c6.gif", "c7.gif", "c8.gif", "c9.gif", "c10.gif",
                   "jack_c.gif", "queen_c.gif", "king_c.gif", ],
         "spades": ["ace_s.gif", "s2.gif", "s3.gif", "s4.gif", "s5.gif",
                    "s6.gif", "s7.gif", "s8.gif", "s9.gif", "s10.gif",
                    "jack_s.gif", "queen_s.gif", "king_s.gif"],
         "hearts": ["ace_h.gif", "h2.gif", "h3.gif", "h4.gif", "h5.gif",
                    "h6.gif", "h7.gif", "h8.gif", "h9.gif", "h10.gif",
                    "jack_h.gif", "queen_h.gif", "king_h.gif"],
         "diamonds": ["ace_d.gif", "d2.gif", "d3.gif", "d4.gif", "d5.gif",
                      "d6.gif", "d7.gif", "d8.gif", "d9.gif", "d10.gif",
                      "jack_d.gif", "queen_d.gif", "king_d.gif"]}

MAX_NUMBER_OF_DECKS = 3
MAX_PLAYERS = 6
FILE_NAME = "stats.txt"


class Player:
    def __init__(self):
        self.__points = 0
        self.__name = "Player"
        self.__cards = []

        # How many ace
        self.__aces = 0
        self.__outcome = ""

    def __int__(self):
        return self.__points

    def __str__(self):
        return self.__name

    def add_card(self, card_number):
        """
        Adds cards to the player and check if the card is and ace
        :param card_number: Int, number of card
        :return: None
        """
        self.__cards.append(card_number)

        # Checks if the card is an ace
        if card_number % 100 == 0:
            self.__aces += 1

        # Calculates new points
        self.calculate_points(card_number)

    def calculate_points(self, card_number):
        """
        Adds points the amount of given card
        :param card_number: Int, number of card
        :return: None
        """
        __card = card_number % 100

        # card is ace
        if __card == 0:
            self.__points += 11

        # card is 10 or higher
        elif __card >= 9:
            self.__points += 10
        else:
            self.__points += __card + 1

        # If points go above 21 and player has and ace the ace's value is 1
        if self.__points > 21 and self.__aces > 0:
            self.__aces -= 1
            self.__points -= 10

    def get_cards(self):
        return self.__cards

    def give_name(self, name):
        self.__name = name

    def give_points(self, points):
        self.__points = points

    def clear_cards(self):
        self.__cards.clear()
        self.__aces = 0

    def get_outcome(self):
        return self.__outcome

    def set_outcome(self, outcome):
        self.__outcome = outcome


class Blackjack:
    def __init__(self):
        self.__window = Tk()
        self.__window.title("Blackjack Game")
        self.__window.resizable(False, False)

        self.__font = ("Helvetica", 10)

        self.__card_families = ["clubs", "spades", "hearts", "diamonds"]

        # Numbers as text for selection menus
        _number_text = ["One", "Two", "Three", "Four", "Five", "Six", "Seven",
                        "Eight", "Nine", "Ten"]

        # Loads card pictures
        self.__cards = {}
        for card_family in CARDS:
            self.__cards[card_family] = []
            for card_file in CARDS[card_family]:
                card = PhotoImage(file=card_file)
                self.__cards[card_family].append(card)

        # Creates Players
        self.__player_list = {}
        for i in range(MAX_PLAYERS + 1):
            self.__player_list[i] = Player()

        # Dictionary for player stats
        self.__player_stats = {}

        # Dictionary for every player's UI elements
        self.__player_ui_elements = {}

        # Indicates which player is in turn
        self.__player_turn = 0

        # Variable for disabling and enabling automatic turn ending
        self.__auto_turn_end_check = False

        # Variable for player count with default 1 player
        self.__players = IntVar()
        self.__players.set(2)

        # Variable for how many players are in play
        self.__player_count = self.__players.get()

        # Variable for deck count
        self.__decks = IntVar()
        self.__decks.set(1)

        # Variable for how many decks are in play
        self.__decks_in_play = self.__decks.get()

        self.__menu_bar = Menu(self.__window)
        self.__window.config(menu=self.__menu_bar)

        __settings_menu = Menu(self.__menu_bar, tearoff=False)
        __player_menu = Menu(__settings_menu, tearoff=False)
        __decks_menu = Menu(__settings_menu, tearoff=False)

        self.__menu_bar.add_cascade(label="Settings", menu=__settings_menu)
        __settings_menu.add_command(label="Stats",
                                    command=self.stats_window)
        __settings_menu.add_cascade(label="Players", menu=__player_menu)
        __settings_menu.add_cascade(label="Decks", menu=__decks_menu)

        self.__menu_bar.add_command(label="New Game",
                                    command=self.new_game)
        self.__menu_bar.add_command(label="Start Game",
                                    command=self.start_game)
        self.__menu_bar.add_command(label="Quit",
                                    command=self.__window.destroy)

        # Creates selection for the dice count
        for i in range(MAX_NUMBER_OF_DECKS):
            __decks_menu.add_radiobutton(label=_number_text[i],
                                         variable=self.__decks, value=(i + 1))

        # Creates selection for the player count
        for i in range(MAX_PLAYERS):
            __player_menu.add_radiobutton(label=_number_text[i],
                                          variable=self.__players,
                                          value=i + 2)

        # Creates frame for the buttons
        self.__button_frame = Frame(self.__window)

        # Creates button for getting more cards
        self.__hit_button = Button(self.__button_frame, command=self.hit)
        self.__hit_button.config(text="\n\n Hit \n\n", font=self.__font)

        # Creates button for ending turn
        self.__stand_button = Button(self.__button_frame,
                                     command=self.next_turn)
        self.__stand_button.config(text="\n\n Stand \n\n", font=self.__font)

        # Show buttons
        self.__button_frame.grid(column=0, sticky="NWE")
        self.__hit_button.grid(row=0, column=0, sticky="NWE")
        self.__stand_button.grid(row=1, column=0, sticky="NWE")

        # Create player uis
        for player in range(MAX_PLAYERS + 1):
            self.create_player_ui(player)

        # Show dealer's ui
        self.show_player_ui(0)

        # Gets game ready to play
        self.new_game()

    def create_player_ui(self, player):
        """
        Creates user interface elements
        :param player: Int player whose UI is being created
        :return: None
        """

        self.__player_ui_elements[player] = {}

        # Create frame for player
        _player_frame = Frame(self.__window)
        _player_frame.config(relief=RIDGE, bd=5)
        self.__player_ui_elements[player][1] = _player_frame

        # Create frame for player's cards
        self.__player_ui_elements[player][2] = Frame(_player_frame)

        # Create label for player
        _new_name_label = Label(_player_frame, font=self.__font)

        # If player is dealer no player name
        if player == 0:
            _label_text = "Dealer"
        else:
            _label_text = "Player {:d}".format(player)
        _new_name_label.configure(text=_label_text)
        self.__player_ui_elements[player][3] = _new_name_label

        # Create label for player's points
        _new__points_label = Label(_player_frame, font=self.__font)
        _new__points_label.configure(text="Points = {:d}"
                                     .format(int(self.__player_list[player])))
        self.__player_ui_elements[player][4] = _new__points_label

        # If player is dealer don't create entry for player name
        if player != 0:

            # Create entry for player name
            _new_entry = Entry(_player_frame, font=self.__font)

            # Save default text for the entry
            _new_entry.insert(END, "Player {:d}".format(player))

            self.__player_ui_elements[player][5] = _new_entry

    def set_stats(self, stats):
        """
        Saves stats from the file to the internal dictionary
        :param stats: Dict, saved stats from the file
        :return: None
        """
        self.__player_stats = stats

    def stats_window(self):
        """
        Creates and shows the window for the stats
        :return: None
        """

        # Create window for stats with fixed size
        __stats_window = Toplevel()
        __stats_window.title("Stats")
        __stats_window.minsize(375, 450)
        __stats_window.maxsize(375, 450)
        __stats_window.resizable(False, False)
        __stats_window.transient(self.__window)

        __scrollbar = Scrollbar(__stats_window)
        __scrollbar.pack(side=RIGHT, fill=Y)

        __menu = Menu(__stats_window)
        # Creates button to clear saved stats, save them to the file and reopen
        # the stats window
        __menu.add_command(label="Clear stats",
                           command=lambda: [self.__player_stats.clear(),
                                            save_stats(self.__player_stats),
                                            __stats_window.destroy(),
                                            self.stats_window()])
        # Creates button to quit stats window
        __menu.add_command(label="Quit", command=__stats_window.destroy)
        __stats_window.config(menu=__menu)

        __stats_list = Listbox(__stats_window)
        __scrollbar.config(command=__stats_list.yview)
        __stats_list.config(font=("Courier", 12), bg="grey")

        # Parses the first line containing titles
        __stats_list.insert(END, "{:<15s}{:>5s}{:>7s}{:>6s}"
                            .format("Name", "Wins", "Losses", "Games"))

        # Goes trough every player in alphabetical order
        for player in sorted(self.__player_stats.keys(),
                             key=lambda x: x.casefold()):

            # Parses players row containing name, wins, losses and played games
            __player_string = "{:<15s}{:>5d}{:>7d}{:>6d}"\
                .format(player,
                        self.__player_stats[player]["wins"],
                        self.__player_stats[player]["losses"],
                        self.__player_stats[player]["total"])

            __stats_list.insert(END, __player_string)

        # Shows list full window
        __stats_list.pack(fill=BOTH, expand=1)

    def show_player_ui(self, player):
        """
        Show player's user interface
        :param player: Int, player whose user interface is wanted to be shown
        :return: None
        """

        # Shows player's frame
        self.__player_ui_elements[player][1].grid(row=0, column=player + 1,
                                                  sticky="NWE")

        # Shows player card frame
        self.__player_ui_elements[player][2].grid(row=3, sticky="NWE")

        # Shows player's player label
        self.__player_ui_elements[player][3].grid(row=0, sticky="WE")

        # Shows player's points label
        self.__player_ui_elements[player][4].grid(row=2, sticky="WE")

        # If player is dealer skip the name entry
        if player != 0:
            self.__player_ui_elements[player][5].grid(row=1)

    def reset_game(self):
        """
        Resets game information for a new game
        :return: None
        """

        # Disable automatic turn end check
        self.__auto_turn_end_check = False

        # Unlock start game button
        self.__menu_bar.entryconfig("Start Game", state=NORMAL)

        # Lock Stand and Hit buttons
        self.__stand_button.config(state=DISABLED)
        self.__hit_button.config(state=DISABLED)

        # Goes through every player except dealer
        for _player in range(1, MAX_PLAYERS + 1):

            # Resets players points
            self.__player_list[_player].give_points(0)

            # Resets name field lock
            self.__player_ui_elements[_player][5].config(state=NORMAL)

            # Hides Player's ui elements
            self.__player_ui_elements[_player][1].grid_forget()

            # Resets player's outcome
            self.set_player_outcome(_player, "reset")

            # Clears player cards
            self.clear_player_cards(_player)
            self.show_points(_player)

        # Clear dealer's cards and points
        self.reset_player(0)

        # Shows dealer's card frame
        self.__player_ui_elements[0][2].grid(row=3, column=0)

        # Clear data of unused players
        for _player in range(self.__player_count, MAX_PLAYERS + 1):
            self.reset_player(_player)

        # Resets whose turn it is
        self.__player_turn = 0

    def reset_player(self, player):
        """
        Resets player's name, points and player label to the defaults and
        clears cards from the user interface
        :param player: Int, player whose info are being reset
        :return: None
        """

        # If player is dealer skip renaming
        if player != 0:
            # Reset player name
            _entry_text = "Player {:d}".format(player)
            self.__player_ui_elements[player][5].configure(text=_entry_text)

            # Resets player's saved name
            self.__player_list[player].give_name("Player")

        # Resets player's outcome
        self.set_player_outcome(player, "reset")

        # Resets player's saved points
        self.__player_list[player].give_points(0)
        self.show_points(player)

        # Clears players cards from the user interface
        self.clear_player_cards(player)

    def clear_player_cards(self, player):
        """
        Erases player's cards from the user interface and clears saved cards
        :param player: Int, player whose cards are being erased
        :return: None
        """

        # Destroys player's whole card frame
        self.__player_ui_elements[player][2].grid_forget()
        self.__player_ui_elements[player][2].destroy()

        # Creates new card frame for the player
        _player_frame = self.__player_ui_elements[player][1]
        self.__player_ui_elements[player][2] = Frame(_player_frame)

        # Clears player's saved cards
        self.__player_list[player].clear_cards()

    def new_game(self):
        """
        Saves how many player and decks are in play and calls for reset of the
        game and for showing of the player's user interfaces
        :return: None
        """
        # Saves how many decks are in play
        self.__player_count = self.__players.get()

        # Saves how many players are in play
        self.__decks_in_play = self.__decks.get()

        # Resets game
        self.reset_game()

        # Shows the user interfaces of used players
        for player in range(1, self.__players.get()):
            self.show_player_ui(player)

    def start_game(self):
        """
        Sets needed buttons disabled and enable, locks name fields and
        gets two cards for every player and one for the dealer
        :return: None
        """

        # Lock star game button
        self.__menu_bar.entryconfig("Start Game", state=DISABLED)

        # Unlock Stand and Hit buttons
        self.__stand_button.config(state=NORMAL)
        self.__hit_button.config(state=NORMAL)

        # Lock name fields
        for __player in range(1, MAX_PLAYERS + 1):
            self.__player_ui_elements[__player][5].config(state=DISABLED)

        # One card for dealer
        self.get_and_show_card(0)
        self.show_points(0)

        for _player in range(1, self.__player_count):

            # Save player's names
            _player_name = self.__player_ui_elements[_player][5].get()
            self.__player_list[_player].give_name(_player_name)

            # Two cards per player
            for __cards in range(2):
                self.get_and_show_card(_player)

            self.show_points(_player)

        # Allow automatic turn check
        self.__auto_turn_end_check = True

        # Start first turn
        self.next_turn()

    def check_card(self, card_whole_number):
        """
        Checks if too many of the wanted cards are in play compared to the
        amount of decks in play
        :param card_whole_number: Int, number of the card to be checked
        :return: False if too many of the same card is in play otherwise True
        """

        # Calculates how many of the wanted cards are in play
        number_of_cards = 0
        for _player in self.__player_list:

            # Check individual player's cards
            for _card in self.__player_list[_player].get_cards():

                # If card is found add to the amount
                if _card == card_whole_number:
                    number_of_cards += 1

        # If too many card are already in play return False
        if number_of_cards >= self.__decks_in_play:
            return False
        else:
            return True

    def get_and_show_card(self, player):
        """
        Randomizes a new card for the player and the shows it
        :param player: Int,
        :return: None
        """

        while True:
            _card_family = random.randint(0, 3)
            _card_number = random.randint(0, 12)

            # Calculate card number
            _card_whole_number = _card_family * 100 + _card_number

            # Check if too many of the selected cards are already in play
            if self.check_card(_card_whole_number):
                break

        # Save card to the player
        self.__player_list[player].add_card(_card_whole_number)

        # Get card from the list of cards
        _card = self.__cards[self.__card_families[_card_family]][_card_number]

        # Create new place for the card
        _new_card_label = Label(self.__player_ui_elements[player][2])

        # Show card
        _new_card_label.config(image=_card)
        _new_card_label.grid()

        self.automatic_turn_end_check(player)

    def parse_end_turn_message(self, player):
        """
        Parses the message for the turn end screen
        :param player:
        :return _whole_msg: String, message that is shown in end turn screen
        """

        # Parses message for turn end

        # Gets previous player's name and outcome
        _prev_player = str(self.__player_list[player - 1])
        _prev_player_outcome = self.__player_list[player - 1].get_outcome()

        # If previous player didn't win or lose the outcome is ended turn
        if _prev_player_outcome == "":
            _prev_player_outcome = "ended turn"

        # If game began change first line text
        if player == 1:
            _first_line = "> Game has begun <"
        else:
            _first_line = "> {:s} has {:s} <".format(_prev_player,
                                                     _prev_player_outcome)

        # Get whose turn it is an parse second line
        _current_player = str(self.__player_list[player])
        _second_line = "{:s} it is your turn".format(_current_player)

        # Parse whole message
        _whole_msg = "{:s}\n{:s}".format(_first_line, _second_line)

        return _whole_msg

    def parse_end_screen_message(self):
        """
        Parses end screen message to show who won if anybody
        :return _message: String, message to be shown in the end screen
        """
        # Gets every player with outcome "won" in to a list
        _winners_list = []
        for player in self.__player_list:
            if self.__player_list[player].get_outcome() == "won":
                _winners_list.append(str(self.__player_list[player]))

        # Adds all the winners to the string
        _sorted_winner_list = sorted(_winners_list, key=lambda x: x.casefold())
        _message = "> Winners are <\n" + "\n".join(_sorted_winner_list)

        # If there is no winners changes message to show that
        if len(_winners_list) == 0:
            _message = "> There are no\nwinners"

        return _message

    def full_window_message(self, msg_text, colour="gold"):
        """
        Creates and show full window message
        :param msg_text: String, message to be shown
        :param colour: String, background colour of the message
        :return: None
        """

        _message = Message(self.__window)

        # Place message on top of the window
        _message.grid(row=0, column=0, columnspan=MAX_PLAYERS + 3,
                      sticky="news")

        # Sets messages settings
        _message.config(text=msg_text, font=("Helvetica", 22),
                        background=colour, aspect=1000)

        # Destroy message after 3 seconds
        _message.after(1000, lambda: _message.destroy())

    def hit(self):
        self.get_and_show_card(self.__player_turn)
        self.show_points(self.__player_turn)

    def next_turn(self):
        """
        Places next player to turn
        :return: None
        """

        # If previous has not won or lost then return the original colour
        if self.__player_list[self.__player_turn].get_outcome() == "":
            self.set_player_outcome(self.__player_turn, "")

        # Places next player to turn
        self.__player_turn += 1
        # If all players have played then go to dealer's turn and end game
        if self.__player_count == self.__player_turn:

            # Continue here for dealers turn
            self.dealers_turn()

            self.game_end()
            return

        else:
            # Checks if player has already won with his/her first two cards
            self.automatic_turn_end_check(self.__player_turn)

            # Only if automatic_turn_end_check ends final player's turn
            if self.__player_count == self.__player_turn:
                return

            # Show turn end screen
            self.full_window_message(self.parse_end_turn_message(
                self.__player_turn))

            # Sets player as the current player
            self.set_player_outcome(self.__player_turn, "current")

    def dealers_turn(self):
        """
        Gives dealer cards until its points are 17 or over
        :return: None
        """

        # Lock Stand and Hit buttons
        self.__stand_button.config(state=DISABLED)
        self.__hit_button.config(state=DISABLED)

        # Disables turn end check
        self.__auto_turn_end_check = False

        # Suppress dealer's colour change
        self.set_player_outcome(0, "reset")

        while int(self.__player_list[0]) < 17:
            self.get_and_show_card(0)
            self.show_points(0)

    def show_points(self, player):
        """
        Updates player's points to the label under the player's name
        :param player: Int, player whose points are being updated
        :return: None
        """

        if player != MAX_PLAYERS + 1:
            _points_label = self.__player_ui_elements[player][4]
            _player_points = int(self.__player_list[player])
            _points_label.config(text="Points = {:d}".format(_player_points))

    def automatic_turn_end_check(self, player):
        """
        Checks if player has either won or lost and ends turn accordingly
        :param player: Int, player whose outcome is being checked
        :return: None
        """

        if self.__auto_turn_end_check:
            # Updates player's points before
            self.show_points(player)

            # If player's point are 21 set player as "won" and end turn
            if int(self.__player_list[player]) == 21:
                self.set_player_outcome(player, "won")
                self.full_window_message(self.parse_end_turn_message(player))
                self.next_turn()

            # If player's point are over 21 set player as "lost" and end turn
            elif int(self.__player_list[player]) > 21:
                self.set_player_outcome(player, "lost")
                self.full_window_message(self.parse_end_turn_message(player))
                self.next_turn()

    def game_end(self):
        """
        Checks every player's outcome and calls for showing of the end screen
        and the saving of the stats
        :return: None
        """
        # Checks every player's outcome
        for player in range(1, self.__player_count):
            _player_points = self.__player_list[player]

            # If player got 21 automatic won
            if int(_player_points) == 21:
                self.set_player_outcome(player, "won")

            # If player got over 21 automatic loss
            elif int(_player_points) > 21:
                self.set_player_outcome(player, "lost")

            else:

                # If player's points are below 21 but dealer's are not
                # so player wins
                if int(_player_points) < 21 < int(self.__player_list[0]):
                    self.set_player_outcome(player, "won")

                # If player's and dealer's points are below 21 but player's
                # points are over dealer's points so player wins
                elif int(_player_points) > int(self.__player_list[0]):
                    self.set_player_outcome(player, "won")

                else:
                    self.set_player_outcome(player, "lost")

        # Shows ending screen
        self.full_window_message(self.parse_end_screen_message())

        # Add stats to the internal dict
        self.add_stats()

        # Saves stats to the file
        save_stats(self.__player_stats)

    def set_player_outcome(self, player, outcome):
        """
        Sets player outcome and player's frame perimeter colour
        :param player: Int, player whose
        :param outcome: String, indicates player's state
        :return: None
        """

        if outcome == "won":
            self.__player_ui_elements[player][1].config(bg="green")

        elif outcome == "lost":
            self.__player_ui_elements[player][1].config(bg="red")

        # Player not in turn
        elif outcome == "":
            self.__player_ui_elements[player][1].config(bg="SystemButtonFace")

        # Player in turn
        elif outcome == "current":
            self.__player_ui_elements[player][1].config(bg="orange")
            return

        elif outcome == "reset":
            self.__player_list[player].set_outcome("")
            self.__player_ui_elements[player][1].config(bg="SystemButtonFace")
            return

        # Save players state to the player
        self.__player_list[player].set_outcome(outcome)

    def add_stats(self):
        """
        Adds stats to the internal dictionary
        :return: None
        """

        # Goes through every player
        for player in range(1, self.__player_count):

            # Gets player name and the outcome of the game
            _name = str(self.__player_list[player])
            _outcome = self.__player_list[player].get_outcome()

            # If new player create entry with default values
            if _name not in self.__player_stats:
                self.__player_stats[_name] = {}
                self.__player_stats[_name]["wins"] = 0
                self.__player_stats[_name]["losses"] = 0
                self.__player_stats[_name]["total"] = 0

            # Adds one to the correct outcome
            if _outcome == "won":
                self.__player_stats[_name]["wins"] += 1
            elif _outcome == "lost":
                self.__player_stats[_name]["losses"] += 1

            # Adds one to the total amount of played games
            self.__player_stats[_name]["total"] += 1

    def start(self):
        self.__window.mainloop()


def save_stats(stats):
    """
    Saves stats to a external file
    :param stats: Dict, contains stats that are being saved to the file
    :return: None
    """
    try:
        _file = open(FILE_NAME, "w", encoding="UTF-8")
        for player in stats:

            # Makes a list of player's stats
            _player_as_list = [player,
                               str(stats[player]["wins"]),
                               str(stats[player]["losses"]),
                               str(stats[player]["total"])]

            # Writes one player in one line
            _file.write(";".join(_player_as_list) + "\n")

        _file.close()
    except FileNotFoundError:
        pass
    except ValueError:
        pass


def read_stats_file():
    """
    Reads game stats from an external file and saves them in a dict.
    File contains one line for one user name;wins;losses;played games\n
    :return: player_stats Dict, saved stats
    """
    player_stats = {}

    try:
        file = open(FILE_NAME, "r", encoding="UTF-8")

        for row in file:

            # Gets players info from the row
            name, wins, losses, total = row.strip().split(";")
            player_stats[name] = {}
            player_stats[name]["wins"] = int(wins)
            player_stats[name]["losses"] = int(losses)
            player_stats[name]["total"] = int(total)

        file.close()
        return player_stats

    except FileNotFoundError:
        return {}
    except ValueError:
        return {}


def main():
    user_interface = Blackjack()
    user_interface.set_stats(read_stats_file())
    user_interface.start()


main()
