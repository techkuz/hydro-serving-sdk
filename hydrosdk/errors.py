class ModelBuildError(RuntimeError):
    def __init__(self, model_version):
        self.model_version = model_version
        super().__init__(model_version)