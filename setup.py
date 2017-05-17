from setuptools import setup

setup(name='link_storage',
      version='0.1.2',
      description='Link Storage DB wrapper',
      url='https://bitbucket.org/henrique_coura/link_storage',
      author='Henrique Coura',
      author_email='coura.henrique@gmail.com',
      license='MIT',
      packages=['link_storage'],
      install_requires=[
          'psycopg2',
      ],
      zip_safe=False)
