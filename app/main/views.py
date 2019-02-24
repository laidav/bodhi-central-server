from . import main


@main.route('/')
def index():
    return '<h1>Hello World Basic app structure!</h1>'
