import logfire


def configure_observability():
    logfire.configure()
    logfire.instrument_system_metrics()
    logfire.instrument_pydantic_ai()