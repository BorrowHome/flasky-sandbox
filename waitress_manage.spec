# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['waitress_manage.py'],
             pathex=['C:\\Users\\llb\\Documents\\coding\\test\\flasky-sandbox'],
             binaries=[],
             datas=[],
             hiddenimports=['sklearn.utils._weight_vector','sklearn.neighbors.typedefs','sklearn.neighbors.quad_tree','sklearn','sklearn.utils.lgamma','sklearn.utils.weight_vector','pkg_resources.py2_warn','pkg_resources.markers'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='waitress_manage',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
