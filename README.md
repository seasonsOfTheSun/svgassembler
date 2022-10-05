# svgassembler

Combine individual ```.svg``` files into one big ```.svg``` file, placing the subplots programatically (i.e. set ```x,y```coordinates and it moves the subplot there).
This makes the subplots automatically evenly spaced, aligned, and it's easy to move them in and out of the viewBox. Hopefully this will save some headaches in inkscape, omnigraffle, illustrator etc.

Here's what you can find in ```example.ipynb```

Make a plot object.
```
from svgassemble import Subplot, Plot
plot = Plot(width=1000, height=300)
```

Import your ```.svg``` files and add them as subplots of the main plot.  

```
filename = "figures/ringiness_genes.svg"
example_subplot1 = Subplot(filename)
plot.append(example_subplot1)

filename = "figures/ringiness_fibro.svg"
example_subplot2 = Subplot(filename)
plot.append(example_subplot2)
```

Adjust the size and position (in that order) of your subplots to taste.

```
example_subplot1.scale(0.1)
example_subplot1.translate(20,50)

example_subplot2.scale(0.1)
example_subplot2.translate(10,10)
```
Now write to a destination file. It will overwrite without promppting so be careful.
```
plot.write("myplot.svg")
```
Sadly you can't view this directly in the notebook, but you can open it in another tab of the browser and take a look at the result. You'll probably have to iterate a few times to get it to look how you wanted so keep hitting that refresh button.
