#!/bin/bash

IMAGE_NAME=root-3d-segmentation

cp ../requirements.txt $IMAGE_NAME
cd $IMAGE_NAME
docker build --no-cache -t $IMAGE_NAME .
rm requirements.txt
cd ../
