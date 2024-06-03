from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from django.http import HttpResponse
from .models import Team, Player
from django.views.decorators.csrf import csrf_exempt

class SoapService(ServiceBase):
    @rpc(Integer, _returns=Iterable(Unicode))
    def get_team_info(ctx, team_id):
        try:
            team = Team.objects.get(id=team_id)
            yield f"Team Name: {team.name}"
            yield "Players:"
            for player in team.players.all():
                yield f" - {player.name}, Position: {player.position}, Number: {player.number}"
        except Team.DoesNotExist:
            yield "Team not found"

application = Application([SoapService],
                          tns='http://example.com/football',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

django_soap_app = csrf_exempt(DjangoApplication(application))
