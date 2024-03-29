# Lever for Change Proposal Landscape

An interactive visualization of Lever for Change's proposal landscape built on the Ploty Dash framework.  

More information on: [Dash](https://dash.plotly.com/introduction), [Plotly](https://plotly.com/python/)

## Instructions

Initialize a virtual environment with `python -m venv venv`, and activate it.

Install dependencies: `pip install -r requirements.txt`.

In `app/const.py` change `sferg` in the expression `if 'sferg' in os.path.expanduser('~'):` to a value that will match the username on your local machine. This will ensure that the datasets are loaded from the local file system and not from the S3 bucket.

Start the app: `python index.py`

If you haven't prepared the UMAP model, follow the directions [here](https://github.com/sfergusond/lfc-model-pipeline#readme). Note that by default, the app expects a PREFIX of `LANDSCAPE_APP_`. You should change this in `const.py` or ensure your UMAP output is configured to use that as the prefix. Also note that the CSV filename defaults to `Proposal_Similarity_DataFrame.csv`. Ensure that your `output_file_name` parameter is set to that for the pipeline.

View the app at `localhost:8050`

## File Structure

### `assets/`

Contains the app static files and the global CSS variables.

### `app/`

Contains the set of files responsible for powering the application, the one exception being `index.py` which is the app entry point and contains basic definitions for the application, including listing the callbacks responsible for managing user interaction.  

Since Dash is written in pure Python, there is no HTML code in the repo. As such, all "HTML" files are under `app/layout/`.  

Instead of querying a database, the dataset, UMAP embeddings, and neighbor matrix are housed in the `const.py` file as `df`, `embeddings`, and `knn_indices` respectively. 
These global variables can be imported from anywhere in the app, making the various callback and plotting functions easier to read. See below for specifications for this data.

## Data Specifications

__Important__: When regenerating new files, they must be named exactly as described below. The same holds for files stored in S3, where the web app pulls from. When using the similarity pipeline, ensure to update the `model_tag` argument to `LANDSCAPE_APP` and the `output_file_name` to `Proposal_Similarity_DataFrame.csv`.

### Proposal Dataframe

Pandas DataFrame of cleaned proposal data stored in `consts.py` as `df` and in `data/` as `lfc-proposals-clean.csv`. 

Note that the `Application #` column is not the index corresponding to the proposal in the loaded dataframe, the index is a different value internally generated by pandas.

The topic model module adds two columns to the cleaned dataset: `Topic` and `Outlier Score`. `Topic` is a numeric variable corresponsing to the index of the topic specified in `topics.pkl`. `Outlier Score` is a numeric variable denoting how closely the observation is associated to its assigned topic. Higher values mean that the observation is more loosely associated with its cluster, and is therefore more of a unique/outlier observation.

### UMAP Embeddings

An embedding matrix with coordinates for each proposal on each dimension in _[1, components]_. Stored in `consts.py` as `embeddings` and in `data/` as `embeddings.pkl`.

With the default number of components (3), the matrix simply becomes a list of x, y, z coordinates. The web app will need minor tweaks to support 2D coordinate pairs or certain subsets of higher-dimensional data.

```
[
  (3.2345, 1.009, 0.13677),
  (6.32454, 2.083, 1.562),
  ...,
  (4.09092, 3.0004, 0.158)
]
```

### KNN Indices Matrix

Stored in `consts.py` as `knn_indices` and in `data/` as `knn_indices.pkl`.

For each element in the KNN Indices Matrix, the index of the element corresponds to a proposal at index `i` in the Proposal Dataframe. Each element contains a list of indices, which represent neighbors of that proposal. A proposal may have no neighbors (empty list).

For example:

```
[
  [0, 10, 15],
  [],
  ...,
  [5000]
]
```

These indices might evaluate to something like (made up names):

```
[
  [Health Equity in Chicago, Building a Hospital in Indiana, Advocacy for Children of Cancer Patients],
  [],
  ...,
  [Investing in Guatemalan Science Education]
]
```

### Topic Model Data

Stored in `consts.py` as `topics` and in `data/` as `topics.pkl`.

This is a dictionary of `cluster_label -> topic_information` mappings. The first key is always `-1`, which corresponds to the "non-cluster" entry and therefore does not have an `exemplar` entry. All other entries have a set of `words` and a 3D `exemplar` coordinate, denoting the coordinates of the point which represents the best center of the cluster.

```
{
  -1: {
    'words': ['social', 'economic', 'work', 'education', 'poverty']
  },
  0: {
    'words': ['news', 'newsroom', 'medium', 'journalism', 'journalist'], 
    'exemplar': (7.306426048278809, -0.29259100556373596, -2.392807960510254)
  }
}
```

The keys in the topics dictionary map to the `Topic` column in the Proposal Dataframe.