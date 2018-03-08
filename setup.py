from setuptools import setup

setup(
    name='twitter-iconfix',
    version='0.1.1',
    description='tool to add transparent pixel to twitter icons to keep as PNG',
    author='Syfaro',
    author_email='syfaro@huefox.com',
    packages=['twitter_iconfix'],
    install_requires=['pillow', 'birdy'],
    entry_points={
        'console_scripts': [
            'twitter_iconfix=twitter_iconfix.__main__:main'
        ]
    }
)
