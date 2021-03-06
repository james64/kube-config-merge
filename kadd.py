
import argparse
import yaml
import sys

def empty(args):
  config = {
    'apiVersion': 'v1',
    'clusters': [],
    'contexts': [],
    'kind': 'Config',
    'preferences': {},
    'users': []
  }
  with open(args.output, 'w') as file:
    yaml.dump(config, file)


def add(args):
  # set current config if not present
  print(args)

def drop(args):
  with open(args.kube_config, 'r+') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

    config['clusters'] = [ c for c in config['clusters'] if c.name != args.cluster_name ]
    config['contexts'] = [ c for c in config['contexts'] if c.name != args.cluster_name ]
    config['users']    = [ c for c in config['users']    if c.name != args.cluster_name ]

    if config['current-context'] == args.cluster_name:
      if len(config['clusters']) == 0:
        del config['current-context']
      else:
        config['current-context'] = config['clusters'][0]['name']

    f.seek(0)
    yaml.dump(config, f)
    f.truncate()


parser = argparse.ArgumentParser(prog='kadd')
subparsers = parser.add_subparsers()

# empty
#  -o --output
parser_empty = subparsers.add_parser('empty', help='Output empty k8s config')
parser_empty.add_argument('-o', '--output', required=True, help='Output path')
parser_empty.set_defaults(func=empty)

# add
#  -c --kube-config
#  -a --add-config
#  -n --cluster-name
parser_add = subparsers.add_parser('add', help='Include config for new cluster into current one')
parser_add.add_argument('-c', '--kube-config',  help='Path to config to be edited', default='~/.kube/config')
parser_add.add_argument('-a', '--add-config', required=True, help='Path to source config. Only first cluster is used')
parser_add.add_argument('-n', '--cluster-name', required=True, help='Add new cluster under this name')
parser_add.set_defaults(func=add)

# drop
#  -c --kube-config
#  -n --cluster-name
parser_drop = subparsers.add_parser('drop', help='Drop cluster from config')
parser_drop.add_argument('-c', '--kube-config',  help='Path to config to be edited', default='~/.kube/config')
parser_drop.add_argument('-n', '--cluster-name', required=True, help='Name of a cluster to drop')
parser_drop.set_defaults(func=drop)

strArgs = ['-h'] if len(sys.argv) == 1 else sys.argv[1:]
args = parser.parse_args(strArgs)
args.func(args)

