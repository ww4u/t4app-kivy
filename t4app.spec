# -*- mode: python -*-
from kivy.deps import sdl2,glew
block_cipher = None


a = Analysis(['E:\\study\\kivy\\t4app\\t4app.py'],
             pathex=['E:\\study\\kivy\\t4app\\output'],
             binaries=[],
             datas=[],
             hiddenimports=[ 'win32timezone' ],
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
          name='MRX-T4',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='E:\\study\\kivy\\t4app\\image\\megarobo.ico' )
coll = COLLECT(exe,Tree('E:\\study\\kivy\\t4app\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='MRX-T4')
