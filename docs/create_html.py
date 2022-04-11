import os
import shutil
import argparse

import numpy as np

HTML_HEAD = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="description" content="Breaking Bad Dataset" />
        <meta name="author" content="anonymous" />

        <title>Breaking Bad Dataset</title>
        <!-- Bootstrap core CSS -->
        <!--link href="bootstrap.min.css" rel="stylesheet"-->
        <link
            rel="stylesheet"
            href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
            integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
            crossorigin="anonymous"
        />

        <!-- Custom styles for this template -->
        <link href="offcanvas.css" rel="stylesheet" />
        <!--    <link rel="icon" href="img/favicon.gif" type="image/gif">-->
    </head>

    <body>
        <div class="jumbotron jumbotron-fluid">
            <div class="container">
                <h2>Breaking Bad Dataset</h2>
                <a href="index.html"><h4>Back to homepage</h4></a>
            </div>
        </div>
"""

HTML_TAIL = """
                <!-- Loads <model-viewer> for modern browsers: -->
                <script
                    type="module"
                    src="https://unpkg.com/@google/model-viewer/dist/model-viewer.js"
                ></script>
            </div>

            <hr />
        </div>

        <script
            src="https://code.jquery.com/jquery-3.5.1.slim.min.js"
            integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
            crossorigin="anonymous"
        ></script>
        <script
            src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"
            integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo"
            crossorigin="anonymous"
        ></script>
        <script
            src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js"
            integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI"
            crossorigin="anonymous"
        ></script>
    </body>
</html>
"""

CATEGORY_HEAD = """
        <div class="container">
            <div class="section">
                <h2>{category}</h2>
                <hr />
                <p>
                    We show randomly selected fractures of {category} category
                    from the dataset. Click the text to download the data.
                </p>
                <div class="container">
"""

CATEGORY_TAIL = """
                </div>
"""

ROW1 = """
                    <div class="row align-items-center">
                        <div class="col-md-3 padding-0 canvas-row">
                            <a href="{src1}" download="{fn1}"><h4>{title1}</h4></a>
                            <model-viewer
                                alt="Object"
                                src="{src1}"
                                style="
                                    width: 100%;
                                    height: 250px;
                                    background-color: #FFFFFF;
                                "
                                exposure=".8"
                                camera-orbit="90deg 90deg 105%"
                                auto-rotate
                                camera-controls
                            >
                            </model-viewer>
                        </div>
                        <div class="col-md-3 padding-0 canvas-row">
                            <a href="{src2}" download="{fn2}"><h4>{title2}</h4></a>
                            <model-viewer
                                alt="Object"
                                src="{src2}"
                                style="
                                    width: 100%;
                                    height: 250px;
                                    background-color: #FFFFFF;
                                "
                                exposure=".8"
                                camera-orbit="90deg 90deg 105%"
                                auto-rotate
                                camera-controls
                            >
                            </model-viewer>
                        </div>
                        <div class="col-md-3 padding-0 canvas-row">
                            <a href="{src3}" download="{fn3}"><h4>{title3}</h4></a>
                            <model-viewer
                                alt="Object"
                                src="{src3}"
                                style="
                                    width: 100%;
                                    height: 250px;
                                    background-color: #FFFFFF;
                                "
                                exposure=".8"
                                camera-orbit="90deg 90deg 105%"
                                auto-rotate
                                camera-controls
                            >
                            </model-viewer>
                        </div>
                        <div class="col-md-3 padding-0 canvas-row">
                            <a href="{src4}" download="{fn4}"><h4>{title4}</h4></a>
                            <model-viewer
                                alt="Fracture"
                                src="{src4}"
                                style="
                                    width: 100%;
                                    height: 250px;
                                    background-color: #FFFFFF;
                                "
                                exposure=".8"
                                camera-orbit="90deg 90deg 105%"
                                auto-rotate
                                camera-controls
                            >
                            </model-viewer>
                        </div>
                    </div>
"""

ROW2 = """
                    <div class="row align-items-center">
                        <div class="col-md-3 padding-0 canvas-row">
                            <model-viewer
                                alt="Object"
                                src="{src1}"
                                style="
                                    width: 100%;
                                    height: 250px;
                                    background-color: #FFFFFF;
                                "
                                exposure=".8"
                                camera-orbit="90deg 90deg 105%"
                                auto-rotate
                                camera-controls
                            >
                            </model-viewer>
                        </div>
                        <div class="col-md-3 padding-0 canvas-row">
                            <model-viewer
                                alt="Object"
                                src="{src2}"
                                style="
                                    width: 100%;
                                    height: 250px;
                                    background-color: #FFFFFF;
                                "
                                exposure=".8"
                                camera-orbit="90deg 90deg 105%"
                                auto-rotate
                                camera-controls
                            >
                            </model-viewer>
                        </div>
                        <div class="col-md-3 padding-0 canvas-row">
                            <model-viewer
                                alt="Object"
                                src="{src3}"
                                style="
                                    width: 100%;
                                    height: 250px;
                                    background-color: #FFFFFF;
                                "
                                exposure=".8"
                                camera-orbit="90deg 90deg 105%"
                                auto-rotate
                                camera-controls
                            >
                            </model-viewer>
                        </div>
                        <div class="col-md-3 padding-0 canvas-row">
                            <model-viewer
                                alt="Fracture"
                                src="{src4}"
                                style="
                                    width: 100%;
                                    height: 250px;
                                    background-color: #FFFFFF;
                                "
                                exposure=".8"
                                camera-orbit="90deg 90deg 105%"
                                auto-rotate
                                camera-controls
                            >
                            </model-viewer>
                        </div>
                    </div>
"""


def convert_windows_path(path):
    return path.replace('\\', '/')


parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', required=True, type=str)
parser.add_argument('--save_dir', required=True, type=str)
parser.add_argument('--html_file', required=True, type=str)
parser.add_argument('--num_obj', default=10, type=int)

args = parser.parse_args()

args.data_dir = convert_windows_path(args.data_dir)
args.save_dir = convert_windows_path(args.save_dir)
args.html_file = convert_windows_path(args.html_file)

DATA_DIR = args.data_dir[:-1] if args.data_dir[-1] == '/' else args.data_dir
SAVE_DIR = args.save_dir[:-1] if args.save_dir[-1] == '/' else args.save_dir
NUM_OBJ = args.num_obj
HTML_FILE = args.html_file
NUM_OBJ = args.num_obj
CATEGORY = DATA_DIR.split('/')[-1]
assert SAVE_DIR.split('/')[-1] == CATEGORY
assert CATEGORY in HTML_FILE

# create html file
html = HTML_HEAD + CATEGORY_HEAD.format(category=CATEGORY)

# data_dir will be 'data/webpage_data/semantic/Bottle'
# save_dir will be 'data/src/semantic/Bottle'
# html_file will be 'Bottle.html'
obj_dirs = [os.path.join(DATA_DIR, d) for d in os.listdir(DATA_DIR)]
np.random.shuffle(obj_dirs)
for i, obj_dir in enumerate(obj_dirs[:NUM_OBJ]):
    mesh_files = [os.path.join(obj_dir, f) for f in os.listdir(obj_dir)]
    num_pcs = [int(f[-8]) for f in mesh_files if '_transformed' not in f]
    num_pcs.sort()
    # we take meshes following the order
    downloads, row1, row2, pieces = [], [], [], []
    for num in num_pcs:
        for f in mesh_files:
            if '_transformed' not in f and f[-8] == str(num):
                # f will be 'xxx/Bottle/abcdefgh/fractured_30_2pcs.glb'
                ori_mesh, ori_mesh_save = f, f.replace(DATA_DIR, SAVE_DIR)
                ori_mesh_save = convert_windows_path(ori_mesh_save)
                trans_mesh = f'{f[:-4]}_transformed.glb'
                trans_mesh_save = trans_mesh.replace(DATA_DIR, SAVE_DIR)
                trans_mesh_save = convert_windows_path(trans_mesh_save)
                row1.append(ori_mesh_save)
                row2.append(trans_mesh_save)
                pieces.append(f'{num} pieces')
                downloads.append(
                    f"{CATEGORY}{i}-{ori_mesh_save.split('/')[-1]}")
                os.makedirs(os.path.dirname(ori_mesh_save), exist_ok=True)
                shutil.copy(ori_mesh, ori_mesh_save)
                shutil.copy(trans_mesh, trans_mesh_save)
                mesh_files.remove(f)
                break
    # compose html lines
    html += ROW1.format(
        title1=pieces[0],
        title2=pieces[1],
        title3=pieces[2],
        title4=pieces[3],
        fn1=downloads[0],
        fn2=downloads[1],
        fn3=downloads[2],
        fn4=downloads[3],
        src1=row1[0],
        src2=row1[1],
        src3=row1[2],
        src4=row1[3],
    )
    html += ROW2.format(
        src1=row2[0],
        src2=row2[1],
        src3=row2[2],
        src4=row2[3],
    )

html = html + CATEGORY_TAIL + HTML_TAIL
# write html file
with open(HTML_FILE, 'w') as f:
    f.write(html)
