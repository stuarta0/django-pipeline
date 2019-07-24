


class PipelineException(Exception):
    pass


class PackageNotFound(PipelineException):
    pass


class CompilerError(PipelineException):
    pass


class CompressorError(PipelineException):
    pass
