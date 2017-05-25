from client.beagle.beagle_api import api as BGL

class Tilemap():
    def __init__(self,**kwargs):
        BGL.auto_configurable.__init__(self,
            {
                "tilemap" : BGL.assets.get("CE-placeholder-art/tilemap/simple_game_room"),
                "color" : [1.0,1.0,1.0,1.0],
                "top_left" : [ -48, -48 ],
            }, **kwargs )

        self.tilemap_buffer = None

    def linkFloor( self, floor ):
        self.floor = floor

    def render(self):

        camera = self.floor.building.camera

        [ org_x , org_y ] = camera.translate_position( self.top_left )

        self.tilemap.set_view( self.floor.building.camera.get_view() )
        self.tilemap.render( org_x, org_y, camera.get_zoom() )
