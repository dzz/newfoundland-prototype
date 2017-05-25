from random import shuffle

from client.beagle.beagle_api import api as BGL

from .Entity.Controllers import Controllers
from .Entity.Player import Player
from .Entity.Building import Building
from .Entity.Camera import Camera


class CyberEspGame(BGL.game, BGL.simple_tick_manager):

    NUM_TEST_PLAYERS = 1

    def __init__(self):
        BGL.simple_tick_manager.__init__(self)

    def tick(self):
        BGL.simple_tick_manager.tick(self)

        ( x, y ) = 0.9 * self.players[0].p[0], 0.9 * self.players[0].p[1]
        self.camera.p = [x,y]


    def init(self):
        self.camera = Camera( p = [0.0,0.0], zoom = 0.5 )
        self.controllers = self.create_tickable( Controllers() )
        self.players = []

        self.building = self.create_tickable( Building( width = 200, height = 200, camera = self.camera, players = self.players ) )

        starting_positions = [
            [-7.0,-7.0],
            #[-5.0,0.0],
            #[ 5.0,0.0],
            #[ 0.0,5.0],
            #[ 0.0,-5.0],
            #[ -5.0,-5.0],
            #[ 5.0,5.0],
            #[ 0.0,0.0],
            #[ 0.25,-0.25]
        ]

        shuffle( starting_positions )
        for num in range(0,CyberEspGame.NUM_TEST_PLAYERS):
            self.players.append(self.create_tickable(Player( num = num, p = starting_positions[num] , controllers = self.controllers, camera = self.camera )))

    def render(self):
        self.building.render()
