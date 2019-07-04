import setuptools

setuptools.setup(
    name="buildbot-washer",
    version="1.2.0",
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Testing'
    ],
    install_requires=[
        "environconfig==1.7.0"
    ],
    entry_points={
        "buildbot.steps": [
            "TriggerFromFile = washer.master.steps.triggerfromfile:TriggerFromFile",
            "WasherTask = washer.master.steps.washertask:WasherTask",
            "ReduceTriggerProperties = washer.master.steps.reducetriggerproperties:ReduceTriggerProperties"
        ],
        "buildbot.worker": [
            "WasherDockerLatentWorker = washer.master.worker.docker:WasherDockerLatentWorker"
        ]
    }
)
