from setuptools import setup

setup(name='cbpi4-inkbird-plugin',
      version='0.1.0',
      description='CraftBeerPi4 inkbird temp controller Plugin',
      author='Mitch Muha',
      author_email='mitch.muha@gmail.com',
      url='',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'cbpi4-inkbird-plugin': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4-inkbird-plugin','tinytuya'],
      install_requires = ['tinytuya']
     )