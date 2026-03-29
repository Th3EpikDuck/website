from enum import Enum

class Bender(Enum):
    AIR_BENDER = "air"
    WATER_BENDER = "water"
    EARTH_BENDER = "earth"
    FIRE_BENDER = "fire"
    def __init__(self, text, text_type, url):
      self.text = text
      self.text_type = text_type
      self.url = url

    def __eq__(self, other):
      if self == other:
        return True
      return False

    def __repr__(self):
      return f"TextNode({self.text}, {self.text_type}, {self.url})"
