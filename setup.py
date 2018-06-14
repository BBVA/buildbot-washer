import setuptools

setuptools.setup(
    name="buildbot-washer",
    version="0.0.4",
    author="Roberto Abdelkader Martínez Pérez",
    author_email="robertomartinezp@gmail.com",
    description="Buildbot Utility Library",
    packages=setuptools.find_packages(exclude=["tests", "docs"]),
    license="Apache",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Framework :: Buildout :: Extension',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing'
    ],
    install_requires=[
        "environconfig==1.7.0"
    ],
    entry_points={
        "buildbot.steps": [
            "TriggerFromFile = washer.master.steps:TriggerFromFile",
            "WasherTask = washer.master.steps:WasherTask"],
        "buildbot.worker": [
            "WasherDockerLatentWorker = washer.master.worker.docker:WasherDockerLatentWorker"
        ]
    }
)
