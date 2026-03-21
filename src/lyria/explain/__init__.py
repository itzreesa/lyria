import os

class LyriaExplain():
  def __init__(self, component):
    self.component = component
    self.base_path = os.path.dirname(os.path.realpath(__file__))

  def get_help_file(self,):
    if not os.path.exists(os.path.join(self.base_path, self.component + ".txt")):
      return None
    with open(os.path.join(self.base_path, self.component + ".txt"), "r") as f:
      return f.read()
    
  def run(self,):
    help_file = self.get_help_file()
    print(f" - Explaining component \"{self.component}\":")
    print(help_file)