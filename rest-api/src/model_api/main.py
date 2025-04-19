from model_api.app import create_app
import sys

if __name__ == "__main__":
    config_name = sys.argv[1]
    create_app(config_name=config_name).run(host="0.0.0.0", debug=True)
