from setuptools import setup, find_packages


def readme() -> str:
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='digiseller',
    version='0.0.1',
    author='slava256',
    author_email='sv2021e@gmail.com',
    description='',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url=''
)
