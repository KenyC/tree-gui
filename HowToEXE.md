# How to turn to .exe

## Launch command

```cmd
python -m PyInstaller --name TreeMaker --icon iconTree.ico path_to_main_python_file
```

## Modify spec file

Add Kivy dependencies, make sure to include the correct provider for SDL (*angle* on my computer). Otherwise, just replace the created TreeMaker.spec with the file provided in this folder (also called *TreeMaker.spec*).

## Launch command

```cmd
python -m PyInstaller path_to_spec_file
```

