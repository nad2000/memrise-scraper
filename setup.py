import re

from setuptools import setup

with open("memrise_scraper/__init__.py", "r") as f:
    VERSION = next(re.finditer("__version__ = \"(.*?)\"", f.read())).group(1).strip()

setup(
    name="Memrise-Scraper",
    author="Radomirs Cirskis",
    author_email="nad2000@gmail.com",
    version=VERSION,
    url="https://github.com/nad2000/memrise-scraper",
    project_urls={
        "Source Code": "https://github.com/nad2000/memrise-scraper",
    },
    packages=[
        "memrise_scraper",
    ],
    license="MIT",
    long_description=open("README.md").read(),
    install_requires=[
        "beautifulsoup4",
        "gTTS",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "memrise2tts=memrise_scraper.memrise2tts:main",
            "memrise=memrise_scraper.memrise:main",
        ]
    },
    keywords=[
        "memrise",
        "scraping",
        "scraper",
        "tts",
        "audio",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ])
