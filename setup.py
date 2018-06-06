import setuptools

setuptools.setup(
    name="buildbot-washer",
    version="0.0.1",
    author="Roberto Abdelkader Martínez Pérez",
    author_email="robertomartinezp@gmail.com",
    description="Buildbot Utility Library",
    packages=setuptools.find_packages(exclude=["tests", "docs"]),
    install_requires=["buildbot-worker>=0.9.0"],
    entry_points={
        "buildbot.worker": [
            "WasherDockerLatentWorker = washer.master.worker.docker:WasherDockerLatentWorker"
        ]
    }
)
