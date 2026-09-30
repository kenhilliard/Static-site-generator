import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType

class TestSplitDelimiter(unittest.TestCase):
    
    def test_split_nodes_delimiter(self):
        node1 = TextNode("This is a plain text node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1], "**", TextType.BOLD)
        expected = [
            TextNode("This is a plain text node", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

        node2 = TextNode("This is a **BOLD** text node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node2], "**", TextType.BOLD)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("BOLD", TextType.BOLD),
            TextNode(" text node", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

        node3 = TextNode("This is a __italic__ text node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node3], "__", TextType.ITALIC)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text node", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

        node4 = TextNode("This is a `code` text node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node4], "`", TextType.CODE)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text node", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

        node5 = TextNode("This is a **BOLD text node", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node5], "**", TextType.BOLD)

        node6 = TextNode("This is a **BOLD** text node", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node6], "**", TextType.BOLD)
        expected = [
            TextNode("This is a **BOLD** text node", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected)

        node7 = TextNode("This **is** a **BOLD** text node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node7], "**", TextType.BOLD)
        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("is", TextType.BOLD),
            TextNode(" a ", TextType.TEXT),
            TextNode("BOLD", TextType.BOLD),
            TextNode(" text node", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com)"
        )
        self.assertListEqual([("link", "https://www.example.com")], matches)

    def test_extract_markdown_link_none(self):
        matches = extract_markdown_links(
            "This is plain text with no links."
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_image_none(self):
        matches = extract_markdown_images(
            "This is plain text with no images."
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_link_multiple(self):
        matches = extract_markdown_links(
            "This is text with a [first link](https://www.example.com) and a [second link](https://www.boot.dev)"
        )
        self.assertListEqual(
            [
                ("first link", "https://www.example.com"),
                ("second link", "https://www.boot.dev"),
            ],
            matches,
        )

    def test_extract_markdown_links_ignores_images(self):
        text = "Here is an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_with_only_image(self):
        text = "Here is just an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_split_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_multiple_links(self):
        node = TextNode(
            "This is text with a [first link](https://www.example.com) and another [second link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("first link", TextType.LINK, "https://www.example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_image_and_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.boot.dev)",
            TextType.TEXT,
        )
        # image is parsed, link remains as plain text
        nodes_with_images = split_nodes_image([node])
        # link is now parsed
        new_nodes = split_nodes_link(nodes_with_images)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is a text with a [link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_no_links_or_images(self):
        node = TextNode(
            "This is plain text with no links or images", TextType.TEXT,
        )
        nodes_with_images = split_nodes_image([node])
        new_nodes = split_nodes_link(nodes_with_images)
        self.assertListEqual(
            [
                TextNode("This is plain text with no links or images", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) starts with an image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" starts with an image", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_at_start(self):
        node = TextNode(
            "[link](https://www.boot.dev) starts with a link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" starts with a link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://www.boot.dev)"
        actual = text_to_textnodes(text)        
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.boot.dev"),
        ]
        self.assertListEqual(actual, expected)


