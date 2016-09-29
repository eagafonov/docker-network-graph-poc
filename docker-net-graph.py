from docker import Client

import os
import pprint
import json

from graphviz import Graph

dot = Graph(comment='Docker Network Graph',
            graph_attr=dict( rankdir="LR")
            )

docker_client = Client(os.environ.get("DOCKER_HOST", "unix:///var/run/docker.sock"))

#pprint.pprint(docker_client.networks())
def dump_json(obj):
    print json.dumps(obj, indent=4)

for net in sorted(docker_client.networks()):
    #print "Net"
    net_name = net['Name']
    
    #subnet = net['IPAM']['Config']['Subnet']
    
    #dump_json(net)

    try:
        gateway = net['IPAM']['Config'][0]['Gateway']
    except IndexError:
        gateway = None

    try:
        subnet = net['IPAM']['Config'][0]['Subnet']
    except IndexError:
        subnet = None

    print "Network: %s %s gw:%s" % ( net_name, subnet,gateway)

    net_node_id = "net_%s" % (net_name,)
    
    net_label_html = '<br/>'.join([s for s in ['net', net_name, subnet, gateway] if s != None])
    
    dot.node(net_node_id, label="<%s>" % net_label_html, shape='note')


    #pprint.pprint(net['Containers'])
    
    for container_id, container in sorted(net['Containers'].iteritems()):
        print " * ", container['Name'], container['IPv4Address'], container['IPv6Address']
        
        container_node_id = 'container_%s' % container_id
        label_html = "<font color='#777777'><i>container</i></font><br/>%s" % container['Name']

        dot.node(container_node_id,
                 label="<%s>" % label_html,
                 shape='component')
        

        label_html = "%s<br/>%s" % (container['IPv4Address'].split('/')[0], container['IPv6Address'])

        container_iface_id = "iface_%s" % container['IPv4Address']
        
        dot.node(container_iface_id,
                 label="<%s>" % label_html,
                 shape='box')

        
        
        
        dot.edge(container_node_id, container_iface_id)
        dot.edge(container_iface_id, net_node_id)
        
    print
    
print dot.source
dot.render('dng.gv')
    
