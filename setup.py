from setuptools import setup

setup(name='faf', version='0.1', description='flexible automation framework',
      url='https://bitbucket.org/infinityworksconsulting/faf',
      author='Bianca Linscott',
      packages=['faf'],
      package_data={'faf': ['resources/*', 'remote/*']},
      install_requires=[
        'Appium-Python-Client==0.28',
        'selenium==3.14.0',
        'urllib3==1.23',
        'colorama==0.3.9',
        'sauceclient==1.0.0',
        'requests==2.19.1',
        'pytest==3.7.3',
        'assertpy==0.14'
      ],
      setup_requires=["pytest-runner"],
      tests_require=["pytest"]
      )