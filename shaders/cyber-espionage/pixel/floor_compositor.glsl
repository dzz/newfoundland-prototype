#version 330

// @description: composite the floor together

uniform sampler2D floor_buffer;
uniform sampler2D light_buffer;
uniform sampler2D object_buffer;
uniform sampler2D vision_buffer;

in vec2 uv;

void main(void) {

    vec4 floor_texel = texture(floor_buffer,uv);
    vec4 light_texel = texture(light_buffer,uv);
    vec4 object_texel = texture(object_buffer, uv);
    vec4 vision_texel = texture(vision_buffer, uv);

    // these are just some basics, to be parameterized and tweaked in the future 

    light_texel = light_texel * light_texel;
    vec4 lit_floor = ((light_texel*floor_texel)*1.0)*(1.0-object_texel.a);
    vec4 lit_object = (object_texel*0.7) + (object_texel*light_texel*0.3);

    lit_object.a = 1.0;

    gl_FragColor = (lit_floor + lit_object) * vision_texel;
    //gl_FragColor = vision_texel;
}

