import logging

from flask import Flask, send_from_directory


# Импортируем блюпринты из их пакетов
from main.views import main_blueprint
from loader.views import loader_blueprint

import loggers

app = Flask(__name__)

app.config["POST_PATH"] = "data/posts.json"
app.config["UPLOAD_FOLDER"] = "uploads/images"

# Регистрируем первый блюпринт
app.register_blueprint(main_blueprint)
# Регистрируем второй блюпринт
app.register_blueprint(loader_blueprint)

loggers.create_logger()

logger = logging.getLogger("basic")


@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path)


logger.info("Приложение запускается")

app.run(debug=True)
