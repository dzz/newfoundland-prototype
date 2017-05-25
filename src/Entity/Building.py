from client.beagle.beagle_api import api as BGL
from .Floor import Floor

class Building( BGL.basic_sprite_renderer, BGL.auto_configurable, BGL.simple_tick_manager ):
    """ Holds floors and goals info per mission, each mission will have one building
    each building will have one or more floors
    """
    def __init__(self, **kwargs):
        BGL.auto_configurable.__init__(self,
            {
                'width':100.0,
                'height':100.0,
                'floors': self.getDefaultFloors(),
                'texture' : BGL.assets.get("CE-placeholder-art/texture/arena"),
                'camera' : None,
                'players' : []
            }, **kwargs )

        BGL.simple_tick_manager.__init__(self)
        for floor in self.floors:
            self.linkFloor( floor )

    def linkFloor(self, floor):
        floor.linkBuilding(self)
        self.create_tickable( floor )

    def getDefaultFloors(self):
        return [ Floor() ] 

    def get_shader_params(self):
        return {
            "texBuffer"            : self.texture,
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ self.width, self.height ],
            "translation_world"    : self.camera.translate_position([0.0,0.0]),
            "scale_world"          : self.camera.get_scale(),
            "view"                 : self.camera.view,
            "rotation_local"       : 0.0,
            "filter_color"         : [ 1.0, 1.0, 1.0, 1.0],
            "uv_translate"         : [ 0,0 ] }

    def render(self):
        BGL.basic_sprite_renderer.render(self)
        for floor in self.floors:
            if floor.is_visible():
                floor.render()
