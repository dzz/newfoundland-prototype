from client.beagle.beagle_api import api as BGL
from .Object import Object
from .Renderers.FloorRenderer import FloorRenderer
from .FloorObjectTickManager import FloorObjectTickManager
from .Drivers.WobbleDriver import WobbleDriver
from .Drivers.ColorCycler import ColorCycler
from .Tilemap import Tilemap

class Floor(FloorRenderer, FloorObjectTickManager, BGL.auto_configurable):
    """ Represents a floor in a building 
    """
    def __init__(self, **kwargs):
        BGL.auto_configurable.__init__(self,
            {
                'width':75.0,
                'height':75.0,
                'objects': self.getDefaultObjects(),
                'camera' : None,
                'building' : None,
                'tilemap' : Tilemap()
            }, **kwargs )

        FloorObjectTickManager.__init__(self)

        self.tilemap.linkFloor(self)
        for obj in self.objects:
            self.linkObject(obj)

    def linkObject(self, obj):
        """ Link an object to this floor
        """
        obj.setFloor(self)
        self.create_tickable(obj)

    def linkBuilding(self, building):
        """ Link this floor to a parent building
        """
        self.building = building
        FloorRenderer.__init__(self)

    def getDefaultObjects(self):
        """ Return a default 'scene' of objects
        """
        def testLightingRig():
            """ Make objects with lighting properties set
            """
            tex_radial = BGL.assets.get("CE-lights/texture/radial")
            tex_flare = BGL.assets.get("CE-lights/texture/flare")
            return [ 
                Object( size = [1.0,1.0], p = [ -5.0, 5.0 ] ),
                Object( size = [1.0,1.0], p = [ 0.0, 0.0 ] ),
                Object( size = [1.0,1.0], p = [ 5.0, -5.0 ] ),
                ## static raytraced lights
                Object( visible = False, light_type = Object.LightTypes.STATIC_SHADOWCASTER, 
                        p = [ -3, -3 ], light_radius=5.0, color = [ 0.6,0.1,0.0,1.0 ] ),

                Object( visible = False, light_type = Object.LightTypes.STATIC_SHADOWCASTER, 
                        p = [ 3, -3 ], light_radius=5.0, color = [ 0.2,0.5,0.9,1.0 ] ),
                ## cheap (but artistic!) overlay sprite (notice size vs. radius, its just a sprite )

                Object( visible = False, light_type = Object.LightTypes.STATIC_TEXTURE_OVERLAY, 
                         p = [ -9, 5 ], size = [12.0,12.0], color = [ 0.1,0.08,0.6,1.0 ], texture = tex_radial ),

                Object( visible = False, light_type = Object.LightTypes.STATIC_TEXTURE_OVERLAY, 
                         p = [ 9, 5 ], size = [24.0,24.0], color = [ 0.1,0.08,0.6,1.0 ], texture = tex_flare ),

                Object( visible = False, light_type = Object.LightTypes.STATIC_TEXTURE_OVERLAY, 
                         p = [ 9, 5 ], size = [24.0,24.0], color = [ 0.1,0.08,0.6,1.0 ], texture = tex_flare ),

                Object( visible = False, light_type = Object.LightTypes.STATIC_TEXTURE_OVERLAY, 
                         p = [ 9, 5 ], size = [48.0,48.0], color = [ 0.3,0.8,0.6,1.0 ], texture = tex_flare ),

                ## expensive(fun) raytraced lights
                Object( visible = False, light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER, 
                        p = [ 0, 0 ], light_radius=34.0, color = [ 0.0,0.0,1.0,1.0 ], drivers = [ WobbleDriver() ] ),

                Object( visible = False, light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER, 
                        p = [ 0, 0 ], light_radius=7.0, color = [ 1.0,0.0,1.0,1.0 ], drivers = [ WobbleDriver( a=0.1,b=-0.2, radius=4.0) ] ),

                Object( visible = False, light_type = Object.LightTypes.DYNAMIC_SHADOWCASTER, 
                        p = [ 0, 0 ], light_radius=10.0, color = [ 1.0,0.0,1.0,1.0 ], drivers = [ ColorCycler(), WobbleDriver( a=-0.3,b=0.4, radius=7.0) ] ),
                ## 
                Object( visible = False, light_type = Object.LightTypes.DYNAMIC_TEXTURE_OVERLAY, 
                        p = [ 0, 3 ], size=[14.5,14.5], color = [ 0.2,0.1,0.01,1.0 ], texture = tex_flare, drivers = [ WobbleDriver( a=-0.03,b=0.08, radius=4.0), ColorCycler() ] )
            ]
        return testLightingRig()

    def tick(self):
        #FloorRenderer.precompute_frame(self)
        FloorObjectTickManager.tick(self)

    def get_occluders(self):
        """ return (in floor-space) coordinates to occluder geometry
        """
        def testLightingRigOccluders():
            """ generates sample data
            """
            #squares = [ [-3.4,3.4,2.5], [6.0,5.5,4.2] ,[-7.0,-4.5,3.2], [-25,-4,7] ]

            squares = [[-5.0,5.0,1.0], [0.0,0.0,1.0], [5.0,-5.0,1.0]]

            room = []
            for (offs_x, offs_y, scale) in squares:
                data = [[[-1.0,-1.0],[1.0,-1.0]],[[-1.0,1.0],[1.0,1.0]],[[-1.0,-1.0],[-1.0,1.0]],[[1.0,-1.0],[1.0,1.0]]]
                for line in data:
                    for coord in line:
                        coord[0] = (coord[0]*scale)+offs_x
                        coord[1] = (coord[1]*scale)+offs_y
                room.extend(data)
            return room
        return testLightingRigOccluders()

    def is_visible(self):
        """ if this floor is visible
        """
        return True

