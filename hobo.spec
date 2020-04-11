# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
         ( 'fonts/', 'fonts' ),
         ( 'images/', 'images' ),
         ( 'media/', 'media' ),
         ]

a = Analysis(['hobo.py'],
             pathex=['C:\\Users\\Lazarus\\Desktop\\hogwartshobo'],
             binaries=[],
             datas=added_files,
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
          name='hobo',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='hobo')
