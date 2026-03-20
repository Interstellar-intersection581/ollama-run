from setuptools import setup

setup(
    name="ollama-run",
    version="4.8.0",
    py_modules=["main"],
    install_requires=[
        "ollama",
        "psutil",
        "duckduckgo-search",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "ollama-run=main:main",
        ],
    },
)
