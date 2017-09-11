from setuptools import setup

setup(name='Factory',
      version='0.1',
      description='Multithread chain factory model.',
      url='',
      author='MetalBlueberry',
      author_email='MetalBlueberry@example.com',
      license='GNU',
      packages=['Factory'],
      # data_files=[('qml', ['Factory/main.qml'])]
      package_data = {'Factory': ['*.qml']},
      )
