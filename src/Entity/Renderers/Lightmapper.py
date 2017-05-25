from client.beagle.beagle_api import api as BGL
from itertools import chain

class Lightmapper(BGL.auto_configurable):
    """ Renders a lightmap to a unit square 
    """

    primitive = BGL.primitive.unit_uv_square

    def __init__(self, **kwargs):

        BGL.auto_configurable.__init__(self,{
            'geometry' : [ [[-1.0,-1.0],[1.0,1.0]], [[1.0,-1.0],[-1.0,1.0]] ],
            'camera' : None
        }, **kwargs );

        self.shader = BGL.assets.get("beagle-2d-lightmap/shader/lightmap")
        self.t = 0.0

        encoded_geometry = Lightmapper.encode_geometry( self.geometry ) 
        self.shader.bind( { "geometry"  : [ encoded_geometry ], 
                            "num_p"     : [ len(encoded_geometry) ]
                          })

        self.target_buffer = BGL.framebuffer.from_dims(  int(kwargs['width']), int(kwargs['height']), filtered = True )
        self.lights = kwargs['lights']

    def encode_geometry( geometry ):
        return list(chain(*chain(*geometry)))

    def get_lightmap_texture(self):
        return self.target_buffer.get_texture()

    def get_lightmap_framebuffer(self):
        return self.target_buffer

    def compute(self):
        with BGL.context.render_target( self.target_buffer ):
            BGL.context.clear(0.0,0.0,0.0,1.0)
            for light in self.lights:
                with BGL.blendmode.add:
                    Lightmapper.primitive.render_shaded( self.shader, 
                        { 
                            "position"          : light["position"],
                            "light_color"       : light["color"],
                            "light_radius"      : light["radius"],
                            "view"              : self.camera.view,
                            "translation_world" : self.camera.translate_position([0.0,0.0]),
                            "scale_world"       : self.camera.get_scale()
                        })

