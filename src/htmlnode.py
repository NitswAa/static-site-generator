class HTMLNode():
    def __init__(self, children=None, tag=None, value=None, props=None):

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise(NotImplemented)
    
    def props_to_html(self):
        if not self.props:
            return ""

        return "".join(map(lambda prop:f" {prop}=\"{self.props[prop]}\"", self.props))
    
    def __repr__(self):
        return f"<HTMLNode with tag={self.tag}, value={self.value}, children={self.children}, props={self.props}>"

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.props == other.props


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError(f"{self.__repr__()} has no value!")

        if not self.tag:
            return self.value

        # Not sure if I want to keep value -> alt text as intended behavior...
        if self.tag == "img":
            return f"<img{super().props_to_html()} alt=\"{self.value}\" />"
        
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"


    def __repr__(self):
        return f"<LeafNode with tag={self.tag}, value={self.value}, props={self.props}>"


class ParentNode(HTMLNode):
    def __init__(self, children, tag=None, props=None):
        self.tag = tag
        self.value = None
        self.children = children
        self.props = props

    def to_html(self):
        if not self.tag:
            raise ValueError(f"{self} has no tag!")

        return f"<{self.tag}{self.props_to_html()}>{''.join(map(lambda child:child.to_html(), self.children))}</{self.tag}>"



