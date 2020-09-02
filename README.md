# Overview
This repository contains Python scripts for allele-specific mapping. They were used
to map ATAC-seq, RNA-seq and Hi-C reads in a mouse hybrid cell line to
study the reactivation kinetics of the X chromosome during iPS cell reprogramming.
However, the scripts are general and they can be used for other purposes.

# System Requirements
## Hardware requirements
The code requires only a standard computer with enough RAM to support the in-memory operations.

## Software requirements
### OS Requirements
This code is supported for *Linux*. The package has been tested on the following systems:
+ Linux: Ubuntu 14.04.6
+ Scientific Linux 7.2

### Python
The code is written for Python 2.7 or 3.7 and does not depend on additional packages.

# Installation Guide:

### Install from Github
```
git clone https://github.com/gui11aume/asmap
```
Downloading the files is sufficient and there is no further requirement to install the
software.

# Demo
To run the demo, set the current directory to `asmap/demo`. Assuming that you just downloaded
the repository from Github, run:
```
cd asmap/demo
```

Then you need to run the script `merge_assign.py` on the two SAM files of dummy ATAC-seq reads
mapped in Mus musculus castaneus and in Mus musculus musculus, and on the p2f files that
contain the information to lift over the coordinates from the genomes of castaneus and musculus
to the mouse reference genome (mm10). You can do this with the following command:
```
python ../merge_assign.py mapped_in_cas.sam mapped_in_mus.sam p2f/* > disambiguated_no_header.sam
```

The running time should be less than 1 minute. The command creates a SAM file without header where
the reads are assigned to one genome or the other. The chromosomes now have the suffix `.ref` and
the coordinates are expressed in the reference genome (mm10).

Every line of the SAM file contains an additional field labelled `ZZ:Z:` that
contains the final call for every read. The values in this demo are `chrX.cas` if the read is
assigned to the castaneus genome; `chrX.mus` if it is assigned to the musculus genome; `amb` if
there is an ambiguity between two unique sites of the castaneus and musculus genome; and `rep`
if there is an ambiguity between several repeated sites of each genome.

# Instructions for use
To run the software on your data, you must first map the reads of interest with
[BWA MEM](https://github.com/lh3/bwa) (an example Makefile is provided). The reads must be mapped
separately in both genomes of interest. It is important that the chromosomes in the two genomes
have the same name with different suffixes (e.g., `chrX.cas` and `chrX.mus`).

The reads can be disambiguated using the same command as in the demo. If p2f files are provided,
the coordonates will be shifted to the corresponding reference. Othewise, they will be set as
`nan`.


# License

This project is the public domain.
