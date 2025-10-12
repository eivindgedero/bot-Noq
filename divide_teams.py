def divide_teams(players, size):
    return [players[i:i + size] for i in range(0, len(players), size)]