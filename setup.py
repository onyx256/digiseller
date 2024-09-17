from setuptools import setup, find_packages


def readme() -> str:
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='digiseller',
    version='0.0.6',
    author='slava256',
    author_email='sv2021e@gmail.com',
    description='Digiseller API wrapper',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/onyx256/digiseller',
    install_requires=['requests>=2.32.3'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='digiseller',
    project_urls={
        'GitHub': 'https://github.com/onyx256/digiseller'
    },
    python_requires='>=3.11'
)
