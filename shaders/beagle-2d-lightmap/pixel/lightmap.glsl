#version 330 core

in vec2 uv;
uniform vec2 position;
uniform vec2 view;
uniform vec2 translation_world;
uniform vec2 scale_world;
uniform vec4 light_color;
uniform int num_p;
uniform float light_radius;
uniform float geometry[512];

float RayToLineSegment(float x, float y, float dx, float dy, float x1, float y1, float x2, float y2)
{
    float r;
    float s;
    float d;

    if (dy / dx != (y2 - y1) / (x2 - x1))
    {
        d = ((dx * (y2 - y1)) - dy * (x2 - x1));
        if (d != 0)
        {
            r = (((y - y1) * (x2 - x1)) - (x - x1) * (y2 - y1)) / d;
            s = (((y - y1) * dx) - (x - x1) * dy) / d;
            if (r >= 0 && s >= 0 && s <= 1)
            {
                return r;
                //return { x: x + r * dx, y: y + r * dy };
            }
        }
    }
    return 1.0;
}

void main(void) {

    vec2 mod_uv = (uv*2)-vec2(1.0,1.0);
    vec2 position_normalized = (position+translation_world) * scale_world * view;
    float dist_to_position = distance( position_normalized, mod_uv*0.5 );
    float pixel_sees_position = 1.0;
    float mod_light_radius = length((vec2(light_radius,light_radius)+translation_world)*scale_world * view);

    if(dist_to_position>mod_light_radius) {
        pixel_sees_position = 0.0;
    } else {
            for( int idx = 0; idx < num_p; idx+=4 ) {
                    float offs = float(idx)*2;
                    vec2 line_a = (vec2(geometry[idx], geometry[idx+1]) + translation_world) * scale_world * view;
                    vec2 line_b = (vec2(geometry[idx+2], geometry[idx+3]) + translation_world) * scale_world * view;
                    float intersection_distance = RayToLineSegment( position_normalized.x, position_normalized.y, mod_uv.x - position_normalized.x, mod_uv.y - position_normalized.y, line_a.x, line_a.y, line_b.x, line_b.y);
                    if( intersection_distance < 1.0) {
                            pixel_sees_position = 0.0;
                            break;
                    } 
            }
    }

    vec4 outputColor = light_color * (1.0-(dist_to_position/mod_light_radius)) * pixel_sees_position;

    gl_FragColor = outputColor;
    //gl_FragColor = vec4( 1.0,0.0,1.0,1.0) * dist_to_position;
}
