# Tree GUI

## Requirements

- Kivy

## Use

- Left-click on nodes to create branches.
- Right-click on nodes to remove daughters.
- Scroll to zoom in and out.
- Use middle mouse button to drag display.
- Edit right text input to add labels.
- Press Enter in the text zone to copy current tree to clipboard (Selection & Ctrl+C is also supported by Kivy).

## More

If you want to export to other formats, you just have to:

1. Derive a class from Transducer (transducer.py).
2. Overload Unsat : it takes a tree as an argument and returns a pre-formatted string of the form: "... {0} ... {1} ...  .... {n-1} ...", where "{i}" is the slot in which the label of node *i* is to be inserted.
3. In app.py, import the class you defined.
4. Modify the definition of DEFAULT_TRANSDUCER and assign it to your class.
```python
DEFAULT_TRANSDUCER = MyCustomTransducer
```

## Note

My version of Kivy on Windows crashed when copying something to the clipboard ; refer to [this](https://github.com/kivy/kivy/pull/5579/files) for a fix.