from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pncl',
    version='1.0.0',
    packages=find_packages(),
    package_data={
        'pncl': ['static/*']
    },
    install_requires=['aiohttp',
                      'aiohttp-sse',
                      'numpy',
                      'requests'],
    url='https://github.com/danielegrattarola/pncl',
    license='MIT',
    author='Daniele Grattarola',
    author_email='daniele.grattarola@gmail.com',
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ],
)
