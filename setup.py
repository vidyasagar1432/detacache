from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name = 'DetaCache', 
    packages = ['DetaCache'],
    version = 'v0.0.3',
    license='MIT', 
    description = 'Decorator to cache in Deta base',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'vidya sagar', 
    author_email = 'svidya051@gmail.com',
    url = 'https://github.com/vidyasagar1432/DetaCache',
    keywords = ['deta','cache','deta base cache','cache api call','cache functions','cache locally'], 
    install_requires=[
        'deta==1.0.1',
        'aiohttp==3.8.1',
        'tinydb==4.5.2'
        ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent', 
    'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)