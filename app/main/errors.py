from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    return "<h1>Page not found</h1>"


@main.app_errorhandler(500)
def internal_server_error(e):
    return "<h1>Internal Server Error</h1>"
