from flask import Flask, make_response, jsonify, request, send_from_directory
import os
import log as log
from datetime import datetime

thispath = os.path.dirname(os.path.realpath(__file__))

APPNAME = "parameter-logger"
VERSION = "v0.1"
LOGPATH = f"{thispath}/var/log/"
LOGFILE = f"{datetime.now().strftime('%Y%m%d')}.log"

log.file_init (LOGPATH, LOGFILE)


app = Flask(__name__)


# Functions


def get_from_json (json, value):
    """
    :param json:
    :param value:
    :return:
    Check whether a value exists in a json blob """

    if value in json.keys():
            return json[value]
    else:
        return ""



@app.route('/', methods=['GET'])
def api_root_page():

    log.entry_add(LOGPATH, LOGFILE, "*** Connection [Begin] ***")
    log.entry_add(LOGPATH, LOGFILE, f"referer: {request.headers.get('Referer')}")

    if request.args:

        if 'cookie' in request.args:
            log.entry_add(LOGPATH, LOGFILE, "[Cookie Parameter Found]")

        data = request.args.to_dict()

        for (p) in request.args:

            log.entry_add (LOGPATH, LOGFILE, f"{p}:{data[p]}")
            log.entry_add(LOGPATH, LOGFILE, "*** Connection [End] ***")

        return (make_response(jsonify('server status', 'ok'), 200))

    log.entry_add(LOGPATH, LOGFILE, f"*** No Parameters Logged [End]  ***")
    return (make_response(jsonify('error', 'bad request'), 400))



@app.route('/log/list', methods=['POST'])
def api_log_list_post():

    log.entry_add(LOGPATH, LOGFILE, f"*** Log/List Request [End / Success] ***")
    return (make_response(jsonify('files', log.file_list(LOGPATH), 200)))



@app.route('/log/show', methods=['POST'])
def api_log_show_post():

    log.entry_add(LOGPATH, LOGFILE, f"*** Log/Show Request [Begin] ***")
    postdata = request.json

    if postdata:

        logfile = f"{get_from_json(postdata, 'file')}"
        logfile = logfile.replace('..','')
        logfile = logfile.replace('/', '')
        log.entry_add(LOGPATH, LOGFILE, f"*** Log/Show Request [Filename] [{logfile}] ***")
        # NB - the above line generates an xss through injection into the log... i think :)


        if not logfile:
            log.entry_add(LOGPATH, LOGFILE, f"*** Log/Show Request [End / Fail] ***")
            return make_response(jsonify({'error': 'bad request'}), 400)

        # check requested file exists
        files = log.file_list(LOGPATH)

        lfexists = False
        for f in files:

            lf = f['file']
            if (lf) == logfile:
                lfexists = True
                break

        if lfexists:

            log.entry_add(LOGPATH, LOGFILE, f"*** Log/Show Request [End / Success] ***")
            return (send_from_directory(LOGPATH, logfile, mimetype='text\plain', as_attachment=True))

        else:
            log.entry_add(LOGPATH, LOGFILE, f"*** Log/Show Request [End / Fail] ***")
            return (make_response(jsonify({'error': 'file not found'}), 404))


    else:
        log.entry_add(LOGPATH, LOGFILE, f"*** Log/Show Request [End / Fail] ***")
        return (make_response(jsonify({'error': 'bad request'}), 400))


# Main Application Loop
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)