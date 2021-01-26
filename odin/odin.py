import yaml
import os
import shutil
import networkx as nx


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
    def get_extensions(self,key):
        """
        Returns valid file extensions associated with key
        """
        if key not in self.get_node_properties():
            raise KeyError("key not found")
        if 'extensions' in self.graph['node'][key].keys():
            return list(self.graph['node'][key]['extensions'])
        return []

    def _check_property_key(self,key):
        """
        Ensures that key belongs to a valid graph property
        """
        key = str(key)
        if key not in self.get_node_properties():
            raise RuntimeError("Invalid property key")

    def _check_property(self,**kwargs):
        """
        Checks property=value pair against format in configuration file
        """
        print(kwargs)
        if len(kwargs) != 1:
            raise RuntimeError("Invalid number of arguments")
        key = list(kwargs.keys())[0]
        self._check_property_key(key)
        val = os.path.abspath(kwargs[key])
        if not os.path.isfile(val):
            raise FileNotFoundError
        filename, extension = os.path.splitext(val)
        if extension not in self.get_extensions(key):
            raise RuntimeError("Invalid file extension")
        return key,val

    def new_node(self,name=None,description=None,**kwargs):
        """
        Adds a new node to the odin graph
        """
        if name is None and description is None and len(kwargs) == 0:
            return None
        

        nodedict = dict()
        print(kwargs)
        
        if len(kwargs) != 0:
            # check property format and get key/value pair
            key,filename= self._check_property(**kwargs)
        
            # get directory where file lives
            dirname = os.path.dirname(filename)
            
            # get base file.ext name
            basename = os.path.basename(filename)

            # copy file to default directory if dirname is not in config file
            if dirname not in self.get_directories(key):
                defaultdir = self.get_directories(key)[0]
                newfilename = os.path.join(defaultdir,basename)
                shutil.copy2(filename,newfilename)
                filename = newfilename

            # add object to node dictionary
            nodedict[key] = filename

            # set name to base filename if no name is given
            if name is None:
                # get base filename 
                name, = os.path.splitext(basename)

        if name is not None:
            propdict['name'] = str(name)

        if description is not None:
            propdict['description'] = str(description)

        # add the node to odin's tree
        self.dg.add_node(self._node_count+1,**propdict)
        self._node_count += 1



        print(kwargs)
        print("New node!")
        return None
    def get_node(self,**kwargs):
        """
        Returns node specified by kwargs
        """
        print(kwargs)
        return None

