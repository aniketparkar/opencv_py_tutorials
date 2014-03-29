from setuptools import setup, find_packages

setup(name='cv2tutorial',
        version='0.1',
        description='python opencv tutorial scripts',
        author='Jason Hobbs',
        author_email='jason.hobbs@gmail.com',
        packages=find_packages(),
        package_data={'cv2tutorial': ['extra/*']},
)
