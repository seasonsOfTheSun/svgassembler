from lxml import etree

class Subplot:
    
    def __init__(self, filename):
        self.metadata = []
        self.defs = []
        self.geometry_nodes = []
        self.top = {}
        # split the elements in the svg file into
        # components
        parser = etree.XMLParser(remove_comments=True)
        tree = etree.parse(filename,parser=parser)
        root = tree.getroot()
        
        self.tag = root.tag
        self.top = root.attrib
        
        for child in root:
            tag = child.tag.split("}")[-1]
            if tag == "metadata":
                self.metadata = child
            if tag == "defs":
                self.defs.append(child)
            if tag == "g":
                self.geometry_nodes.append(child)
                
        
        
        # group all the geometry nodes together into one
        self.geometry = etree.Element("{http://www.w3.org/2000/svg}g")
        for i,node in enumerate(self.geometry_nodes):
            self.geometry.insert(i, node)

    def translate(self, dx, dy):
        self.geometry.set("transform", f"translate({dx}, {dy})")

    def scale(self, factor):
        self.geometry.set("transform", f"scale({factor})")

    def to_svg(self):
        
        root = etree.Element("{http://www.w3.org/2000/svg}svg")
        
        root.append(self.metadata)
        root.extend(self.defs)
        root.append(self.geometry)
        
        root.tag = self.tag
        for i,v in self.top.items():
            root.set(i,v)
        
        self.root = root
        
    def write(self, filename):
        self.to_svg()
        prefix = b"""<?xml version="1.0" encoding="utf-8" standalone="no"?>
        <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
          "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n"""
        fp = open(filename, 'wb')
        fp.write(prefix + etree.tostring(self.root))
        fp.flush()
        fp.close()

class Plot:
    
    def __init__(self, height, width):
        self.subplots = []
        self.height = height
        self.width = width
        
    def append(self, subplot):
        self.subplots.append(subplot)
        
    def to_svg(self):
        
        # group all the geometry nodes together into one
        self.geometry = etree.Element("{http://www.w3.org/2000/svg}g")

        root = etree.Element("{http://www.w3.org/2000/svg}svg")
        
        root.set("width", str(self.width)+"pt")
        root.set("height", str(self.height)+"pt")
        root.set("viewBox", f"0 0 {self.width} {self.height}")
        root.set("version","1.1") 
        
        root.append(self.subplots[0].metadata)
        
        for subplot in self.subplots:
            for i in subplot.defs:
                root.append(i)
            root.append(subplot.geometry)


        self.root = root
            
    def write(self, filename):
        self.to_svg()
        prefix = b"""<?xml version="1.0" encoding="utf-8" standalone="no"?>
        <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
          "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n"""
        fp = open(filename, 'wb')
        fp.write(prefix + etree.tostring(self.root))
        fp.flush()
        fp.close()            
        