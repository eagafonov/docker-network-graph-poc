# Docker Network Graph

Sample python script to draw graph of Docker networks and containers


## Usage
    usage: docker-net-graph.py [-h] [-v] [-o OUT]

    Generate docker network graph.
    
    optional arguments:
      -h, --help         show this help message and exit
      -v, --verbose      Verbose output
      -o OUT, --out OUT  Write output to file

In most cases what you want to run are the following couple commands:

    git clone https://github.com/LeoVerto/docker-network-graph-poc.git
    cd docker-network-graph-poc
    pipenv install
    pipenv run python docker-net-graph.py -o output.gv

This will end up generating a .pdf file containing the graph.