#!/usr/bin/python3
import os
import json
import argparse
import random
from docker import Client
from graphviz import Graph

# colorlover.scales["12"]["qual"]["Paired"] converted to hex strings
COLORS = ['#1f78b4', '#33a02c', '#e31a1c', '#ff7f00', '#6a3d9a', '#b15928', '#a6cee3', '#b2df8a', '#fb9a99', '#fdbf6f',
          '#cab2d6', '#ffff99']
i = 0


def get_unique_color():
    global i

    if i < len(COLORS):
        c = COLORS[i]
        i += 1
    else:
        c = "#%06x".format(random.randint(0, 0xFFFFFF))
    return c


def generate_graph(verbose: bool, file: str):
    g = Graph(comment='Docker Network Graph', engine="fdp", format='png',
              graph_attr=dict(packed="true", splines="true"))

    docker_client = Client(os.environ.get("DOCKER_HOST", "unix:///var/run/docker.sock"))

    def dump_json(obj):
        print(json.dumps(obj, indent=4))

    for c in docker_client.containers():
        name = c['Names'][0]
        container_id = c['Id']

        node_id = 'container_%s' % container_id

        iface_labels = []

        for net_name, net_info in c['NetworkSettings']['Networks'].items():
            label_iface = "<%s> %s" % (net_info['EndpointID'], net_info['IPAddress'])

            iface_labels.append(label_iface)

        if verbose:
            print('|'.join(iface_labels))

        g.node(node_id,
               shape='record',
               label="{ %s | { %s } }" % (name, '|'.join(iface_labels)),
               fillcolor='#ff9999',
               style='filled')

    i = 0
    for net in docker_client.networks():
        net_name = net['Name']
        color = get_unique_color()

        try:
            gateway = net['IPAM']['Config'][0]['Gateway']
        except IndexError:
            gateway = None

        try:
            subnet = net['IPAM']['Config'][0]['Subnet']
        except IndexError:
            subnet = None

        if verbose:
            print("Network: %s %s gw:%s" % (net_name, subnet, gateway))

        net_node_id = "net_%s" % (net_name,)

        net_label_html = '<br/>'.join([s for s in ['<font color="#777777"><i>network</i></font>', net_name, subnet, gateway] if s is not None])

        g.node(net_node_id,
               shape='record',
               label="{<gw_iface> %s| %s }" % (gateway, net_name),
               fillcolor=color,
               style='filled')

        for container_id, container in sorted(net['Containers'].items()):
            if verbose:
                dump_json(container)
            if verbose:
                print(" * ", container['Name'], container['IPv4Address'], container['IPv6Address'])

            container_node_id = 'container_%s' % container_id

            container_iface_ref = "%s:%s" % (container_node_id, container['EndpointID'])

            g.edge(container_iface_ref, net_node_id+":gw_iface", color=color)

    print(g.source)
    if file:
        g.render(file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate docker network graph.")
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    parser.add_argument("-o", "--out", help="Write output to file", type=str)
    args = parser.parse_args()

    generate_graph(args.verbose, args.out)
