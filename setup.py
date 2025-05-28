from setuptools import setup, find_packages

setup(
    name="ndw",  
    version="0.0.1", 
    author="Ashwin Praseed",
    author_email="ashwinpraseed25@gmail.com",  
    description="A lightweight asynchronous Discord API wrapper.",
    url="",                                                                  #TO UPDATE 
    project_urls={ 
        "Bug Tracker": "https://github.com/yourusername/ndw/issues",
        "Documentation": "https://github.com/yourusername/ndw/wiki",         ##  TO UPDATE
    },
    classifiers=[
                                                                             ### TO UPDATE
    ],
    packages=find_packages(),  # Includes ndw, ndw.functions, etc.
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3.8.0",
    ],
    include_package_data=True,
    zip_safe=False,
    license="MIT",  # Change to your preferred license
    keywords="",                                                           ### TO UPDATE
)

