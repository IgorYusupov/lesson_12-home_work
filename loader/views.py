import logging

from flask import Blueprint, request, render_template


loader_blueprint = Blueprint("loader_blueprint", __name__, template_folder="templates")

# Добавили файл, в который пишем логи
logging.basicConfig(filename="basic.log", level=logging.INFO)


@loader_blueprint.route("/post", methods=["GET"])
def page_form():

    return render_template("post_form.html")


@loader_blueprint.route("/post", methods=["POST"])
def page_create_posts():

    picture = request.files.get("picture", None)
    content = request.form.get("content", "")
    posts_handler = PostsHandler("posts.json")

    if not picture or not content:
        logging.info("Данные не загружены")
        return "Данные не загружены"
    try:
        picture_path = save_uploaded_picture(picture)
    except PictureWrongTypeError:
        logging.info("Неверный тип файла")
        return "Неверный типа файла"
    except FileNotFoundError:
        return "Не удалось сохранить файл, путь не найден"

    picture_url = "/"+picture_path
    post_object = {"pic": picture_url, "content": content}

    try:
        posts_handler.add_post(post_object)
    except DataLayerError:
        return "Не удалось добавить пост, ошибка записи в список постов"

    return render_template("post_uploaded.html", picture_url=picture_url, content=content)
