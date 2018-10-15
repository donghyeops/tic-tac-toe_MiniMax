# -*- mode: python -*-

block_cipher = None


datas= [
    ('icon/*', 'icon'),
    ('3x3_game.ui', './')
]

a = Analysis(['run_game.py'],
             pathex=[r'C:\Python36\Lib\site-packages\PyQt5\Qt\bin'],
             binaries=[],
             datas=datas,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher
             )
pyz = PYZ(a.pure,
          a.zipped_data,
          cipher=block_cipher)
          
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='run_game',
          debug=False,
          strip=False,
          upx=True,
          console=True )