# Big_Data_Processing_Labs 

### Lab1:
The goal of this laboratory work is to develop skills in dataset analysis and processing by performing feature selection, handling outliers and missing values, and visualizing data. Additionally, you will implement the K-Nearest Neighbors (KNN) algorithm to make predictions and evaluate model performance using given datasets. This work aims to enhance your ability to manage and analyze large datasets effectively and apply machine learning techniques.

***Task 1.*** Perform dataset analysis (define types of features, prepare a data quality report). For further analysis, choose a subset of features (>8) from categorical (at least 2) and continuous variables (at least 2). Feature selection (or rejection) must have a logical basis following directly from the logical problem of the task or data quality report.

***Task 2.*** Perform data processing: handle outliers and missing values (use the methodology provided in Individual_problems_LD1.xlsx for handling missing values). Visualize the dependencies between features using at least 3 different visualization methods.

***Task 3.*** Implement the KNN algorithm and make predictions for the feature specified in Individual_problems_LD1.xlsx. Provide results when predicting based on "train_*.csv" data for "test_*.csv" data.

### Grading Criteria:
##### Feature Identification and Data Quality Report

Correctly identifies and categorizes all features in the dataset as either categorical or continuous. Provides a clear and detailed data quality report, including information on missing values, cardinality, statistical indicators.

##### Feature Selection with Logical Basis

Chooses an appropriate subset of features, including at least 2 categorical and 2 continuous variables. Provides a logical and well-justified basis for feature selection or rejection, directly related to the task's problem or the data quality report.

##### Handling Outliers and Missing Values

Correctly identifies and handles outliers in the dataset. Properly addresses missing values according to the methodology provided in Table 1.

##### Visualization of Feature Dependencies

Uses at least 3 different visualization methods to represent feature dependencies. The visualizations are clear, well-labeled, and provide meaningful insights into the relationships between features.

##### KNN Algorithm Implementation

Correctly implements the KNN algorithm to predict the target feature specified in table 1.

##### Results
Provides well-formatted analysis of KNN performance (including accuracy and other potential issues) on prediction results for "test_.csv" data using the "train_.csv" data as training data.

### Lab2 (merged with Lab3):
Data collection, processing and grouping

***Task 1.*** automatically collect information about the places of interest of the specified cities (see individual task). There have to be at least 200 objects for each city (you can extend search radius to municipality if there are no enough objects founds) . The collected data must be sufficiently large to be able to form dataset with at least 10 features for each place. Use Wiki and optionally OpenStreetMap for data collection.

***Task 2.*** Save all collected into database (choice one: SQLite, PostgreSQL, DuckDB). "All" means - raw response data, intermediate data(if applicable) and final features.  

***Task 3.*** process collected data about places and extract features for further analysis. Compare data sizes before and after processing and structurization. Provide data quality report, other analysis if needed.

***Task 4.*** group collected places (use K-means), and implement code, which allows for selected place provide N other places from its group at other cities (use KNN inside specific cluster to find N). Algorithms (KNN, K-means) must be implemented from scratch (libraries implementing them should not be used - for example using scipy.cluster.vq.kmeans not allowed ).

***Task 5.*** provide assumptions, API led approach, shorthand specification and return data example for provided user story:

User Story: As a food delivery driver, I want to:

* Get today’s delivery orders on my smartphone
* Get delivery orders for a specific day on a web browser, where available options are: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday
* Get detailed information about each order, including customer address, meal details, and estimated delivery time
* The data should be returned as a JSON object 

Python language is preferred, pandas package is not allowed, the data analysis cannot be automatic visualization from library 

note: during collection it is recommended implement rate limiting and exponential back-off, SQLite and DuckDB are single writer databases - if it used in multi-threading environment it is to create independent databases and after finishing merge them

### Grading Criteria:
##### Data Collection

Collects data on at least t 800 places (total from all cities) of interest for each specified city, ensuring comprehensive coverage. Uses both Wiki and optionally OpenStreetMap, demonstrating effective use of these sources for data collection.

##### Data storage:

Effectively processes and saves collected data into database (Sqlite, Postgresql, duckdb or similar). There are no strict requirement for table format - it need to be enough data to allow recalculate all tasks using database.

##### Feature Completeness:

The collected dataset includes at least 10 features for each place, providing detailed information. Data is formatted appropriately.

##### Data Quality Report and Analysis:

Provides a comprehensive data quality report and additional analysis if needed.

##### K-means Clustering Implementation and KNN:

Correctly implements the K-means clustering algorithm to group collected places. Provides a clear explanation of the clustering approach and results. Provides example program look up objects using KNN

##### User Story: As a food delivery driver:
Provides user story for:

* Get today’s delivery orders on my smartphone

* Get delivery orders for a specific day on a web browser, where available options are: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday

* Get detailed information about each order, including customer address, meal details, and estimated delivery time

* The data should be returned as a JSON object



### Lab3 part:
Data collection, processing and grouping

***Task 1.*** Automatically process already collected (or collected) information about the places of interest of the specified cities (see individual task in LD2, include relevance score for each object) using MPI collective communication (main source: wiki). 

***Task 2.*** Store data in SQLite/PostgreSQL/DuckDB (create schema and tables). 

***Task 3.*** Create connection graph between objects (use  classifiers, words in wiki article, semantic meaning etc., avoid using internal urls). 

***Task 4.*** Implement distributed PageRank algorithm using MPI collective communication, calculate page rank value for collected data and compare it to wiki relevance score.


note1: If all tasks with collective communication are implemented only using bcast and barrier - points will not be given.

note2: tasks implementations must not rely on send, recv methods.

note3: how graph it is connected is up to you and it can be directional. For example in object 1 wiki article have mentional word "blue", it will be connected with other 10 objects (chosen by distance) which have word "red".  

### Grading Criteria:
##### Task 1.
Python project calling independent script which with help of MPI, perform preprocessing (or downloading) wiki/osm data items and have ready to use parallel computing function. This task is linked with Task no. 2

##### Task 2.
Stores all necessary initial data for processing in SQL type database

##### Task 3.
Using data collected from Task 1&2 creates connection graph and stores somewhere (can be to file using pickle or database). Strongly recommended using mpi for calculating graph connections.

##### Task 4.
* Implemented parallel pagerank using MPI

* One script to calculate page rank and save results to Database for query (enough to have table with to columns: title/description, pr)

* Second script to perform query from created database.



### Lab4:
The goal of these tasks is to develop expertise in automated image collection, color analysis, and similarity-based search in image datasets. You will collect and manage image data related to places of interest, analyze the dominant colors in these images using clustering techniques, and implement a similarity search algorithm to find similar places based on color features. These tasks aim to enhance your skills in image processing, feature extraction, and similarity-based data retrieval.

Image Based Data Comparison

***Task 1.*** Automatically collect images about the places of interest of the specified cities (see individual task from  Lab 2 & Lab 3). There must be at least 1000 objects with images for each city. (3 points).

***Task 2.*** Apply K-means algorithm for extraction of dominant colors. Sort the clusters based on the number of assigned points in decreasing order. (Format feature vector of Kx3 numerical values, here 1-3 positions represent the centroid of largest cluster (RGB), the last 3 positions represent the centroid of smallest cluster (RGB)). (4 points).

***Task 3.*** Apply similar places search by formatted vectors (task 2) using KNN. (3 points).

### Grading Criteria:
##### Data Collection
Collects at least 1000 images for each specified city, ensuring a diverse and representative dataset. Images are appropriately labeled or associated with their respective places of interest.

##### K-means Clustering Implementation
Successfully applies the K-means algorithm to extract dominant colors from the images including the formatting of the feature vector with Kx3 numerical values, representing the centroids from largest to the smallest clusters (RGB values).

##### KNN Implementation for Similar Places
Correctly implements the K-Nearest Neighbors (KNN) algorithm to search for similar places based on the color feature vectors. The KNN implementation is efficient and correctly configured.
