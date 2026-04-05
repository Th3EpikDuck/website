class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
      self.tag = tag
      self.value = value
      self.children = children
      self.props = props
    
  def to_html(self):
      raise NonImplementedError()

  def props_to_html(self):
      if not self.props:
          return ""
      for key, value in self.props.items():
          props_str += f' {key}="{value}"'
      return props_str

  def __repr__(self):
      print(f"HTMLNODE: ({self.tag}, {self.value}, {self.children}, {self.props})")
