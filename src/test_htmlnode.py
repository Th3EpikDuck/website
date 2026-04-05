import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://boot.dev", "target": "_blank"})
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://boot.dev" target="_blank"')

    def test_props_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("a", "click", None, {"href": "link"})
        self.assertEqual(repr(node), "HTMLNode(a, click, None, {'href': 'link'})")

    def test_values(self):
        node = HTMLNode("p", "hello")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "hello")

    def test_children(self):
        child = HTMLNode("span", "hi")
        parent = HTMLNode("div", children=[child])
        self.assertEqual(parent.children[0], child)

if __name__ == "__main__":
    unittest.main()
