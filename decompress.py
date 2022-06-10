import os
import time
import argparse

import numpy as np
from scipy.sparse import load_npz
import igl

ALL_CATEGORY = [
    'BeerBottle', 'Bowl', 'Cup', 'DrinkingUtensil', 'Mug', 'Plate', 'Spoon',
    'Teacup', 'ToyFigure', 'WineBottle', 'Bottle', 'Cookie', 'DrinkBottle',
    'Mirror', 'PillBottle', 'Ring', 'Statue', 'Teapot', 'Vase', 'WineGlass'
]
ALL_SUBSET = ['everyday', 'artifact', 'other']


def decompress(category_dir):
    if not os.path.isdir(category_dir):
        return
    print("Processing", category_dir)
    num_fracs = 0
    t0 = time.time()
    for mesh_dir in os.listdir(category_dir):
        mesh_dir_full_path = os.path.join(category_dir, mesh_dir)
        if not os.path.isdir(mesh_dir_full_path):
            continue
        # Read main mesh and data
        compressed_mesh_path = os.path.join(mesh_dir_full_path,
                                            "compressed_mesh.ply")
        compressed_data_path = os.path.join(mesh_dir_full_path,
                                            "compressed_data.npz")
        fine_vertices, fine_triangles = igl.read_triangle_mesh(
            compressed_mesh_path)
        piece_to_fine_vertices_matrix = load_npz(compressed_data_path)
        # Now, go over all fractures
        for frac_dir in os.listdir(mesh_dir_full_path):
            frac_dir_full_path = os.path.join(mesh_dir_full_path, frac_dir)
            if not os.path.isdir(frac_dir_full_path):
                continue
            # Load fracture data
            frac_data_path = os.path.join(frac_dir_full_path,
                                          "compressed_fracture.npy")
            piece_labels_after_impact = np.load(frac_data_path)
            # Now actually construct the meshes to write
            fine_vertex_labels_after_impact = \
                piece_to_fine_vertices_matrix @ piece_labels_after_impact
            n_pieces_after_impact = round(np.max(piece_labels_after_impact))
            for i in range(n_pieces_after_impact):
                tri_labels = \
                    fine_vertex_labels_after_impact[fine_triangles[:, 0]]
                if np.any(tri_labels == i):
                    vi, fi = igl.remove_unreferenced(
                        fine_vertices, fine_triangles[tri_labels == i, :])[:2]
                else:
                    continue
                ui, I, J, _ = igl.remove_duplicate_vertices(vi, fi, 1e-10)
                gi = J[fi]
                # Now we write the mesh ui, gi
                write_file_name = os.path.join(frac_dir_full_path,
                                               "piece_" + str(i) + ".ply")
                igl.write_triangle_mesh(write_file_name, ui, gi)
                num_fracs = num_fracs + 1
    total_time = time.time() - t0
    print("Decompressed a total of", str(num_fracs), "fracture pieces in",
          round(total_time, 3), "seconds.")


def process_everyday(data_root, category):
    if not os.path.isdir(os.path.join(data_root, 'everyday_compressed')):
        print('compressed everyday subset does not exist, skipping...')
        return
    if category.lower() == 'all':
        category = ALL_CATEGORY.copy()
    else:
        category = [category]
    for cat in category:
        cat_dir = os.path.join(data_root, 'everyday_compressed', cat)
        decompress(cat_dir)


def process_artifact(data_root):
    if not os.path.isdir(os.path.join(data_root, 'artifact_compressed')):
        print('compressed artifact subset does not exist, skipping...')
        return
    decompress(os.path.join(data_root, 'artifact_compressed'))


def process_other(data_root):
    if not os.path.isdir(os.path.join(data_root, 'other_compressed')):
        print('compressed other subset does not exist, skipping...')
        return
    decompress(os.path.join(data_root, 'other_compressed'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Data decompression')
    parser.add_argument('--data_root', required=True, type=str)
    parser.add_argument(
        '--subset',
        type=str,
        required=True,
        choices=ALL_SUBSET + [
            'all',
        ],
        help='data subset')
    parser.add_argument(
        '--category',
        type=str,
        default='all',
        choices=ALL_CATEGORY + [
            'all',
        ],
        help='category in everyday subset')
    args = parser.parse_args()

    if args.subset == 'all':
        subsets = ALL_SUBSET
    else:
        subsets = [args.subset]
    for subset in subsets:
        if subset == 'everyday':
            process_everyday(args.data_root, args.category)
        elif subset == 'artifact':
            process_artifact(args.data_root)
        elif subset == 'other':
            process_other(args.data_root)
        else:
            raise NotImplementedError('Unknown subset:', subset)
