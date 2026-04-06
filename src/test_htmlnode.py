import unittest
from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

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

class TestLeafNode(unittest.TestCase):
    def test_basic_tag(self):
        node = LeafNode("p", "Hello")
        self.assertEqual(node.to_html(), "<p>Hello</p>")

    def test_no_tag(self):
        node = LeafNode(None, "Hello")
        self.assertEqual(node.to_html(), "Hello")

    def test_with_props(self):
        node = LeafNode("a", "Click", {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">Click</a>')

    def test_multiple_props(self):
        node = LeafNode("a", "Click", {"href": "https://boot.dev","target": "_blank"})
        result = node.to_html()
        self.assertIn('href="https://boot.dev"', result)
        self.assertIn('target="_blank"', result)

    def test_no_value_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr(self):
        node = LeafNode("p", "Hello", None)
        self.assertEqual(repr(node), "LeafNode(p, Hello, None)")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

if __name__ == "__main__":
    unittest.main()
