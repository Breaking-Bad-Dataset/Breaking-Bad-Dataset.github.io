#!/bin/bash

# script for downloading zip files from Dataverse and unziping them
# comment out subsets you don't want to download
# if this doesn't work, please download manually from Dataverse (https://doi.org/10.5683/SP3/LZNPKB)

# README
wget -O README.md "https://olrc2.scholarsportal.info/dataverse/10.5683/SP3/LZNPKB/1814f2c30d5-b3731db536d6?response-content-disposition=attachment%3B%20filename%2A%3DUTF-8%27%27README.md&response-content-type=text%2Fmarkdown&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220610T200246Z&X-Amz-SignedHeaders=host&X-Amz-Expires=7200&X-Amz-Credential=33b141c798354e21a3394e9e4f546bbe%2F20220610%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=e23b704336c297beca5368ce1eba4728f3bd55bfcd06eedbad9ba0526fe55838"

# data split, this is necessary
wget -O data_split.tar.gz "https://olrc2.scholarsportal.info/dataverse/10.5683/SP3/LZNPKB/1814f1d4284-ebffc06cfe78?response-content-disposition=attachment%3B%20filename%2A%3DUTF-8%27%27data_split.tar.gz&response-content-type=application%2Fx-gzip&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220610T200017Z&X-Amz-SignedHeaders=host&X-Amz-Expires=7200&X-Amz-Credential=33b141c798354e21a3394e9e4f546bbe%2F20220610%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=1ddef173078bdcc5e36ae392a8fdcdef74c7c5975ade51ae8649516eb85392ff"
tar -zxvf data_split.tar.gz

# everyday subset
wget -O everyday_compressed.zip "https://olrc2.scholarsportal.info/dataverse/10.5683/SP3/LZNPKB/1814598f602-1537545e4ae5?response-content-disposition=attachment%3B%20filename%2A%3DUTF-8%27%27everyday_compressed.zip&response-content-type=application%2Fzip&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220610T200109Z&X-Amz-SignedHeaders=host&X-Amz-Expires=7200&X-Amz-Credential=33b141c798354e21a3394e9e4f546bbe%2F20220610%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=3306b63f9a4e36b8bed5e2be0867ff18c17f4b39cab69238416d719e445397d7"
unzip everyday_compressed.zip

# artifact subset
wget -O artifact_compressed.zip "https://olrc2.scholarsportal.info/dataverse/10.5683/SP3/LZNPKB/181459705b3-f054ffea8838?response-content-disposition=attachment%3B%20filename%2A%3DUTF-8%27%27artifact_compressed.zip&response-content-type=application%2Fzip&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220610T200115Z&X-Amz-SignedHeaders=host&X-Amz-Expires=7200&X-Amz-Credential=33b141c798354e21a3394e9e4f546bbe%2F20220610%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=fc54b630d58d75dea6b61ffe32f5e7729d1ae4e583fd5ef8b31db1360ed37830"
unzip artifact_compressed.zip

# other subset, which consists of 4 splitted zip files
wget -O other_compressed_split.zip.001 "https://olrc2.scholarsportal.info/dataverse/10.5683/SP3/LZNPKB/181459be0a2-4c9d8538bcbf?response-content-disposition=attachment%3B%20filename%2A%3DUTF-8%27%27other_compressed_split.zip.001&response-content-type=application%2Foctet-stream&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220610T200312Z&X-Amz-SignedHeaders=host&X-Amz-Expires=7200&X-Amz-Credential=33b141c798354e21a3394e9e4f546bbe%2F20220610%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=f55e7cebd2095da83f339ac1d076c972208ccdedcd136bfebb84e29a08cf8d93"
wget -O other_compressed_split.zip.002 "https://olrc2.scholarsportal.info/dataverse/10.5683/SP3/LZNPKB/181459e7a9c-c0193a52a226?response-content-disposition=attachment%3B%20filename%2A%3DUTF-8%27%27other_compressed_split.zip.002&response-content-type=application%2Foctet-stream&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220610T200316Z&X-Amz-SignedHeaders=host&X-Amz-Expires=7200&X-Amz-Credential=33b141c798354e21a3394e9e4f546bbe%2F20220610%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=319c711a6e5cab621d02577ad6037400d390a0bda9466ff595689c1739640b95"
wget -O other_compressed_split.zip.003 "https://olrc2.scholarsportal.info/dataverse/10.5683/SP3/LZNPKB/18145a0c6d6-73ddc70d9947?response-content-disposition=attachment%3B%20filename%2A%3DUTF-8%27%27other_compressed_split.zip.003&response-content-type=application%2Foctet-stream&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220610T200317Z&X-Amz-SignedHeaders=host&X-Amz-Expires=7200&X-Amz-Credential=33b141c798354e21a3394e9e4f546bbe%2F20220610%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=5b496dc71539acc486af9a52b8d01ff735052334cab38b542d6c226185aac960"
wget -O other_compressed_split.zip.004 "https://olrc2.scholarsportal.info/dataverse/10.5683/SP3/LZNPKB/18145a14a6b-b2471d275ed2?response-content-disposition=attachment%3B%20filename%2A%3DUTF-8%27%27other_compressed_split.zip.004&response-content-type=application%2Foctet-stream&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220610T200319Z&X-Amz-SignedHeaders=host&X-Amz-Expires=7200&X-Amz-Credential=33b141c798354e21a3394e9e4f546bbe%2F20220610%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=b5af7badcb0bdd4d12b4c0a3a4539b18d93e90108a631b8bdd051fed45756bf9"
cat other_compressed_split.zip.* > other_compressed.zip
unzip other_compressed.zip
