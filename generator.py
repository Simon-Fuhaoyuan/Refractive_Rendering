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

# options
OUT_DIRS = ['Images_Glass/', 'Images_Lens/', 'Images_Complex/', 'Images_Debug/']
CATEGORIES = ['Glass/', 'Lens/', 'Complex/', 'Glass/']
FILES = ['train_glass_obj.txt', 'train_lens_obj.txt', 'train_complex_obj.txt', 'train_glass_obj.txt']
COUNTER = ['counter_glass', 'counter_lens', 'counter_complex', 'counter_debug']
SETTINGS = ['setting_glass.pov', 'setting_lens.pov', 'setting_complex.pov', 'setting_debug.pov']

camera_parameters = {
    'cl_x': [0.00], # Camera Location
    'cl_y': [0.00], 
    'cl_z': [0.00], 
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
    'COLOR': [], # Category Color
    'Trans': [1.00], # Transmit
    'SC': [0.3, 0.5], # Scale
    'IOR': [1.3, 1.5], # Index of Refraction
    'RotZ': [-180, 180], # Object Rotation
    'RotY': [-180, 180],
    'TX': [], # Object Translation
    'TY': [],
    'FadedD': [1.63], # Fade Distance
    'FadedP': [1001.00], # Fade Power
}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', '-m', default='0')
    args = parser.parse_args()

    return args

def update_counter(counter_file, cnt):
    with open(counter_file, 'w') as f:
        f.write(str(cnt))

def set_environ(mode):
    objects_list_file = FILES[mode]
    objects_path_prefix = OBJECT_ROOT + CATEGORIES[mode]
    counter_file = COUNTER[mode]

    os.putenv('objects_prefix', objects_path_prefix)
    os.putenv('outDir', OUT_DIRS[mode])
    os.putenv('setting', os.path.join('./data/', SETTINGS[mode]))

    return objects_list_file, counter_file


def generate_setting(template_file, objects_list):
    template = ''
    with open(template_file, 'r') as f:
        template = f.read()
    indices = random.sample(range(0, len(objects_list)), random.randint(1, 3))
    print(indices)
    for i in range(len(indices)):
        index = indices[i]
        inc_file = os.path.join(OBJECT_ROOT, objects_list[index])
        added_code = '#include \"%s\"' % inc_file
        replacement_key = '// include_file%d' % (i + 1)
        template = template.replace(replacement_key, added_code)
    print(template)

def generate(counter_file):
    objects_list = os.listdir(OBJECT_ROOT)
    generate_setting('data/new_template.pov', objects_list)
    exit()
    for i in range(1):
        
        

        os.putenv('obj', str(i + 1))
        

        # os.system('bash debug_render.sh')
        update_counter(counter_file, i)
        

if __name__ == '__main__':
    args = parse_args()
    counter_file = set_environ(int(args.mode))
    generate(counter_file)
    
