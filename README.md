# MSA Project Week, 2022-01-07 to 2022-01-14

### Problem
Cox communications is collecting full band capture data but is not using it to its greatest effect.

### Hypothesis
We can detect the sources for general network noise by targeting the most impaired customers based on their RAW signal.

### Datasets
**fbc.7z** - Contains 40 .csv files with Full Band Capture from devices
device_id: The device’s distinct network ID.
amplitude: array like string containing the full band capture energy. Data stored as actual_dB*100.
collection_time: when the FBC data was collected
span: total hz span of the sweep
bins: number of distinct samples in the fbc array
first: starting hz of the array
last: ending hz of the array

**device_geo_data.csv** - Device Location
mac: unique device id
geo_id: non-unique identifier for geo location of a mac address
node: geographic region in network

**network_parent_child.csv** - Network Structure
geo_id: unique identifier for geo location of a network element
Parent_id: unique identifier for geo location of a network element’s parent device
lon: longitude value of geo location
lat: latitude value of geo location
device_type: type of network object

### Objectives
1. Discover a way to cluster array like FBC strings by Node and measure precision of clustering accuracy.
2. Using secondary sources, parse the array like FBC strings for WAVE and INGRESS impairments.
3. Using the network parent to child relationships, discover a way to algorithmically find the most common ancestor of any collection of address network elements and visualize this.
4. Find a way to losslessly compress the FBC raw signal for easier access in Hive Hadoop.
