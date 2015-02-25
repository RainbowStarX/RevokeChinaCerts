from distutils.core import setup
setup(name='revoke_china_certs',
      version='1.0',
    description="Tools to disable unwanted certificates on Linux.",
    author='phoeagon',
    url='https://github.com/chengr28/RevokeChinaCerts/Linux/',
    packages=['revoke_china_certs'],
    install_requires=[],
    entry_points="""
    [console_scripts]
    revoke_china_certs = revoke_china_certs.main:main
    """,
)
