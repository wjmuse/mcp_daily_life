"""Setup configuration for Document Assistant MCP Server."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="document-assistant-mcp",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="MCP Server for document processing, note-taking, and knowledge management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/document-assistant-mcp",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "mcp>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "document-assistant=document_assistant.server:main",
        ],
    },
)
