from setuptools import setup, find_packages

"""
The setup.py file is used to package the project as a Python package.
It includes metadata about the package, such as its name, version, author, and description.
It also specifies the dependencies required to run the package.
The setup.py file is used by setuptools to build and distribute the package.
"""


def get_requirements() -> list[str]:
    """
    Reads the requirements.txt file and returns a list of required packages.
    """
    try:
        with open("requirements.txt", "r") as f:
            requirements = f.readlines()
            for requirement in requirements:
                if requirement.startswith("#") or requirement.startswith("-e"):
                    requirements.remove(requirement)
            requirements = [r.strip() for r in requirements]
            return requirements
    except FileNotFoundError:
        print("requirements.txt file not found. Please create one.")
        return []
    except Exception as e:
        print(f"An error occurred while reading requirements.txt: {e}")
        return []


setup(
    name="NetworkSecurity",
    version="0.1.0",
    author="Bhupendra Parmar",
    author_email="bhupenparmar192@gmail.com",
    description="A Python package for Network Security.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=get_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "network_security=network_security.__main__:main",
        ],
    },
    project_urls={},
    keywords="phishing detection, network security, malware detection, url classifier,email security,cyber security",
    license="MIT",
)
