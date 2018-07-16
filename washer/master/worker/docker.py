from buildbot.worker.docker import DockerLatentWorker


class WasherDockerLatentWorker(DockerLatentWorker):
    def checkConfig(self, name, password=None,
                    environment=None, **kwargs):
        return DockerLatentWorker.checkConfig(
            self, name, password, **kwargs)

    def reconfigService(self, name, password=None,
                        environment=None, **kwargs):
        if environment is not None:
            self.environment = environment.copy()
        return DockerLatentWorker.reconfigService(
            self, name, password, **kwargs)

    def createEnvironment(self):
        result = super().createEnvironment()
        result.update(self.environment)
        return result
