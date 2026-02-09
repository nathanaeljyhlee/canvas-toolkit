from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="canvas-toolkit",
    version="0.1.0",
    author="Nathanael",
    description="Export Canvas LMS assignments to Excel, CSV, or JSON",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/[your-username]/canvas-toolkit",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "pandas>=2.0.0",
        "openpyxl>=3.1.0",
        "xlsxwriter>=3.1.0",
        "streamlit>=1.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "mypy>=1.5.0",
        ],
        "notion": [
            "notion-client>=2.0.0",
        ],
    },
)
