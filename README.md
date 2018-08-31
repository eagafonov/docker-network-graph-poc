# Docker Network Graph

Visualize the relationship between Docker networks and containers
as a neat graphviz graph.


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

## Running inside docker
If you want to generate a graph for a remote system you can also easily
run this script inside a pre-built docker container:
    
    docker run -v /var/run/docker.sock:/var/run/docker.sock leoverto/docker-network-graph

This will just generate and output the graph. You can then run
`fdp -Tpdf -o out.pdf`or `fdp -Tpng -o out.png` on a system with
graphviz installed, paste the previous output there, press enter
and finally CTRL+C to generate the file.