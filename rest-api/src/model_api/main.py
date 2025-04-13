from model_api.app import create_app
import sys

if __name__ == "__main__":
    config_name = sys.argv[1]
    create_app(config_name=config_name).run(debug=True)
