import unittest
import yaml
from ..odin import *

class TestGraphCreation(unittest.TestCast):
    
    def setUp(self):
        configstr = """
        odin:
          dir: /Users/noahgreen/Documents/.odin
        node:
          note:
            types: 
            - md
            dirs:
            - /Users/noahgreen/Documents/Notes
          reference:
            types: pdf
            dirs:
            - /Users/noahgreen/Documents/References
        """
        configyaml = yaml.load(configstr)
        
        with file('testconfig.yaml','w') as stream:
            yaml.dump(configyaml,stream)

        self.odin = Odin("testconfig.yaml")

    def test_get_node_properties(self):
        nodeattachments = ["note","reference"]

