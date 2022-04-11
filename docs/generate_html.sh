#!/bin/bash

DATA_DIR=$1
SAVE_DIR=$2
NUM_OBJ=$3

for cat in BeerBottle Bottle Bowl Cookie Cup DrinkBottle DrinkingUtensil Mirror Mug PillBottle Plate Ring Spoon Statue Teacup Teapot ToyFigure Vase WineBottle WineGlass
do
    cmd="python create_html.py --data_dir $DATA_DIR/$cat --save_dir $SAVE_DIR/$cat --html_file $cat.html --num_obj $NUM_OBJ"
    echo $cmd
    eval $cmd
done

DATA_DIR="${DATA_DIR/semantic/thingi10k}"
SAVE_DIR="${SAVE_DIR/semantic/thingi10k}"
cmd="python merge_scan_sculpture.py --data_dir $DATA_DIR"
echo $cmd
eval $cmd

cmd="python create_html.py --data_dir $DATA_DIR/artifact --save_dir $SAVE_DIR/artifact --html_file artifact.html --num_obj $NUM_OBJ"
echo $cmd
eval $cmd

cmd="python create_html.py --data_dir $DATA_DIR/other --save_dir $SAVE_DIR/other --html_file other.html --num_obj $NUM_OBJ"
echo $cmd
eval $cmd
