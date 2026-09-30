import unittest
from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_initialization(self):
        node = HTMLNode(tag="div", value="Hello", children=[], props={"class": "my-class"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "my-class"})

    def test_props_to_html_with_props(self):
        node = HTMLNode(tag="div", props={"class": "my-class", "id": "my-id"})
        expected_html = ' class="my-class" id="my-id"'
        self.assertEqual(node.props_to_html(), expected_html)

    def test_props_to_html_without_props(self):
        node = HTMLNode(tag="div")
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode(tag="span", value="Text", children=[], props={"style": "color:red;"})
        expected_repr = "HTMLNode(tag=span, value=Text, children=[], props={'style': 'color:red;'})"
        self.assertEqual(repr(node), expected_repr)

class TestLeafNode(unittest.TestCase):
    def test_initialization(self):
        leaf = LeafNode(tag="p", value="Paragraph", props={"class": "text"})
        self.assertEqual(leaf.tag, "p")
        self.assertEqual(leaf.value, "Paragraph")
        self.assertEqual(leaf.props, {"class": "text"})

    def test_to_leafnode_with_tag_and_value(self):
        leaf = LeafNode(tag="p", value="Paragraph", props={"class": "text"})
        expected_html = '<p class="text">Paragraph</p>'
        self.assertEqual(leaf.to_html(), expected_html)

    def test_to_leafnode_without_tag(self):
        leaf = LeafNode(tag=None, value="Just text", props={"class": "text"})
        expected_html = 'Just text'
        self.assertEqual(leaf.to_html(), expected_html)

    def test_to_leafnode_without_value(self):
        leaf = LeafNode(tag="p", value=None, props={"class": "text"})
        with self.assertRaises(ValueError):
            leaf.to_html()

    def test_to_leafnode_without_props(self):
        leaf = LeafNode(tag="p", value="Paragraph", props=None)
        expected_html = '<p>Paragraph</p>'
        self.assertEqual(leaf.to_html(), expected_html)

class TestParentNode(unittest.TestCase):
    def test_initialization(self):
        child1 = LeafNode(tag="span", value="Child 1")
        child2 = LeafNode(tag="span", value="Child 2")
        parent = ParentNode(tag="div", children=[child1, child2], props={"class": "container"})
        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, [child1, child2])
        self.assertEqual(parent.props, {"class": "container"})

    def test_to_parentnode_with_tag_and_children(self):
        child1 = LeafNode(tag="span", value="Child 1")
        child2 = LeafNode(tag="span", value="Child 2")
        parent = ParentNode(tag="div", children=[child1, child2], props={"class": "container"})
        expected_html = '<div class="container"><span>Child 1</span><span>Child 2</span></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_to_parentnode_without_tag(self):
        child1 = LeafNode(tag="span", value="Child 1")
        parent = ParentNode(tag=None, children=[child1], props={"class": "container"})
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_parentnode_without_children(self):
        parent = ParentNode(tag="div", children=None, props={"class": "container"})
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_with_children(self):
        child1 = LeafNode(tag="span", value="Child 1")
        child2 = LeafNode(tag="span", value="Child 2")
        parent = ParentNode(tag="div", children=[child1, child2], props={"class": "container"})
        expected_html = '<div class="container"><span>Child 1</span><span>Child 2</span></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_to_html_with_grandchildren(self):
        grandchild1 = LeafNode(tag="em", value="Grandchild 1")
        grandchild2 = LeafNode(tag="strong", value="Grandchild 2")
        child1 = ParentNode(tag="span", children=[grandchild1])
        child2 = ParentNode(tag="span", children=[grandchild2])
        parent = ParentNode(tag="div", children=[child1, child2], props={"class": "container"})
        expected_html = '<div class="container"><span><em>Grandchild 1</em></span><span><strong>Grandchild 2</strong></span></div>'
        self.assertEqual(parent.to_html(), expected_html)