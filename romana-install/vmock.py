#!/usr/bin/env python

from jinja2 import Template
from optparse import OptionParser
import simplejson as json
import os

parser = OptionParser(usage="%prog [options] --list | --host <machine>")
parser.add_option('--list', default=False, dest="list", action="store_true",
                  help="Produce a JSON consumable grouping of Vagrant servers for Ansible")
parser.add_option('--host', default=None, dest="host",
                  help="Generate additional host specific details for given host for Ansible")
parser.add_option('--template', default="vagrant-nodes.j2", dest="template_file",
                  help="Use non default jinja template to render hosts")
parser.add_option('--compute-num', default=1, dest="compute_num", type="int",
                  help="How many compute hosts to run")

(options, args) = parser.parse_args()

f = open(options.template_file, "r")
template = Template(f.read())

template_vars = {}
template_vars["control"] = { "id": 0, "ip": "192.168.99.10" }
template_vars["computes"] = []

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

if 'NUM_COMPUTE_NODES' in os.environ:
	cnum = int(os.environ['NUM_COMPUTE_NODES'])
else:
	cnum = options.compute_num

for i in range(cnum):
	id=i+1
	ip="192.168.99.1" + str(id)
	template_vars["computes"].append({"id": id, "ip": ip})

if options.list:
	print template.render(template_vars)

elif options.host:
	j = json.loads(template.render(template_vars))
	jb = byteify(j)
	print json.dumps(jb["_meta"]["hostvars"][options.host])
