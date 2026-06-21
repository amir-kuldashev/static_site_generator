class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag=tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError()

    def __eq__(self, other:HTMLNode):
        return self.tag == other.tag and self.value == other.value \
            and self.children == other.children and self.props == other.props

    
    def props_to_html(self):
        if self.props is None or not self.props:
            return ""
        
        answer = ""
        
        for key, val in self.props.items():
            answer += f' {key}="{val}"'
        return answer

    
    def __repr__(self):
        return f"HTMLNode({self.tag}{self.value}{self.children}{self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value,props = None):
        super().__init__(tag,value,None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        
        answer = f"<{self.tag}"
        if self.props is not None:
            for key, val in self.props.items():
                answer += f' {key}="{val}"'
        answer += f">{self.value}</{self.tag}>"
        return answer
            
    def __repr__(self):
        return f"HTMLNode({self.tag}{self.value}{self.props})"




class ParentNode(HTMLNode):
    def __init__(self,tag, children,props = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("tag is missing")
        if not self.children:
            raise ValueError("children are missing")
        
        
        result = f"<{self.tag}>"
        for child in self.children:
            result += child.to_html()
        result += f"</{self.tag}>"
        
        return result
    
    