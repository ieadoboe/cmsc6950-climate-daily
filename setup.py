from setuptools import setup, find_packages

setup(
    name="climate-dtr",
    version="0.1.0",
    description="Diurnal Temperature Range analysis for St. John's climate data",
    author="Your Name",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
    ],
)
