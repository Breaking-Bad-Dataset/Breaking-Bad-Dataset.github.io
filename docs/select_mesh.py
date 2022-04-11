import os
import copy
import argparse

import trimesh
import numpy as np
from scipy.spatial.transform import Rotation as R

parser = argparse.ArgumentParser()
parser.add_argument('--info_file', default='', type=str)
parser.add_argument('--data_dir', required=True, type=str)
parser.add_argument('--save_dir', required=True, type=str)
parser.add_argument('--num_obj', default=10, type=int)

args = parser.parse_args()

COLORS = np.array([
    [255, 128, 0, 255],
    [227, 26, 26, 255],
    [54, 125, 184, 255],
    [76, 173, 74, 255],
    [102, 194, 163, 255],
    [166, 214, 82, 255],
    [230, 138, 194, 255],
    [250, 140, 97, 255],
],
                  dtype=np.uint8)
TRANS = np.array([
    [0., -0.3, 1.5],
    [0., 0.3, 1.2],
    [0., 0.3, 1.8],
    [0., -0.3, 0.9],
    [0., -0.3, 2.1],
    [0., 0.3, 0.6],
    [0., 0.3, 2.4],
    [0., -0.3, 2.2],
])
PARTS = ((2, 2), (4, 4), (6, 6), (8, 8))
NUM_OBJ = args.num_obj
DATA_DIR = args.data_dir[:-1] if args.data_dir[-1] == '/' else args.data_dir
SAVE_DIR = args.save_dir[:-1] if args.save_dir[-1] == '/' else args.save_dir


def any_str_in(str, str_lst):
    """Check if any string in a list is in a string."""
    for s in str_lst:
        if s in str:
            return True
    return False


def check_collision(mesh, mesh_lst):
    """Check if a mesh collides with any other mesh in the list."""
    manager = trimesh.collision.CollisionManager()
    manager.add_object('object', mesh)
    for m in mesh_lst:
        min_dist = np.min([manager.min_distance_single(m)])
        if min_dist < 0.01:
            return True
    return False


def random_translate(mesh):
    """Randomly translate a mesh."""
    N = 0.3
    trans_vec = (np.random.rand(3) - 0.5) * 2. * N
    trans_vec[0] = 0.  # don't translate along x-axis
    mesh.apply_translation(trans_vec)
    return mesh


def translate_meshes(mesh_lst):
    """Translate each mesh so that they don't overlap."""
    trans = copy.deepcopy(TRANS)
    if len(mesh_lst) == 2:
        trans[0, 2] = trans[1, 2]
    for i, mesh in enumerate(mesh_lst):
        mesh.apply_translation(trans[i])
    ret_mesh = [mesh_lst[0]]
    for mesh in mesh_lst[1:]:
        while check_collision(mesh, ret_mesh):
            mesh = random_translate(mesh)
        ret_mesh.append(mesh)
    return ret_mesh


def read_part_meshes(mesh_dir):
    """Read all mesh parts under a directory."""
    mesh_files = os.listdir(mesh_dir)
    mesh_files.sort()
    meshes = [
        trimesh.load(os.path.join(mesh_dir, mesh_file))
        for mesh_file in mesh_files
    ]
    # TODO: need to rotate so that camera is front-facing
    rmat = R.from_euler(
        'xyz', np.array([-90, 0, 0.]), degrees=True).as_matrix()
    pmat = np.eye(4)
    pmat[:3, :3] = rmat
    for mesh in meshes:
        mesh.apply_transform(pmat)
    return meshes


def preprocess_part_meshes(mesh_lst, translate=False):
    """Translate and color each part mesh."""
    if translate:
        mesh_lst = translate_meshes(mesh_lst)
    for i, mesh in enumerate(mesh_lst):
        mesh.visual.vertex_colors = COLORS[i]
    return mesh_lst


def export_glb(mesh_lst, save_name):
    """Concat all meshes to a scene and export it to .glb format."""
    os.makedirs(os.path.dirname(save_name), exist_ok=True)
    s = trimesh.Scene([mesh_lst])
    _ = s.export(file_obj=f'{save_name}.glb')


def process_one_fracture(mesh_dir):
    """Process meshes belongs to one fracture.
    Load, translate, color, and export to .glb.
    """
    mesh_lst = read_part_meshes(mesh_dir)
    mesh_dir = f'{mesh_dir}_{len(mesh_lst)}pcs'
    # original mesh with different colors
    mesh_lst = preprocess_part_meshes(mesh_lst, translate=False)
    save_name = mesh_dir.replace(DATA_DIR, SAVE_DIR)
    export_glb(mesh_lst, save_name)
    # translated mesh with same colors
    mesh_lst = preprocess_part_meshes(mesh_lst, translate=True)
    save_name = mesh_dir.replace(DATA_DIR, SAVE_DIR) + '_transformed'
    export_glb(mesh_lst, save_name)


def sample_fractures(obj_dir):
    """Randomly pick fractures in one object for desired number of parts."""
    small_cat = [
        'Teapot', 'DrinkBottle', 'BeerBottle', 'Spoon', 'WineGlass',
        'PillBottle', 'Teacup', 'Ring', 'Statue', 'Cookie'
    ]

    def _select(parts):
        mesh_dirs = [os.path.join(obj_dir, d) for d in os.listdir(obj_dir)]
        np.random.shuffle(mesh_dirs)
        ret_dirs = []
        for part_num in parts:
            for mesh_dir in mesh_dirs:
                num_meshes = len(os.listdir(mesh_dir))
                if part_num[0] <= num_meshes <= part_num[1]:
                    ret_dirs.append(mesh_dir)
                    mesh_dirs.remove(mesh_dir)
                    break
        return ret_dirs

    ret_dirs = _select(PARTS)
    if len(ret_dirs) < len(PARTS) and any_str_in(obj_dir, small_cat):
        ret_dirs = _select(((2, 2), (2, 4), (2, 6), (2, 8)))
    assert len(ret_dirs) == len(PARTS)
    return ret_dirs


def sample_meshes(cat_dir):
    """Sample X objects from a category, Y meshes within each object."""
    if 'semantic' in cat_dir or 'scan' in cat_dir or 'sculpture' in cat_dir:
        all_obj_dirs = [os.path.join(cat_dir, d) for d in os.listdir(cat_dir)]
        obj_dirs = []
        category = cat_dir.split('/')[-1]
        assert args.info_file
        with open(args.info_file, 'r') as f:
            info = [
                line.strip() for line in f.readlines()
                if category in line.strip('/')
            ]
        for obj_dir in all_obj_dirs:
            if any_str_in(obj_dir, info):
                obj_dirs.append(obj_dir)
    else:
        obj_dirs = [os.path.join(cat_dir, d) for d in os.listdir(cat_dir)]
    np.random.shuffle(obj_dirs)
    ret_dirs, success = [], 0
    for obj_dir in obj_dirs:
        try:
            ret_dirs.extend(sample_fractures(obj_dir))
            success += 1
        except AssertionError:
            continue
        if success == NUM_OBJ:
            break
    return ret_dirs


cat_dirs = [os.path.join(DATA_DIR, d) for d in os.listdir(DATA_DIR)]
cat_dirs.sort()
for cat_dir in cat_dirs:
    obj_dirs = sample_meshes(cat_dir)
    print(f'Saving {len(obj_dirs)} fractures from {cat_dir}')
    for obj_dir in obj_dirs:
        process_one_fracture(obj_dir)
