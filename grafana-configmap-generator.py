#!/usr/bin/env python

import ruamel.yaml
import argparse

parser = argparse.ArgumentParser(description='Grafana Dashboard JSON to Kubernetes configmap YAML converter.')
parser.add_argument('--namespace', '-n', default='monitoring', help='Namespace to deploy configmap into.')
parser.add_argument('dashboard', metavar='grafana-dashboard.json', help='Exported Grafana Dashboard json file.')

args = parser.parse_args()

namespace = args.namespace
dashboardjsonfile = args.dashboard

literal = ruamel.yaml.scalarstring.LiteralScalarString

yaml = ruamel.yaml.YAML()

with open(dashboardjsonfile, 'r') as inputfile:

    inputfilename = inputfile.name
    dashboardname = inputfilename.strip(('.json'))
    outputfilename = dashboardname + '.yaml'
    yaml_str = {
        'apiVersion': 'v1',
        'data':{inputfilename: literal(inputfile.read())},
        'kind': 'ConfigMap',
        'metadata':{'labels':{'grafana_dashboard': 'true'},
                    'name': dashboardname,
                    'namespace': namespace
                    }
    }
    with open(outputfilename, 'w') as outputfile:
        dashboard_yaml = yaml.dump(yaml_str, outputfile)