import unittest
import yaml
from odin import *

class TestGraphCreation(unittest.TestCase):
    
    def setUp(self):
        configstr = """
        odin:
          dir: /Users/noahgreen/Documents/.odin
        node:
          note:
            extensions: 
            - md
            dirs:
            - /Users/noahgreen/Documents/Notes
          reference:
            extensions: 
            - pdf
            dirs:
            - /Users/noahgreen/Documents/References
        """
        configyaml = yaml.load(configstr, Loader=yaml.FullLoader)
        
        with open('testconfig.yaml','w') as stream:
            yaml.dump(configyaml,stream)
        self.odin = Odin("testconfig.yaml")

    def test_get_node_properties(self):
        nodeattachments = ["note","reference","bibitem"]
        for name in nodeattachments:
            self.assertIn(name,self.odin.get_node_properties())

    def test_get_directories(self):
        nodeprops = self.odin.get_node_properties()
        for key in nodeprops:
            dirs = self.odin.get_directories(key)
            self.assertIsInstance(dirs,list)
            for dirname in dirs:
                self.assertTrue(os.path.isdir(dirname))

    def test_get_extensions(self):
        noteextensions = self.odin.get_extensions("note")
        print(noteextensions)
        self.assertEqual(1,len(noteextensions))
        self.assertEqual("md",noteextensions[0])

    def test_new_node(self):
        self.odin.new_node("test","this is a test",note="test.md")





if __name__ == '__main__':
    unittest.main()
