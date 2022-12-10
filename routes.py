from flask import request, send_file

from components.helper import (
    create_json_from_dict,
    decode_df,
    decode_dict,
    get_excel_demo,
    get_excel_from_df,
)


def register_routes(app):
    @app.server.route("/download_df/", methods=["POST"])
    def download_result():
        df_ser = request.form.get("result")
        df = decode_df(df_ser)
        if len(df) > 0:
            buf = get_excel_from_df(df)
            return send_file(
                buf,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                attachment_filename="result.xlsx",
                as_attachment=True,
                cache_timeout=0,
            )

    @app.server.route("/download_demo/", methods=["POST"])
    def download_demo():
        buf = get_excel_demo()
        return send_file(
            buf,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            attachment_filename="demo.xlsx",
            as_attachment=True,
            cache_timeout=0,
        )

    @app.server.route("/download_dict/", methods=["POST"])
    def download_dictionary():
        d_ser = request.form.get("result")
        d = decode_dict(d_ser)
        if d:
            buf = create_json_from_dict(d)
            return send_file(
                buf,
                mimetype="application/json",
                attachment_filename="wnrs_progress.json",
                as_attachment=True,
                cache_timeout=0,
            )

    @app.server.route("/<path:path>")
    def serve_sphinx_docs(path="index.html"):
        return app.server.send_static_file(path)
