from setuptools import setup, find_packages


with open("README.md") as readme_f:
    readme = readme_f.read()

setup(
    name="batch_text_io",
    version="0.1.0",
    description="Batch text processing with OpenAI",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="mimoody",
    author_email="svev2369@example.com",
    install_requires=["openai==1.44.1", "pydantic==2.9.1"],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
