from setuptools import setup

setup(name='Factory',
      version='0.1',
      description='Multithread chain factory model.',
      url='https://github.com/MetalBlueberry/Factory/tree/master/Factory',
      author='MetalBlueberry',
      author_email='MetalBlueberry@example.com',
      license='GNU',
      packages=['Factory','Factory/PremadeWorks'],
      # data_files=[('qml', ['Factory/main.qml'])]
      package_data = {'Factory': ['*.qml']},
      install_requires=[
            'PyQt5',
      ],
      )
