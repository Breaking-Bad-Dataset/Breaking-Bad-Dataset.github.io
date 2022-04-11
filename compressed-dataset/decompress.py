# Include existing libraries
import numpy as np
from scipy.sparse import load_npz
# Libigl
import igl
# For paths
import os
# For profiling info
import time
# For argv
import sys

t0 = time.time()

parent_directory = "."
if len(sys.argv)>1:
    parent_directory = sys.argv[1]
    do_all = False
else:
    do_all = True

# For debug info
num_fracs = 0

if do_all:
    current_directory_enc = os.fsencode('.')
    for parent_directory_enc in os.listdir(current_directory_enc):
        parent_directory = os.fsdecode(parent_directory_enc)
        if os.path.isdir(parent_directory):
            for mesh_dir_enc in os.listdir(parent_directory_enc):
                mesh_dir = os.fsdecode(mesh_dir_enc)
                mesh_dir_full_path = os.path.join(parent_directory, mesh_dir)
                if os.path.isdir(mesh_dir_full_path):
                    # Read main mesh and data
                    compressed_mesh_path = os.path.join(parent_directory, mesh_dir, "compressed_mesh.ply")
                    compressed_data_path = os.path.join(parent_directory, mesh_dir, "compressed_data.npz")
                    fine_vertices, fine_triangles = igl.read_triangle_mesh(compressed_mesh_path)
                    piece_to_fine_vertices_matrix = load_npz(compressed_data_path)
                    # Now, go over all fractures
                    mesh_dir_full_path_enc = os.fsencode(mesh_dir_full_path)
                    for frac_dir_enc in os.listdir(mesh_dir_full_path_enc):
                        frac_dir = os.fsdecode(frac_dir_enc)
                        frac_dir_full_path = os.path.join(parent_directory, mesh_dir, frac_dir)
                        if os.path.isdir(frac_dir_full_path):
                            # Load fracture data
                            frac_data_path =  os.path.join(parent_directory, mesh_dir, frac_dir, "compressed_fracture.npy")
                            piece_labels_after_impact = np.load(frac_data_path)
                            #print(frac_data_path)
                            # Now actually construct the meshes to write
                            fine_vertex_labels_after_impact = piece_to_fine_vertices_matrix @ piece_labels_after_impact
                            n_pieces_after_impact = round(np.max(piece_labels_after_impact))
                            for i in range(n_pieces_after_impact):
                                tri_labels = fine_vertex_labels_after_impact[fine_triangles[:,0]]
                                if np.any(tri_labels==i):
                                    vi, fi = igl.remove_unreferenced(fine_vertices,fine_triangles[tri_labels==i,:])[:2]
                                else:
                                    continue
                                ui, I, J, _ = igl.remove_duplicate_vertices(vi,fi,1e-10)
                                gi = J[fi]
                                # Now we write the mesh ui, gi
                                write_file_name = os.path.join(frac_dir_full_path,"piece_" + str(i) + ".ply")
                                igl.write_triangle_mesh(write_file_name,ui,gi)
                                num_fracs = num_fracs + 1
else:
    # Let's start traversing the directory
    parent_directory_enc = os.fsencode(parent_directory)
    for mesh_dir_enc in os.listdir(parent_directory_enc):
        mesh_dir = os.fsdecode(mesh_dir_enc)
        mesh_dir_full_path = os.path.join(parent_directory, mesh_dir)
        if os.path.isdir(mesh_dir_full_path):
            # Read main mesh and data
            compressed_mesh_path = os.path.join(parent_directory, mesh_dir, "compressed_mesh.ply")
            compressed_data_path = os.path.join(parent_directory, mesh_dir, "compressed_data.npz")
            fine_vertices, fine_triangles = igl.read_triangle_mesh(compressed_mesh_path)
            piece_to_fine_vertices_matrix = load_npz(compressed_data_path)
            # Now, go over all fractures
            mesh_dir_full_path_enc = os.fsencode(mesh_dir_full_path)
            for frac_dir_enc in os.listdir(mesh_dir_full_path_enc):
                frac_dir = os.fsdecode(frac_dir_enc)
                frac_dir_full_path = os.path.join(parent_directory, mesh_dir, frac_dir)
                if os.path.isdir(frac_dir_full_path):
                    # Load fracture data
                    frac_data_path =  os.path.join(parent_directory, mesh_dir, frac_dir, "compressed_fracture.npy")
                    piece_labels_after_impact = np.load(frac_data_path)
                    #print(frac_data_path)
                    # Now actually construct the meshes to write
                    fine_vertex_labels_after_impact = piece_to_fine_vertices_matrix @ piece_labels_after_impact
                    n_pieces_after_impact = round(np.max(piece_labels_after_impact))
                    for i in range(n_pieces_after_impact):
                        tri_labels = fine_vertex_labels_after_impact[fine_triangles[:,0]]
                        if np.any(tri_labels==i):
                            vi, fi = igl.remove_unreferenced(fine_vertices,fine_triangles[tri_labels==i,:])[:2]
                        else:
                            continue
                        ui, I, J, _ = igl.remove_duplicate_vertices(vi,fi,1e-10)
                        gi = J[fi]
                        # Now we write the mesh ui, gi
                        write_file_name = os.path.join(frac_dir_full_path,"piece_" + str(i) + ".ply")
                        igl.write_triangle_mesh(write_file_name,ui,gi)
                        num_fracs = num_fracs + 1

t1 = time.time()
total_time = t1-t0
print("Decompressed a total of",str(num_fracs),"fracture pieces in",round(total_time,3),"seconds.")
