import xml.dom.minidom as minidom
import lxml.etree
from typing import List

class Lost(Exception):
    def __str__(self):
        return "element not found"

class Player(object):
    def __init__(self, name: str, number: int):
        self.name = name
        self.number = number

class Team(object):
    def __init__(self, name: str, id: int, players: List[Player]):
        self.id = id
        self.name = name
        self.players = players

class FootballClub(object):
    def __init__(self):
        self.teams = []
        self.players = []

    def add_team(self, team: Team):
        id = team.id
        for t in self.teams:
            if id == t.id:
                raise Lost
        self.teams.append(team)

    def add_player(self, player: Player):
        self.players.append(player)

    def save_to_xml(self, filename):
        doc = minidom.Document()
        footballclub_elem = doc.createElement("FootballClub")
        doc.appendChild(footballclub_elem)

        for team in self.teams:
            team_elem = doc.createElement("Team")
            team_elem.setAttribute("id", str(team.id))
            team_elem.setAttribute("name", team.name)
            footballclub_elem.appendChild(team_elem)

            for player in team.players:
                player_elem = doc.createElement("Player")
                player_elem.setAttribute("name", player.name)
                player_elem.setAttribute("number", str(player.number))
                team_elem.appendChild(player_elem)

        with open(filename, "w") as file:
            file.write(doc.toprettyxml(indent="  "))

    def load_from_xml(self, filename):
        doc = xml.dom.minidom.parse(filename)
        footballclub_elem = doc.documentElement

        team_nodes = footballclub_elem.getElementsByTagName("Team")
        for team_node in team_nodes:
            team_id = team_node.getAttribute("id")
            name = team_node.getAttribute("name")

            team_players = []
            player_nodes = team_node.getElementsByTagName("Player")
            for player_node in player_nodes:
                player_name = player_node.getAttribute("name")
                player_number = player_node.getAttribute("number")

                player = Player(name=player_name, number=int(player_number))
                team_players.append(player)

            team = Team(id=int(team_id), name=name, players=team_players)
            self.teams.append(team)

    @staticmethod
    def checkIsValid(filename) -> bool:
        xml_validator = lxml.etree.XMLSchema(lxml.etree.parse("schema.xsd"))
        xml_file = lxml.etree.parse(filename)
        is_valid = xml_validator.validate(xml_file)
        return is_valid
