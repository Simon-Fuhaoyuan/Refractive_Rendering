import os
from tqdm import tqdm
import random
import argparse
import copy


OBJECT_ROOT = '/home/haoyuan/rendering/data/objects/'
OBJECT_DEFINITION = \
'object {\n\
    shape\n\
    #ifdef (mask)\n\
        pigment {color ${COLOR}}\n\
    #else\n\
        texture {\n\
            pigment{\n\
                color filter 1\n\
                #ifdef (Calib) transmit 1 #else transmit ${Trans} #end\n\
            }\n\
        }\n\
        interior {\n\
            ior ${IOR} \n\
            #ifndef (Calib)\n\
                fade_distance ${FadeD} fade_power ${FadeP}\n\
            #end\n\
        }\n\
    #end\n\
    scale     ${SC}\n\
    rotate    z*${RotZ}\n\
    rotate    y*${RotY}\n\
    translate x*${TX}\n\
    translate y*${TY}\n\
}'
BG_ROOT = '/disk1/data/coco/train2017'

camera_parameters = {
    'cl_x': [0.00], # Camera Location
    'cl_y': [0.00], 
    'cl_z': [-4.5, -3.5], 
    'lk_x': [0.00], # Camera Look At
    'lk_y': [0.00],
    'lk_z': [0.00],
    'cs_x': [0.00], # Camera Sky
    'cam_a': [1.00], # Aspect ratio
    'cam_z': [1.50, 2.00], # Zoom
    'bg_sc': [2.50, 3.50], # Background Scale
    'bg_pz': [3.02],
    'bg_rx': [0.00], # Background Rotation
    'bg_ry': [0.00], 
    'bg_rz': [0.00], 
    'Dim': [0.85, 1.00], # Ambient intensity
}

object_parameters = {
    'COLOR': ['Green'], # Category Color
    'Trans': [1.00], # Transmit
    'SC': [0.3, 0.5], # Scale
    'IOR': [1.3, 1.5], # Index of Refraction
    'RotZ': [-180, 180], # Object Rotation
    'RotY': [-180, 180],
    'TX': [0.00], # Object Translation
    'TY': [0.00],
    'FadeD': [1.63], # Fade Distance
    'FadeP': [1001.00], # Fade Power
}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', '-m', default='0')
    args = parser.parse_args()

    return args

def update_counter(counter_file, cnt):
    with open(counter_file, 'w') as f:
        f.write(str(cnt) + '\n')

def set_environ(mode):
    return 'counter'

def generate_parameter(parameter):
    if len(parameter) == 0:
        return []
    elif len(parameter) == 1:
        return parameter[0]
    else:
        return random.random() * (parameter[1] - parameter[0]) + parameter[0]

def randomize_object_parameters(object_name):
    # TODO: assign the color for each category
    parameters = copy.deepcopy(object_parameters)
    for key, value in parameters.items():
        parameters[key] = generate_parameter(value)
    
    return parameters

def randomize_camera_parameters():
    parameters = copy.deepcopy(camera_parameters)
    for key, value in parameters.items():
        parameters[key] = generate_parameter(value)
    
    return parameters

def value2str(value):
    if type(value) == float:
        return '%.2f' % value
    elif type(value) == str:
        return value
    else:
        return '~'

def generate_setting(template_file, objects_list, output):
    template = ''
    with open(template_file, 'r') as f:
        template = f.read()
    indices = random.sample(range(0, len(objects_list)), random.randint(1, 3))
    # print(indices)
    for i in range(len(indices)):
        index = indices[i]
        inc_file = os.path.join(OBJECT_ROOT, objects_list[index])
        added_code = '#include \"%s\"' % inc_file
        replace_inc = '// include_file%d' % (i + 1)
        template = template.replace(replace_inc, added_code)

        parameters = randomize_object_parameters(objects_list[index])
        object_definition = copy.deepcopy(OBJECT_DEFINITION)
        object_definition = object_definition.replace('shape', objects_list[index][:-4])
        for key, value in parameters.items():
            object_definition = object_definition.replace('${' + key + '}', value2str(value))
        replace_object = '// object%d' % (i + 1)
        template = template.replace(replace_object, object_definition)
    # print(template)
    with open(output, 'w') as f:
        f.write(template)

def generate_shell(shell_file, bg_list, output):
    template = ''
    with open(shell_file, 'r') as f:
        template = f.read()
    parameters = randomize_camera_parameters()
    for key, value in parameters.items():
            template = template.replace('${' + key + '}', value2str(value))
    index = random.randint(0, len(bg_list) - 1)
    background = os.path.join(BG_ROOT, bg_list[index])
    template = template.replace('${COCOImage}', background)
    print(template)
    with open(output, 'w') as f:
        f.write(template)

def generate(counter_file):
    objects_list = os.listdir(OBJECT_ROOT)
    backgrounds_list = os.listdir(BG_ROOT)
    for i in range(1):
        generate_setting('data/new_template.pov', objects_list, 'data/runtime_template.pov')
        generate_shell('template_render.sh', backgrounds_list, 'runtime_render.sh')
        os.putenv('obj', str(i + 1))
        os.system('bash runtime_render.sh')
        update_counter(counter_file, i)
        

if __name__ == '__main__':
    args = parse_args()
    counter_file = set_environ(int(args.mode))
    generate(counter_file)
