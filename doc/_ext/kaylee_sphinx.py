
def setup(app):
    app.add_crossref_type(
        directivename = "config",
        rolename      = "config",
        indextemplate = "pair: %s; config",
    )
