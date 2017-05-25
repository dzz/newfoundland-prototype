from enum import Enum
from client.beagle.beagle_api import api as BGL

class Collision(Enum):
    #outer edges
    TOP = 0
    LEFT= 1
    BOTTOM = 2
    RIGHT = 3
    #through the middle
    VERTICAL = 4
    HORIZONTAL = 5
    #defined based on quadrant and is a 45 from the intersection between the two
    #middles of a tile as they cut through the respective quadrant
    SLASH_I = 6 # \ tr
    SLASH_II = 7 # / tl
    SLASH_III = 8 # \ bl
    SLASH_IV = 9 # / br
    #cutting the full tile just like the characters / and \
    FORWARD_SLASH = 10
    BACKWARD_SLASH = 11


class Tile(BGL.basic_sprite_renderer):

    def __init__(self,**kwargs):
        defaults = {
            'collisions':[]
        }
        defaults.update(kwargs)

        self.p = defaults['p']
        #list of Collision constants above that are applicable to this tile
        self.collisions = defaults['collisions']

        self.gid = defaults['gid']
        self.camera = defaults['camera']
        self.texture = BGL.assets.get("CE-placeholder-art/texture/tile_grass")

    def get_shader_params(self):
        return {
            "texBuffer"            : self.texture,
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 1.0, 1.0 ],
            "translation_world"    : self.camera.translate_position( self.p ),
            "scale_world"          : self.camera.get_scale(),
            "view"                 : self.camera.view,
            "rotation_local"       : 0,
            "filter_color"         : [ 1.0, 1.0, 1.0, 1.0],
            "uv_translate"         : [ 0,0 ] }
