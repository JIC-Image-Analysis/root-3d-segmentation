#!/bin/bash

# Build singularity image
docker run \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v ~/mnt/cluster_home/singularity/:/output \
    --privileged \
    -t \
    --rm \
    mcdocker2singularity \
    root-3d-segmentation-production \
    root-3d-segmentation-production

