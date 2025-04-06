def load_config(name=None):
    if name == "Production":
        from model_api.config.prod_config import ProdConfig

        return ProdConfig

    if name == "Test":
        from model_api.config.test_config import TestConfig

        return TestConfig
    if name == "Dev":
        from model_api.config.dev_config import DevConfig

        return DevConfig
