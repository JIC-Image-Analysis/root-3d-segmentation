#!/bin/bash

CONTAINER=root-3d-segmentation
docker run -it --rm -v `pwd`/data:/data:ro -v `pwd`/scripts:/scripts:ro -v `pwd`/output:/output $CONTAINER
