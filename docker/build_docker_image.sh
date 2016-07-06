!#/bin/bash

IMAGE_NAME=root-3d-segmentation

cp ../requirements.txt $IMAGE_NAME
cd $IMAGE_NAME
docker build -t $IMAGE_NAME .
cd ../
