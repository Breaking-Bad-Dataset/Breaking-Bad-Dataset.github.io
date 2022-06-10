# Breaking Bad: A Dataset for Geometric Fracture and Reassembly

*Under review at NeurIPS 2022 Datasets and Benchmarks Track*

Please visit [our website](https://breaking-bad-dataset.github.io) for more information.

## Accessing the dataset

We provide a compressed version of our dataset, together with a python decompressor script that you can run to locally decompress it. Proceed as follows (this assumes you have [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) installed):

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
