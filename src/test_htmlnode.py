import unittest
from htmlnode import HTMLNode


class Test_HTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("p", "hello")
        node2 = HTMLNode("p", "hello")
        
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = HTMLNode("p", "hello")
        node2 = HTMLNode("div", "hello")
        
        self.assertNotEqual(node1,node2)

if __name__ == "__main__":
    unittest.main()