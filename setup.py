from setuptools import setup, find_packages

VERSION = '0.0.1'
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name="b2b-AI",
    version=VERSION,
    description='A package that analyses songs and converts them to MIDI files.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Gheorghe Andrei",
    author_email="gheorgheandrei13@gmail.com",
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    classifiers= [
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6"
)
