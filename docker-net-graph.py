from docker import Client

import os
import pprint
import json

from graphviz import Graph

dot = Graph(comment='Docker Network Graph',
            graph_attr=dict( rankdir="TB", packmode='graph', pack='true')
            )

docker_client = Client(os.environ.get("DOCKER_HOST", "unix:///var/run/docker.sock"))

def dump_json(obj):
    print(json.dumps(obj, indent=4))

for c in sorted(docker_client.containers()):
    name = c['Names'][0]
    container_id = c['Id']
    
    node_id = 'container_%s' % container_id
    
    iface_labels = []
    
    for net_name, net_info in c['NetworkSettings']['Networks'].items():
        label_iface = "<%s> %s" % (net_info['EndpointID'], net_info['IPAddress'])
        
        iface_labels.append(label_iface)
        
    print('|'.join(iface_labels))
        
    
    dot.node(node_id,
             shape='record',
             label="{ %s | { %s } }" % (name, '|'.join(iface_labels)),
             fillcolor='#ff9999',
             style='filled')
    
    

for net in docker_client.networks():
    net_name = net['Name']
    
    try:
        gateway = net['IPAM']['Config'][0]['Gateway']
    except IndexError:
        gateway = None

    try:
        subnet = net['IPAM']['Config'][0]['Subnet']
    except IndexError:
        subnet = None

    print("Network: %s %s gw:%s" % ( net_name, subnet,gateway))

    net_node_id = "net_%s" % (net_name,)
    
    net_label_html = '<br/>'.join([s for s in ['<font color="#777777"><i>network</i></font>', net_name, subnet, gateway] if s != None])
    
    dot.node(net_node_id, 
             shape='record',
             label="{<gw_iface> %s| %s }" % (gateway, net_name),
             fillcolor='#99ff99',
             style='filled')


    for container_id, container in sorted(net['Containers'].items()):
        dump_json(container)
        print(" * ", container['Name'], container['IPv4Address'], container['IPv6Address'])
        
        container_node_id = 'container_%s' % container_id
        
        container_iface_ref = "%s:%s" % (container_node_id, container['EndpointID'])
        
        dot.edge(container_iface_ref, net_node_id+":gw_iface")
    
print(dot.source)
dot.render('dng.gv')
    
