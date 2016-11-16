# README

Scripts to segment roots and calculate intensities per cell.

For information about the methods see the [methodology](methodology.md).

## Installation notes

This image analysis project has been setup to take advantage of a technology
known as Docker.

This means that you will need to:

1. Download and install the [Docker Toolbox](https://www.docker.com/products/docker-toolbox)
2. Build a docker image

Before you can run the image analysis in a docker container.


## Build a Docker image

Before you can run your analysis you need to build your docker image.  Once you
have built the docker image you should not need to do this step again.

A docker image is basically a binary blob that contains all the dependencies
required for the analysis scripts. In other words the docker image has got no
relation to the types of images that we want to analyse, it is simply a
technology that we use to make it easier to run the analysis scripts.

```
$ cd docker
$ bash build_docker_image.sh
$ cd ..
```

## Run the image analysis in a Docker container

The image analysis will be run in a Docker container.  The script
``run_docker_container.sh`` will drop you into an interactive Docker session.

```
$ bash run_docker_container.sh
[root@048bd4bd961c /]#
```

Now you can run the image analysis on a series within a microscopy file.  The
below analyses series ``0`` in ``data/raw.lif`` and writes the output to
``output``.

```
[root@048bd4bd961c /]# python scripts/analyse_series.py data/raw.lif 0 output/
```

## Mass processing of data

We need to create a bash script for mass processing.
If running outside of a docker container using a virtual environment
setup we need to add a line sourcing it.

```
echo "source env/bin/activate" > mass_process.sh
```

We can then append all the jobs to the newly created ``mass_process.sh``
script.

```
$ python scripts/mass_process.py input_dir ouput_dir bash-script >> mass_process.sh
```

Finally, we can run the mass processing bash script.

```
$ bash mass_process.sh
```

## Generating histogram from all data

Create master csv file.

```
$ python scripts/cat_csv_files.py output_dir > data.csv
```

Create faceted histogram.

```
$ Rscript scritps/all_histograms.R data.csv histograms.png
```
