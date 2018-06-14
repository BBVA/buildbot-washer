import setuptools

setuptools.setup(
    name="buildbot-washer",
    version="0.0.2",
    author="Roberto Abdelkader Martínez Pérez",
    author_email="robertomartinezp@gmail.com",
    description="Buildbot Utility Library",
    packages=setuptools.find_packages(exclude=["tests", "docs"]),
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
