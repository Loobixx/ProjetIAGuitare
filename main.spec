# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[("Modele_IA\modele_notes_guitare.h5", "C:\Users\yprud\OneDrive\Documents\L3\MonProjet\IA\Modele_IA\modele_notes_guitare.h5")("Modele_IA\scaler.pkl", "C:\Users\yprud\OneDrive\Documents\L3\MonProjet\IA\Modele_IA\scaler.pkl"), ("Modele_IA\encodeur_etiquettes.pkl","C:\Users\yprud\OneDrive\Documents\L3\MonProjet\IA\Modele_IA\encodeur_etiquettes.pkl"), ("Modele_IA", "C:\Users\yprud\OneDrive\Documents\L3\MonProjet\IA\Modele_IA"],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],C:\Users\yprud\OneDrive\Documents\L3\MonProjet\IA\Modele_IA
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
