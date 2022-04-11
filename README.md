# Breaking Bad: A Dataset for Geometric Fracture and Reassembly

*Under review at SGP 2022*

Please visit [our website](https://breaking-bad-dataset.github.io) for more information.

## Accessing the dataset

Peer review anonymity constraints require that we use this repository to host our dataset prior to publication. Unfortunately, Github's file size limits make it impossible to host it here, as it exceeds 1 TB. Upon acceptance, we will migrate this website to a deanonymized host, where anyone will be able to download it in full.

Until then, we provide a *compressed* portion of our dataset, together with a python decompressor script that you can run to locally recover the `everyday` and `artifact` categories of our dataset. Proceed as follows (this assumes you have [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) installed):

1. Clone or download this repository
```bash
git clone git@github.com:Breaking-Bad-Dataset/Breaking-Bad-Dataset.github.io.git breaking-bad-dataset
```
2. Navigate to the compressed dataset
```bash
cd breaking-bad-dataset/compressed-dataset
```
3. Install dependencies
```bash
conda install -c conda-forge igl
```
4. Run decompressor script
```bash
python decompress.py [NAME_OF_SUBSET]
```
where [NAME_OF_SUBSET] is the name of any one of the folders in the `compressed-dataset` directory; for example, 
```bash
python decompress.py Bottle
```
If you ommit [NAME_OF_SUBSET] and just run `python decompress.py`, it will decompress the entire dataset. This will take a while.

After decompressing, the structure of the dataset will be
```
compressed-dataset/
├──── [category_name]/
│     ├──── [shape_name]/
│     |     |──── mode_0/
|     |     |     |──── piece_0.ply
•     •     •     •  
•     •     •     •
|     |     |     |──── piece_n.ply
•     •     •
•     •     •
|     |     |──── mode_19/
|     |     |     |──── piece_0.ply
•     •     •     •  
•     •     •     •
|     |     |     |──── piece_n.ply 
│     |     |──── fracture_0/
|     |     |     |──── piece_0.ply
•     •     •     •  
•     •     •     •
|     |     |     |──── piece_n.ply
•     •     •
•     •     •
|     |     |──── fracture_79/
|     |     |     |──── piece_0.ply
•     •     •     •  
•     •     •     •
|     |     |     |──── piece_n.ply 
```
