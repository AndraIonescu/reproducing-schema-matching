# Reproducing schema matching algorithms

The repository contains our own implementation of the algorithms presented in [1] and [2] 
and reproduced in a [master thesis](https://repository.tudelft.nl/islandora/object/uuid:9f8056e6-cfdf-4240-99e3-5f45947d1fa7?collection=education) according to the specifications indicated 
in the papers. Paper [3] is already open-sourced and a fork of the original repository is available 
[here](https://github.com/AndraIonescu/aurum-datadiscovery).

[1] [Zhang, Meihui, et al. "Automatic discovery of attributes in relational databases." Proceedings of the 2011 ACM SIGMOD International Conference on Management of data. 2011.](https://dl.acm.org/doi/pdf/10.1145/1989323.1989336?casa_token=rBsHeImB_M8AAAAA:XW3PK9oDVGKSXtuIgbLkE-R2VyE1_Ym2SOoRvx3puR2BE2kSASiPHGGs3hDWrFizLK5B6DZjkLnA)

[2] [Madhavan, Jayant, Philip A. Bernstein, and Erhard Rahm. "Generic schema matching with cupid." vldb. Vol. 1. 2001.
](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2001-58.pdf)

[3] [Fernandez, Raul Castro, et al. "Seeping semantics: Linking datasets using word embeddings for data discovery." 2018 IEEE 34th International Conference on Data Engineering (ICDE). IEEE, 2018.](http://da.qcri.org/ntang/pubs/icde2018semantic.pdf)

The repository contains the [algorithms](algorithms), [experiments](experiments) and the [data](data) used in the experiments.

## Install
> The project has been developed on MacOS Catalina and Ubuntu 19.10
#### Prerequisites 
* The algorithms require Python 3.6+ and pip
* Some packages require C++. Make sure you have it in your OS before installing the requirements.
> For Windows 10+, you should install Virtual Studio and add the C++ package from there.

> There are some more issues regarding building the packages using pip on Windows. To fix them, follow the next steps:
```
Copy these files:

rc.exe
rcdll.dll

From

C:\Program Files (x86)\Windows Kits\8.1\bin\x86 (or similar)

To

C:\Program Files (x86)\Microsoft Visual Studio 11.0\VC\bin (or similar)
```

#### Install packages
* We advise to create a virtual environment using your preferred method.

* Install the requirements:
```
pip install -r requirements.txt
```

## Run
### Clustering [1]
In the [experiments](experiments) folder, the [clustering_experiments](experiments/clustering_experiments.py) file
contains the method to run the algorithm. It needs command line arguments such as: 
* the data folder - make a folder and add the data. You can add two or more **csv files** and the algorithm will cluster all the matching columns together
* one threshold - the threshold is used to discover the cutoff value (see the paper [1] for more details). Typical values:
0.1, 0.2, 0.3
* number of quantiles - the more quantiles, the more precise the algorithm is. Typical values: 50, 100, 150, 256
* a clear cache boolean - the algorithm caches the data. Typical value _True_ 

```
python clustering_experiments.py ./data/clustering/paper 0.1 50 True
```

In the [data](data/clustering) folder, you can find the data used in the examples in the paper [1].

### Cupid [2]
In the [experiments](experiments) folder, the [cupid_experiments](experiments/cupid_experiments.py) file
contains the method to run the experiments in order to find the proper thresholds and create plots
to visualise the precision, recall and F1-score. 

An example on how to run the experiments is in [cupid_cupid_data](experiments/cupid_cupid_data.py) which uses the 
[data example](data/cupid/paper) indicated in the paper [1]. 
* Read your data in your preferred method;
* Create a "Cupid" object 
```python
cupid_model = Cupid()
```
* Add the data: schema_name, table_name, pairs of column_name, data_tye. **Note**: schema name should be different for two datasets
```python
cupid_model.add_data(schema_name1, table_name1, (column_name1, data_type1))
cupid_model.add_data(schema_name2, table_name2, (column_name2, data_type2))
```
* Next, decide on a source tree and a target tree
```python
source_tree = cupid_model.get_schema_by_index(0)
target_tree = cupid_model.get_schema_by_index(1)
```
* Indicate the output directory (for the results), the gold standard file (for computing the statistics - precision, recall, F1-score)
and two intervals for thresholds (for more details about the thresholds see [2]):
    * leaf range - typically lower than 1.0
    * accept threshold - typical value = 0.5, but you can experiment with lower values
```python
out_dir = CURRENT_DIR + '/cupid-output/'
gold_standard_file = CURRENT_DIR + '/cupid-paper-gold.txt'
leaf_range = np.arange(0.1, 1, 0.1)
th_accept_range = np.arange(0.05, 0.5, 0.02)
```
* Run experiments:
```python
run_experiments(source_tree, target_tree, cupid_model, out_dir, leaf_range, th_accept_range)
```
* If you have a gold standard file, compute the statistics - make sure you provide the matchings as tuples (see [cupid-paper-gold](experiments/cupid-paper-gold.txt)):
```python
compute_statistics(gold_standard_file, out_dir, leaf_range, th_accept_range)
```

### Seeping semantics [3]
The [seeping-semantics](algorithms/seeping-semantics) folder contains scripts to help setting up the project 
and a [README.md](algorithms/seeping-semantics/README.md) with all the necessary steps.
