import os
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', required=True, type=str)
args = parser.parse_args()

scan_dir = os.path.join(args.data_dir, 'scan')
sculpture_dir = os.path.join(args.data_dir, 'sculpture')
artifact_dir = os.path.join(args.data_dir, 'artifact')
os.makedirs(artifact_dir, exist_ok=True)

scans = os.listdir(scan_dir)
sculptures = os.listdir(sculpture_dir)
sculptures = [s for s in sculptures if s not in scans]

for scan in scans:
    shutil.copytree(
        os.path.join(scan_dir, scan), os.path.join(artifact_dir, scan))
for sculpture in sculptures:
    shutil.copytree(
        os.path.join(sculpture_dir, sculpture),
        os.path.join(artifact_dir, sculpture))
