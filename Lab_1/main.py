from FootballClub import Player, Team, FootballClub

if __name__ == '__main__':
    football_club = FootballClub()

    player1 = Player("Messi", 10)
    player2 = Player("Ronaldo", 7)
    player3 = Player("Neymar", 11)

    try:
        football_club.add_player(player1)
        football_club.add_player(player2)
        football_club.add_player(player3)
    except Exception as e:
        print(e)

    team1 = Team("Barcelona", 1, [player1, player3])
    team2 = Team("Real Madrid", 2, [player2])

    try:
        football_club.add_team(team1)
        football_club.add_team(team2)
    except Exception as e:
        print(e)

    print("IS VALID ", football_club.checkIsValid("data.xml"))
    football_club.save_to_xml("data.xml")

