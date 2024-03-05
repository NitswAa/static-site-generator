class TextNode():
    valid_types =   [
                    "text",
                    "bold",
                    "italic",
                    "code",
                    "link",
                    "img",
                    ]

    def __init__(self, text, text_type, url=None):
        if text_type not in self.valid_types:
            raise ValueError("Invalid Text Type")
       
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text 
                and self.text_type == other.text_type 
                and self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    
