from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pythonik",
    version="0.5.0",  # This will be dynamically updated in CI/CD
    author="brant",
    author_email="brant@northshoreautomation.com",
    description="Python SDK for Iconik's API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/your-repo-url",  # Replace with your actual repository URL
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",  # Adjust if you have a different license
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pydantic>=2.4.2,<3.0.0",
        "requests>=2.31.0,<3.0.0",
        "loguru>=0.7.2,<1.0.0",
        "requests-mock>=1.11.0,<2.0.0",
    ],
    extras_require={
        "dev": [
            "ipython>=8.16.1,<9.0.0",
            "pytest>=7.4.2,<8.0.0",
        ],
    },
)