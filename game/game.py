import curses


def wdwPrint(window, msg, y=0, x=0):
    window.erase()
    window.addstr(y, x, msg)
    window.refresh()

# shows the updated attributes after each fight
def calcAttrs(player, window):
    window.erase()
    window.addstr(0, 0, "Player: " + player.getName())
    window.addstr(1, 0, "HP: " + str(player.getHP()))
    window.addstr(2, 0, "Gold: " + str(player.getGold()))
    window.refresh()


def game(player, msg, side, art, stdscr):
    #Set backgrounds
    art.bkgd(' ', curses.color_pair(2))
    msg.bkgd(' ', curses.color_pair(3))
    side.bkgd(' ', curses.color_pair(1))

    #set up side panel
    calcAttrs(player, side)

    wdwPrint(art, "Monster")
    art.refresh()
    
    wdwPrint(msg, "I arrived at school on a chilly, windy morning.\nI hadn't slept too well last night, too much Math homework.\nAs I stepped up the ramp leading into the school, I saw…")
    msg.bkgd(' ', curses.color_pair(3))    
    msg.refresh()

    stdscr.getch()





if __name__ == "__main__":
    print("This file is not meant to be run by itself. Exiting.")
    exit()
