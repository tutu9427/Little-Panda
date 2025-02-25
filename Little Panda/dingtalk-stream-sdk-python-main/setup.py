import os
import re
from setuptools import setup

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
VERSION_STRING = ''
with open(os.path.join(BASE_PATH, 'dingtalk_stream', 'version.py')) as fp:
    content = fp.read()
    VERSION_STRING = re.findall(r"VERSION_STRING\s*=\s*\'(.*?)\'", content)[0]

setup(
    name='dingtalk-stream',
    version=VERSION_STRING,
    description='A Python library for sending messages to DingTalk chatbot',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/open-dingtalk/dingtalk-stream-sdk-python',
    author='Ke Jie',
    author_email='jinxi.kj@alibaba-inc.com',
    license='MIT',
    packages=['dingtalk_stream'],
    install_requires=[
        'websockets>=11.0.2',
        'requests>=2.27.1',
        'aiohttp>=3.10.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
