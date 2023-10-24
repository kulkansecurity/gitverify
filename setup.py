from setuptools import setup

setup(
    name='gitverify',
    description='GitVerify is a tool designed to analyze GitHub repositories and provide insights into their trustworthiness. It gathers data from the GitHub API and, optionally, performs VirusTotal checks on associated domains, then presents the results in a concise, user-friendly manner.',
    author='kulkansecurity',
    url='https://github.com/kulkansecurity/gitverify',
    packages=[
        'gitverify'
    ],
)
