import io
import json
import pandas as pd

from flask import request, send_file

from components.helper import decode_df, decode_dict


def register_routes(app):
    @app.server.route('/download_df/', methods=['POST'])
    def download_result():
        df_ser = request.form.get('result')
        df = decode_df(df_ser)
        if len(df) > 0:
            buf = io.BytesIO()
            excel_writer = pd.ExcelWriter(buf, engine='xlsxwriter')
            df.to_excel(excel_writer, sheet_name='Sheet1', index=False)
            excel_writer.save()
            excel_data = buf.getvalue()
            buf.seek(0)
            return send_file(
                buf,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                attachment_filename='result.xlsx',
                as_attachment=True,
                cache_timeout=0
            )

    @app.server.route('/download_demo/', methods=['POST'])
    def download_demo():
        df_ser = request.form.get('demo')
        df = decode_df(df_ser)
        if len(df) > 0:
            buf = io.BytesIO()
            excel_writer = pd.ExcelWriter(buf, engine='xlsxwriter')
            df.to_excel(excel_writer, sheet_name='Sheet1', index=False)

            # Set style
            worksheet = excel_writer.sheets['Sheet1']
            workbook = excel_writer.book
            cell_format = workbook.add_format({'bold': True, 'font_color': 'red'})
            worksheet.write('A1', 'Name', cell_format)
            worksheet.write('B1', 'Email (Optional)', cell_format)

            excel_writer.save()
            excel_data = buf.getvalue()
            buf.seek(0)
            return send_file(
                buf,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                attachment_filename='demo.xlsx',
                as_attachment=True,
                cache_timeout=0
            )

    @app.server.route('/download_dict/', methods=['POST'])
    def download_dictionary():
        d_ser = request.form.get('result')
        d = decode_dict(d_ser)
        if d:
            d_save = dict(
                list_of_deck=d['list_of_deck'],
                index=d['wnrs_game_dict']['index'],
                pointer=d['wnrs_game_dict']['pointer'],
            )
            d_save_ser = io.BytesIO(json.dumps(d_save).encode())
            return send_file(
                d_save_ser,
                mimetype='application/json',
                attachment_filename="wnrs_progress.json",
                as_attachment=True,
                cache_timeout=0
            )

    @app.server.route('/<path:path>')
    def serve_sphinx_docs(path='index.html'):
        return app.server.send_static_file(path)
