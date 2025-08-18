import os
from setuptools import setup


APP = [os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'polkadot_image_reviewer.py'))]
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': None,
    'plist': {
        'CFBundleName': 'PolkaDot Image Reviewer',
        'CFBundleDisplayName': 'PolkaDot Image Reviewer',
        'CFBundleShortVersionString': '1.0',
        'CFBundleVersion': '1.0',
        'LSMinimumSystemVersion': '11.0',
        'NSHighResolutionCapable': True,
    },
    'packages': [
        'PIL',
    ],
    'includes': [
        'tkinter',
        'tkinterdnd2',
        'icu',
    ],
}


setup(
    app=APP,
    name='PolkaDot Image Reviewer',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

