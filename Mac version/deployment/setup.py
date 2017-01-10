from setuptools import setup

setup(
    app=['query_agent.py'],
    setup_requires=['py2app'],
    options={
          'py2app': {
              'packages': ['requests']
           }
       }
)