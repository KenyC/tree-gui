# -*- mode: python -*-
from kivy.deps import sdl2, angle
block_cipher = None


a = Analysis(['..\\TreeApp\\app.py'],
             pathex=['C:\\Keny\\ProjetsPython\\TreeMakerExe'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='TreeMaker',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='treeIcon.ico')
coll = COLLECT(exe, Tree('..\\TreeApp\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + angle.dep_bins)],
               strip=False,
               upx=True,
               name='TreeMaker')