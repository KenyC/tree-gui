# Tree GUI

## Requirements

- Kivy

## Use

- Left-click on nodes to create branches.
	* click on leaves will sprout two new branches
	* click on internal nodes will create a binary branching mother for node ; node will be rightmost daughter
- Right-click on nodes to remove daughters.
- Scroll to zoom in and out.
- Use middle mouse button to drag display.
- Ctrl+Left click on a node to put text cursor on position of node in tree
- Edit right text input to add labels.
- Press Enter in the text zone to copy current tree to clipboard (Selection & Ctrl+C is also supported by Kivy).

## More

If you want to export to other formats, you just have to:

1. Derive a class from Transducer (transducer.py).
2. Overload Unsat : it takes a tree and a list of labels for it as an argument and returns a list of strings of the form: "[... , labels[0], ... , labels[1], ...  .... ]", which when joined, gives the string representation of the tree with the provided list of labels.
3. In app.py, import the class you defined.
4. Modify the definition of DEFAULT_TRANSDUCER and assign it to your class.
```python
DEFAULT_TRANSDUCER = MyCustomTransducer
```

## Note

My version of Kivy on Windows crashed when copying something to the clipboard ; refer to [this](https://github.com/kivy/kivy/pull/5579/files) for a fix.