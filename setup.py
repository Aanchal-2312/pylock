from setuptools import setup, find_packages

setup(
    name="pylock",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "bcrypt",
        "pyperclip"
    ],
    entry_points={
        "console_scripts": [
            "pylock=pylock.cli:main"
        ]
    }
)