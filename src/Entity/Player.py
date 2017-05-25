from math import atan2
from client.beagle.beagle_api import api as BGL

class Player(BGL.basic_sprite_renderer, BGL.auto_configurable):
    def __init__(self, **kwargs):
        BGL.auto_configurable.__init__(self,
            {
                "num" : 0,
                "speed" : 0.1,
                "controllers" : None,
                "p" : [ 0.0, 0.0 ],
                "dir" : [ 0.0, 1.0 ],
                "rads" : 0.0,
                "texture" : BGL.assets.get("CE-placeholder-art/texture/player"),
                "camera" : None,
                "site_radius" : 10.0
            }, **kwargs)
        self.texture = BGL.assets.get("CE-placeholder-art/texture/player")

    def tick(self):
        pad = self.controllers.get_virtualized_pad( self.num )

        self.p[0] = self.p[0] + (pad.left_stick[0])*self.speed;
        self.p[1] = self.p[1] + (pad.left_stick[1])*self.speed;

        self.dir = ( pad.right_stick[0], pad.right_stick[1] )
        self.rads = atan2( self.dir[1], self.dir[0] )

    def get_shader_params(self):
        return {
            "texBuffer"            : self.texture,
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 1.0, 1.0 ],
            "translation_world"    : self.camera.translate_position( self.p ),
            "scale_world"          : self.camera.get_scale(),
            "view"                 : self.camera.view,
            "rotation_local"       : self.rads,
            "filter_color"         : [ 1.0, 1.0, 1.0, 1.0],
            "uv_translate"         : [ 0,0 ] }
