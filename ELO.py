# ELO Module:
#   Functions:
#       match - receives two players, the game and who won, and changes their ELO value accordingly.
#           win=0 if player1 won win=1 if player2 won and win=0.5 if the game was a draw.
#       create_player - receives a name and a game and creates a user in the game table for that player.
#       get_user_elo - receives a player and a game and returns the player's ELO rating.
#       reset_user_elo - receives a player and a game and reset the player's ELO rating.
#       create_game - receives game name and creates a new game table.
#       delete_game - receives game name and deletes that game table.
#       show_game - receives game name and returns a list of tuples of players names and ELO ratings.


import sqlite3

K = 32
STARTING_ELO = 500.0
conn = sqlite3.connect("ELO.db")


def reset_user_elo(name, game):
    global STARTING_ELO, conn
    cur = conn.cursor()
    cur.execute("UPDATE'" + game + "' SET ELO="+str(STARTING_ELO)+" WHERE ID='"+name+"'")
    conn.commit()


def get_user_elo(name, game):
    global conn
    cur = conn.cursor()
    cur.execute("SELECT ELO FROM'" + game + "' WHERE ID='" + name + "'")
    elo = cur.fetchone()[0]
    return elo


def create_player(name, game):
    global STARTING_ELO, conn
    cur = conn.cursor()
    cur.execute("INSERT INTO'" + game + "' (ID, ELO) VALUES ('"+name+"', "+str(STARTING_ELO)+")")
    conn.commit()


def create_game(game):
    global conn
    conn.execute('''CREATE TABLE IF NOT EXISTS ''' + game + '''
                   ( ID TEXT PRIMARY KEY   ,
                   ELO           FLOAT    NOT NULL);''')


def delete_game(game):
    global conn
    conn.execute('DROP TABLE ' + game)


def show_game(game):
    cur = conn.cursor()
    cur.execute("SELECT * FROM'" + game)
    return cur.fetchall()


def match(player1, player2, win, game):
    #recalculates elo values gets elo rank of first and second player.
    #win = 0 if first player won win = 1 if second player won and win = 0.5 if tie.
    def calculate_elo(r1, r2, win):
        global K
        R1 = 10**(r1/400)
        R2 = 10**(r2/400)
        E1 = R1 / (R1 + R2)
        E2 = R2 / (R1 + R2)
        if win == "0":
            S1 = 1
            S2 = 0
        if win == "1":
            S1 = 0
            S2 = 1
        if win == "0.5":
            S1 = 0.5
            S2 = 0.5
        return r1 + K * (S1 - E1), r2 + K * (S2 - E2)

    global conn
    cur = conn.cursor()
    cur.execute("SELECT ELO FROM'" + game + "' WHERE ID='" + player1 + "'")
    plr1_elo = cur.fetchone()[0]
    cur.execute("SELECT ELO FROM'" + game + "' WHERE ID='" + player2 + "'")
    plr2_elo = cur.fetchone()[0]
    r1, r2 = calculate_elo(plr1_elo, plr2_elo, win)
    cur = conn.cursor()
    cur.execute("UPDATE'" + game + "' SET ELO="+str(r1)+" WHERE ID='"+player1+"'")
    cur = conn.cursor()
    cur.execute("UPDATE'" + game + "' SET ELO="+str(r2)+" WHERE ID='"+player2+"'")
    conn.commit()





