import timeit
import json
from pandas import DataFrame
from definitions import ROOT_DIR
import re

import algorithms.clustering.discovery as discovery
from algorithms.clustering.utils import process_columns


class CorrelationClustering:
    """
    A class that contains the data and methods required for the algorithms proposed in
    "Automatic Discovery of Attributes in Relational Databases" from M. Zhang et al. [1]

    Attributes
    ----------
    quantiles: int
        the number of quantiles of the histograms
    threshold : float
        the global threshold described in [1]
    columns : list(str)
        a list with all the compound column names (table_name + '__' + column_name)

    Methods
    -------
    add_data(data, source_name, pool)
        Returns the quantile histogram of the column

    find_matches(pool)
        Returns the column name

    """
    def __init__(self, quantiles: int, threshold1: float, threshold2: float):
        """
        Parameters
        ----------
        quantiles : int
            The number of quantiles of the column's quantile histogram
        threshold : float
            The global threshold described in [1]
        """
        self.quantiles = quantiles
        self.threshold1 = threshold1
        self.threshold2 = threshold2
        self.columns = list()

    def add_data(self, data: DataFrame, source_name: str):
        """
        Processes a table into column_model_scale.Column objects and stores them as pickle files

        Parameters
        ---------
        data : pandas.Dataframe
            a table of the database
        source_name : str
            the name of the table
        pool: multiprocessing.Pool
            the process pool that will be used in the pre-processing of the table's columns
        """
        for column_name in data.columns:
            process_columns((column_name, data[column_name], source_name, data.dtypes[column_name], self.quantiles))

        self.columns = self.columns + list(map(lambda name: source_name + '__' + name, data.columns))

    def find_matches(self):
        """
        "Main" function of [1] that will calculate first the distribution clusters and then the attribute clusters

        Parameters
        ---------
        pool: multiprocessing.Pool
            the process pool that will be used in the algorithms 1, 2 and 3 of [1]
        chunk_size: int, optional
            the number of chunks of each job process (default let the framework decide)
        """
        start = timeit.default_timer()

        print("Compute distribution clusters ...\n")

        connected_components = discovery.compute_distribution_clusters(self.columns, self.threshold1, self.quantiles)

        stop = timeit.default_timer()

        print('Time: ', stop - start)

        self.write_clusters_to_json(connected_components,
                                    'Distribution_Clusters.json')

        start = timeit.default_timer()

        print("Compute attributes ... \n")
        all_attributes = list()
        for components in connected_components:
            if len(components) > 1:
                edges = discovery.compute_attributes(list(components), self.threshold2, self.quantiles)
                all_attributes.append((list(components), edges))

        print(all_attributes)

        stop = timeit.default_timer()

        print('Time: ', stop - start)

        start = timeit.default_timer()

        print("Solve linear program ... \n")
        results = list()
        for components, edges in all_attributes:
            results.append(discovery.correlation_clustering_pulp(components, edges))

        stop = timeit.default_timer()

        print('Time: ', stop - start)

        start = timeit.default_timer()

        print("Extract clusters ... \n")

        attribute_clusters = discovery.process_correlation_clustering_result(results, self.columns)

        stop = timeit.default_timer()

        print('Time: ', stop - start)

        # self.print_info(attribute_clusters)
        self.write_clusters_to_json(attribute_clusters,
                                    'Attribute_Clusters(Matches).json')

    @staticmethod
    def write_clusters_to_json(clusters: list, file_name: str):
        """
        Writes the clusters with their attributes and their connections in a json file

        Parameters
        ---------
        clusters : list(list(str))
            a list with the clusters, their attributes and their connections
        file_name : str
            the name of the JSON file to write
        """
        d = {}
        clusters.sort(key=lambda item: -len(item))
        for (cluster, idx) in zip(clusters, range(len(clusters))):
            d["Cluster " + str(idx + 1)] = list(cluster)
        with open(ROOT_DIR + "/" + file_name, 'w') as fp:
            json.dump(d, fp, indent=2)

    @staticmethod
    def print_info(clusters):
        i = 0
        for cluster in clusters:
            i = i + 1
            entries = []
            for entry in cluster:
                match_obj = re.match(r'(.*)__(.*)_(.*)', entry)
                entries.append(match_obj.group(3))
            unique_num = len(set(entries))
            total = len(entries)
            print("Cluster ", i, " number of unique ", unique_num, " out of ", total)
