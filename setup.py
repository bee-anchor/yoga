from setuptools import setup

setup(name='yoga', version='0.1', description='the flexible automation framework',
      url='https://bitbucket.org/infinityworksconsulting/yoga',
      author='Bianca Linscott',
      packages=['yoga'],
      package_data={'yoga': ['resources/*', 'remote/*', 'data/*', 'pytest/*']},
      install_requires=[
        'Appium-Python-Client==0.46',
        'selenium==3.141.0',
        'urllib3==1.25.3',
        'colorama==0.4.1',
        'sauceclient==1.0.0',
        'requests==2.22.0',
        'pytest==5.0.0',
        'assertpy==0.14',
        'ipdb==0.12',
        'boto3==1.9.183',
        'PyMySQL==0.9.3',
        'pystunnel==1.0a1',
        'PyYAML==5.1',
        'Cerberus==1.3.1',
        'pytest-rerunfailures==7.0'
      ],
      setup_requires=["pytest-runner"],
      tests_require=["pytest"]
      )