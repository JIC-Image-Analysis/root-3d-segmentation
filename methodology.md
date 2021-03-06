# Methodology

## Overview

Root images were analysed to generate mean FLC-Venus intensities per cell using
a custom image processing pipeline written in the Python programming language
(1), using the jicbioimage (2), Bio-Formats (3) and SimpleITK (4) libraries.
Full source code for the pipeline is available at
https://github.com/JIC-Image-Analysis/root-3d-segmentation.

The pipeline consisted of four stages: generating three dimensional (3D) masks
of the cell volume, segmenting the area within the mask into individual cells,
filtering the resulting segmentation and then using this segmentation to
compute mean FLC-Venus intensities per cell.

## Mask generation

A 3D root mask was generated by firstly applying Otsu thresholding to the
propidium iodide (cell wall) channel of the image. A binary opening filter was
applied to remove small objects from the thresholded image, and then the convex
hull of the result yielded the mask.

## Image segmentation

Image segmentation was separately performed on the cell wall channel. To
preprocess the image, a median smoothing filter was applied (radius 1 voxel),
the gradient magnitude of the resultant image was calculated and a discrete
Gaussian filter (radius 2 voxels) applied to the result. This image was then
segmented with the morphological watershed function provided by the SimpleITK
library. SimpleITK's watershed algorithm provides an option to dynamically
filter the minima used as seeds to reduce over segmentation (5). The level
for this option was set to 0.644.

## Cell filtering

The resulting segmentation was filtered by firstly removing any segmented
regions outside the mask and any touching the edges of the image. Then very
small (<10000 voxels) and large (>80000 voxels) segmented regions were removed.

## Intensity measurements

The segmented cells were used to determine the mean FLC-Venus intensity by
summing voxel intensities from the FLC-Venus channel within a mask defined by
the segmentation, and dividing by the total cell volume in voxels. These
per-cell mean intensities were used to generate histograms using the R
statistical computing environment (6).

## References

1. Python Software Foundation. Python Language Reference, version 2.7.
   Available at http://www.python.org
2. Olsson TSG, Hartley M. (2016) jicbioimage: a tool for automated and
   reproducible bioimage analysis. PeerJ 4:e2674
   https://doi.org/10.7717/peerj.2674
3. Linkert M, Rueden CT, Allan C, Burel J-M, Moore W, Patterson A, Loranger B,
   Moore J, Neves C, Macdonald D, Tarkowska A, Sticco C, Hill E, Rossner M,
   Eliceiri KW, Swedlow JR. 2010. Metadata matters: access to image data in the
   real world. Journal of Cell Biology 189(5):777-782
   https://doi.org/10.1083/jcb.201004104
4. Lowekamp BC, Chen DT, Ibáñez L, Blezek D. 2013. The design of simpleITK.
   Frontiers in Neuroinformatics 7:45
   http://doi.org/10.3389/fninf.2013.00045
5. Beare R, Lehmann G. (2006) The watershed transform in ITK - discussion and
   new developments.
   The Insight Journal
   http://hdl.handle.net/1926/202
6. R Development Core Team. 2016. R: a language and environment for statistical
   computing. Vienna: R Foundation for Statistical Computing.
   https://www.R-project.org
