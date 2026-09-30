
class HTMLNode:
    # The base class representing a node in an HTML tree.
    # It's generic - it doesn't know how to render itself yet,
    # that's left to the subclasses (LeafNode and ParentNode).
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        # This is intentionally unimplemented here.
        # Every subclass MUST override this to define how it turns into an HTML string.
        raise NotImplementedError("Subclasses should implement this method.")

    def props_to_html(self):
        # Converts the props dictionary into a string of HTML attributes.
        # e.g. {"href": "https://boot.dev", "target": "_blank"}
        # becomes: ' href="https://boot.dev" target="_blank"'
        if not self.props:
            return ""
        props_str = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        return f" {props_str}"

    def __repr__(self):
        # Just a helpful debug string so print(node) shows something readable.
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    # A LeafNode represents a node with NO children - just a tag and a value.
    # Think: <b>bold text</b> or <a href="...">link text</a>, or even plain text.
    def __init__(self, tag, value, props=None):
        # Leaf nodes never have children, so we hardcode children=None
        # by calling the parent constructor with children=None.
        super().__init__(tag=tag, value=value, children=None, props=props)

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"
    
    def to_html(self):
        # A leaf node must have a value - it's the whole point of a leaf
        # (there's nothing to render otherwise).        
        if self.value is None:
            raise ValueError("LeafNode must have a value.")
        # If there's no tag, it's just raw text with no wrapping HTML element.
        # e.g. LeafNode(None, "hello") -> "hello"
        if self.tag is None:
            return self.value
        # Otherwise wrap the value in the appropriate tag, including any props.
        # e.g. LeafNode("p", "hello") -> "<p>hello</p>"
        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    # A ParentNode represents a node that WRAPS other nodes (children),
    # rather than holding a direct text value itself.
    # Think: <div><p>...</p><p>...</p></div>
    def __init__(self, tag, children, props=None):
        # Parent nodes never hold a direct "value" - their content
        # comes entirely from rendering their children.
        super().__init__(tag=tag, children=children, props=props)

    def __repr__(self):
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"
    
    def to_html(self):
        # A parent node needs a tag to wrap around its children.
        if self.tag is None:
            raise ValueError("ParentNode must have a tag.")
        # A parent node needs children - otherwise what is it wrapping?
        if self.children is None:
            raise ValueError("ParentNode must have children.")        
        props_str = self.props_to_html()
        # Recursively call to_html() on every child, then join them together.
        # This is what makes nested structures work - a ParentNode's child
        # could itself be another ParentNode, and this line handles that
        # recursion for free.
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"