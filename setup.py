import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="faa-aircraft-registry",
    version="0.1.0",
    author="Austin Baldwin",
    author_email="austin.baldwin@clearaerospace.com",
    description="Format FAA aircraft registry database into Python dictionaries for programmatic use.",
    keywords="faa aircraft registry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ClearAerospace/faa-aircraft-registry",
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
    ],
    python_requires='>=3.8',
)
