import yaml
import os
import networkx as nx
from .node import *
from .edge import *


class Odin(object):
    def __init__(self,config,graph = None):
        # open graph configuration file
        configfile = os.path.abspath(config)
        if os.path.isfile(configfile):
            self._config = configfile
        else:
            raise FileNotFoundError("Config file does not exist")
        # load and validate yaml from configuration file 
        raw_yaml = None
        with open(self._config,'r') as conf:
           raw_yaml = yaml.load(conf, Loader=yaml.FullLoader)

        #TODO: make default files and directories instead of raising exceptions
        if 'odin' not in raw_yaml:
            raise RuntimeError("odin not specified in config file")
        if 'node' not in raw_yaml:
            raise RuntimeError("node not spefified in config file")

        # check to see if odin directory is valid
        raw_yaml['odin']['dir'] = os.path.abspath(raw_yaml['odin']['dir'])
        if not os.path.isdir(raw_yaml['odin']['dir']):
            raise RuntimeError("invalid odin directory")

        # check if node property directories are valid
        for key in raw_yaml['node'].keys():
            if 'dirs' in raw_yaml['node'][key].keys():
                for i in range(len(raw_yaml['node'][key]['dirs'])):
                    raw_yaml['node'][key]['dirs'][i] = os.path.abspath(raw_yaml['node'][key]['dirs'][i])
                    if not os.path.isdir(raw_yaml['node'][key]['dirs'][i]):
                        raise RuntimeError("Invalid directory for \"{}\" node property".format(key))
                
        self._node_count = 0
        self.dg = nx.DiGraph(
                loc = raw_yaml['odin']['dir'],
                node = raw_yaml['node']
                )
        self.graph = self.dg.graph

    def get_node_properties(self):
        """
        Returns a list of available node properties
        """
        return list(self.graph['node'].keys())

    def get_directories(self,key):
        """
        Returns directories where attachments for property are stored
        """
        if key not in self.get_node_properties():
            raise KeyError("key not found")
        if 'dirs' in self.graph['node'][key].keys():
            return list(self.graph['node'][key]['dirs'])
        return []

    def new_node(self,name,**kwargs):
        """
        Adds a new node to the odin graph
        """
        return None
    def get_node(self,**kwargs):
        """
        Returns node specified by kwargs
        """
        print(kwargs)
        return None

