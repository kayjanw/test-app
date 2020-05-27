import io
import pandas as pd

from flask import request, send_file

from components.helper import decode_df


def register_routes(app):
    @app.server.route('/download_df/', methods=['POST'])
    def download_result():
        df_ser = request.form.get('result')
        df = decode_df(df_ser)
        if len(df) > 0:
            buf = io.BytesIO()
            excel_writer = pd.ExcelWriter(buf, engine="xlsxwriter")
            df.to_excel(excel_writer, sheet_name="Sheet1")
            excel_writer.save()
            excel_data = buf.getvalue()
            buf.seek(0)
            return send_file(
                buf,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                attachment_filename="result.xlsx",
                as_attachment=True,
                cache_timeout=0
            )

    @app.server.route('/<path:path>')
    def serve_sphinx_docs(path='index.html'):
        return app.server.send_static_file(path)
