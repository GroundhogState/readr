#!/usr/bin/env bash

conda install -c conda-forge jupyter_contrib_nbextensions ase
conda install memory_profiler

jupyter nbextension enable collapsible_headings/main
jupyter nbextension enable toc2/main
