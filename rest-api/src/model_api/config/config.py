def load_config(name=None):
    if name == "Production":
        from model_api.config.prod_config import ProdConfig

        return ProdConfig
