# Mage Generators & Solves

## Project Overview

The goal of the project is to implement a variety of maze generating and solving algorithms.

The following generating algorithms are implemented:
- Aldous-Broder algorithm
- Randomized depth-first search
- Iterative randomized Kruskal's algorithm
- Iterative randomized Prim's algorithm
- Recursive division
- Wilson's algorithm

The following solving algorithms are implemented:
- Bredth-first search
- A* (allowing to choose a variety of supporting data structures and with the possibility to fallback to Dijkstra)
- 

## Repository Structure

This directory contains the following files and directories:

* [**generate.py**](generate.py): Main Python script used to generate a maze using a given algorithm.
* [**solve.py**](solve.py): Main Python script used to solve a maze using a given algorithm.
* [**generators**](generators): Directory collecting all implementations of maze generating algorithms.
* [**solvers**](solvers): Directory collecting all implementations of maze solving algorithms.
* [**examples**](examples): Directory containing examples of generated and solved mazes as images.
* [**environment.yml**](environment.yml): YAML file describing the conda environment needed to run the scripts.
* [**README.md**](README.md): The Readme file you are currently reading.


## Getting Started

### 0) Python Environment

An environment containing the required packages with compatible versions can be created as follows:

```bash
conda env create -f environment.yml
conda activate mazes
```


### 1) Run

To generate a new maze, run:

```bash
python generate.py -a ALGORITHM
```

where `ALGORITHM` can be any of: `random_depth_first_search`, `random_kruskal`, `random_prim`, `wilson`, `aldous_broder`, `recursive_division`.

To solve a maze, run:

```bash
python solve.py -a ALGORITHM
```

where `ALGORITHM` can be any of: `a_star`, `a_star_linked_list`, `a_star_binary_heap`, `a_star_bucket_queue`, `dijkstra`, `dijkstra_linked_list`, `dijkstra_binary_heap`, `dijkstra_bucket_queue`, `breadth_first_search`.

Both scripts support additional parameters which can be seen running them with `-h`.