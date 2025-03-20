from collections import defaultdict

class addressdefaultdict(defaultdict):
    def __missing__(self,key):
        self[key] = key
        return key
    
class colordefaultdict(defaultdict):
    color=["PURPLE","DEEP_PURPLE","INDIGO","CYAN","TEAL","LIME","AMBER","ORANGE","DEEP_ORANGE","BROWN"]
    def __missing__(self,key):
        self[key] = self.color[0]
        self.color.pop(0)
        return self[key]