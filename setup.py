from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='detacache',
    packages=['detacache'],
    version='v0.1.2',
    license='MIT',
    description='Async and Sync Function Decorator to cache function call\'s to Deta base',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='vidya sagar',
    author_email='svidya051@gmail.com',
    url='https://github.com/vidyasagar1432/detacache',
    keywords=['deta', 'cache', 'asyncio', 'deta base cache','fastapi cache',
              'cache api call', 'cache functions', 'cache requests'],
    install_requires=[
        'aiohttp',
        'requests',
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
