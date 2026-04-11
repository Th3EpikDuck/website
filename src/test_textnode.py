import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks
from textnode import BlockType, block_to_block_type

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_diff_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("Different text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_diff_type(self):
        node = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_with_url(self):
        node = TextNode("link", TextType.LINK, "https://boot.dev")
        node2 = TextNode("link", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_diff_url(self):
        node = TextNode("link", TextType.LINK, "https://a.com")
        node2 = TextNode("link", TextType.LINK, "https://b.com")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")
        self.assertEqual(html_node.props, None)

    def test_code(self):
        node = TextNode("print('hi')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hi')")
        self.assertEqual(html_node.props, None)

    def test_link(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Boot.dev")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_image(self):
        node = TextNode("logo", TextType.IMAGE, "https://boot.dev/logo.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://boot.dev/logo.png", "alt": "logo"}
        )

    def test_invalid_text_type_raises_exception(self):
        node = TextNode("bad", "not_a_valid_type")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_split_nodes_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]
        )
    
    def test_split_nodes_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ]
        )
    
    def test_split_nodes_multiple_delimiters(self):
        node = TextNode("This has `code` and `more code` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("more code", TextType.CODE),
                TextNode(" here", TextType.TEXT),
            ]
        )
    
    def test_split_nodes_no_delimiter(self):
        node = TextNode("This has no special text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [TextNode("This has no special text", TextType.TEXT)]
        )
    
    def test_split_nodes_non_text_node(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [TextNode("already bold", TextType.BOLD)]
        )
    
    def test_split_nodes_mixed_nodes(self):
        nodes = [
            TextNode("This is `code`", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode("already bold", TextType.BOLD),
            ]
        )
    
    def test_split_nodes_raises_error_on_invalid_markdown(self):
        node = TextNode("This is `broken code text", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)
    
    def test_split_nodes_delimiter_at_start(self):
        node = TextNode("`code` at start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("code", TextType.CODE),
                TextNode(" at start", TextType.TEXT),
            ]
        )
    
    def test_split_nodes_delimiter_at_end(self):
        node = TextNode("at end `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("at end ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ]
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link to [to youtube](https://www.youtube.com)"
        )
        self.assertListEqual([("to youtube", "https://www.youtube.com")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "Here is ![first](https://a.com/1.png) and ![second](https://a.com/2.jpg)"
        )
        self.assertListEqual(
            [
                ("first", "https://a.com/1.png"),
                ("second", "https://a.com/2.jpg"),
            ],
            matches,
        )

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images(
            "This text has no markdown images."
        )
        self.assertListEqual([], matches)
    
    def test_extract_markdown_images_empty_alt(self):
        matches = extract_markdown_images(
            "An image with no alt text: ![](https://a.com/blank.png)"
        )
        self.assertListEqual(
            [("", "https://a.com/blank.png")],
            matches,
        )
    
    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "Links: [Boot.dev](https://boot.dev) and [YouTube](https://youtube.com)"
        )
        self.assertListEqual(
            [
                ("Boot.dev", "https://boot.dev"),
                ("YouTube", "https://youtube.com"),
            ],
            matches,
        )
    
    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links(
            "This text has no markdown links."
        )
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links_ignores_images(self):
        matches = extract_markdown_links(
            "Here is an image ![logo](https://a.com/logo.png) and a link [site](https://a.com)"
        )
        self.assertListEqual(
            [("site", "https://a.com")],
            matches,
        )
    
    def test_extract_markdown_links_empty_anchor(self):
        matches = extract_markdown_links(
            "Empty anchor: [](https://a.com)"
        )
        self.assertListEqual(
            [("", "https://a.com")],
            matches,
        )

    def test_split_nodes_image_basic(self):
        nodes = [
            {"type": "text", "text": "Here is an image ![alt](https://a.com/img.png)"}
        ]
    
        result = split_nodes_image(nodes)
    
        self.assertEqual(
            result,
            [
                {"type": "text", "text": "Here is an image "},
                {"type": "image", "alt": "alt", "url": "https://a.com/img.png"},
            ]
        )
    
    
    def test_split_nodes_image_multiple(self):
        nodes = [
            {"type": "text", "text": "![a](1.png) and ![b](2.png)"}
        ]
    
        result = split_nodes_image(nodes)
    
        self.assertEqual(
            result,
            [
                {"type": "image", "alt": "a", "url": "1.png"},
                {"type": "text", "text": " and "},
                {"type": "image", "alt": "b", "url": "2.png"},
            ]
        )
    
    
    def test_split_nodes_image_no_image(self):
        nodes = [
            {"type": "text", "text": "just text"}
        ]
    
        result = split_nodes_image(nodes)
    
        self.assertEqual(result, nodes)
    
    
    def test_split_nodes_image_mixed_nodes(self):
        nodes = [
            {"type": "text", "text": "before ![alt](img.png) after"},
            {"type": "image", "alt": "existing", "url": "x.png"},
        ]
    
        result = split_nodes_image(nodes)
    
        self.assertEqual(
            result,
            [
                {"type": "text", "text": "before "},
                {"type": "image", "alt": "alt", "url": "img.png"},
                {"type": "text", "text": " after"},
                {"type": "image", "alt": "existing", "url": "x.png"},
            ]
        )

    def test_split_nodes_link_basic(self):
        nodes = [
            {"type": "text", "text": "click [here](https://a.com)"}
        ]
    
        result = split_nodes_link(nodes)
    
        self.assertEqual(
            result,
            [
                {"type": "text", "text": "click "},
                {"type": "link", "text": "here", "url": "https://a.com"},
            ]
        )
    
    
    def test_split_nodes_link_multiple(self):
        nodes = [
            {"type": "text", "text": "[a](1.com) and [b](2.com)"}
        ]
    
        result = split_nodes_link(nodes)
    
        self.assertEqual(
            result,
            [
                {"type": "link", "text": "a", "url": "1.com"},
                {"type": "text", "text": " and "},
                {"type": "link", "text": "b", "url": "2.com"},
            ]
        )
    
    
    def test_split_nodes_link_no_links(self):
        nodes = [
            {"type": "text", "text": "no links here"}
        ]
    
        result = split_nodes_link(nodes)
    
        self.assertEqual(result, nodes)
    
    
    def test_split_nodes_link_mixed_nodes(self):
        nodes = [
            {"type": "text", "text": "before [x](a.com) after"},
            {"type": "link", "text": "existing", "url": "b.com"},
        ]
    
        result = split_nodes_link(nodes)
    
        self.assertEqual(
            result,
            [
                {"type": "text", "text": "before "},
                {"type": "link", "text": "x", "url": "a.com"},
                {"type": "text", "text": " after"},
                {"type": "link", "text": "existing", "url": "b.com"},
            ]
        )

    def test_text_to_textnodes_plain(self):
        result = text_to_textnodes("just text")
    
        self.assertEqual(
            result,
            [TextNode("just text", TextType.TEXT)]
        )

    def test_text_to_textnodes_bold(self):
        result = text_to_textnodes("this is **bold** text")
    
        self.assertEqual(
            result,
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]
        )
    
    
    def test_text_to_textnodes_italic(self):
        result = text_to_textnodes("this is _italic_ text")
    
        self.assertEqual(
            result,
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ]
        )
    
    
    def test_text_to_textnodes_code(self):
        result = text_to_textnodes("this is `code` text")
    
        self.assertEqual(
            result,
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ]
        )

    def test_basic_split(self):
        md = "# Heading\n\nParagraph text\n\n- item 1\n- item 2"
        result = markdown_to_blocks(md)
        self.assertEqual(result, [
            "# Heading",
            "Paragraph text",
            "- item 1\n- item 2"
        ])

    def test_strips_whitespace(self):
        md = "   # Heading   \n\n   Paragraph   "
        result = markdown_to_blocks(md)
        self.assertEqual(result, [
            "# Heading",
            "Paragraph"
        ])

    def test_extra_newlines_removed(self):
        md = "# Heading\n\n\n\nParagraph"
        result = markdown_to_blocks(md)
        self.assertEqual(result, [
            "# Heading",
            "Paragraph"
        ])

    def test_only_newlines(self):
        md = "\n\n\n"
        result = markdown_to_blocks(md)
        self.assertEqual(result, [])

    def test_single_block(self):
        md = "Just a single block"
        result = markdown_to_blocks(md)
        self.assertEqual(result, ["Just a single block"])

    def test_block_heading(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_code_block(self):
        block = "```\ncode here\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_block_quote(self):
        block = "> line1\n> line2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_block_unordered_list(self):
        block = "- item1\n- item2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_block_ordered_list(self):
        block = "1. item1\n2. item2"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_block_paragraph(self):
        block = "just a normal paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
