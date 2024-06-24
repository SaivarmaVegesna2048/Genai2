from setuptools import setup,find_packages
setup(
    name='mcq_generator',
    version='0.0.1',
    author='VNSKVarma',
    author_email='saivarma2710@gmail.com',
    install_requires=['openai','langchain','streamlit','python-dotenv','PyPDF2'],
    packages=find_packages()

)