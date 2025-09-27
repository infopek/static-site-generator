class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("Not implemented")

    def props_to_html(self):
        if not self.props:
            return ""

        res = ""
        for k, v in self.props.items():
            res += f" {k}=\"{v}\""
        return res
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("all parent nodes must have a tag")
        if not self.children:
            raise ValueError("all parent nodes must have children nodes")
        
        res = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            res += child.to_html()
        res += f"</{self.tag}>"

        return res

