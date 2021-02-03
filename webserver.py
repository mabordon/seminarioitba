from flask import Flask, render_template
from itbatools import get_dir_property_hook

webserver_info = get_dir_property_hook()


app = Flask(
    __name__,
    template_folder=webserver_info.templates,
    static_folder=webserver_info.static_folder,
)


@app.route("/")
@app.route("/index")
def get_images():
    return render_template(
        "index.html",
        serie_temperaturas=f"{webserver_info.static_folder}/{webserver_info.images['serie_temperaturas']}",
        descomposicion=f"{webserver_info.static_folder}/{webserver_info.images['descomposicion']}",
        ajuste_normal=f"{webserver_info.static_folder}/{webserver_info.images['ajuste']}",
    )


# Metodo para arrancar el webserver en el puerto 8000 que es el que esta configurado en wservconfig.json
def start_server():
    app.run(host="localhost", port=webserver_info.webserver_port)


if __name__ == "__main__":
    start_server()
