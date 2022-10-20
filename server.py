 
def parse_command_line_args():
    parser = argparse.ArgumentParser(
        description='Webservice to detect intracrancial hemorrhages.')

    parser.add_argument('--model', type=str,
                        help='Path to the trained model.')

    parser.add_argument('--input_size', type=int, default=224,
                        help='Dimensions of the input image.')

    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='server ip address.')

    parser.add_argument('--port', type=str, default='5000',
                        help='port of the service.')

    args = parser.parse_args()
    return args


def request_has_file(request_files):
    return not(
        (request_files is None) or
        (len(request_files) == 0) or
        (request_files['file']) is None)


def save_file(received_request,
              upload_folder: str,
              allowed_extensions: List[str]
              ) -> Dict:

    print('1:', received_request)
    print('2:', received_request.files)

    # check if the post request has the file field
    if not request_has_file(received_request.files):
        return {
            "file_path": '',
            "success": False,
            "error_msg": 'request without attached file.'
        }

    file = received_request.files['file']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    extension = str(".".join(Path(file.filename).suffixes)).lower()

    ext_valid = extension in allowed_extensions

    if (file.filename == '') or (not ext_valid):
        return {
            # "file_path": '',
            "extension": extension,
            "success": False,
            "error_msg": 'invalid file.'
        }

    unique_id = str(uuid4())
    file_path = f"{upload_folder}/{unique_id}{extension}"
    file.save(file_path)
    
    if extension == ".zip":
        extract_case(
            file_path,
            upload_folder,
            unique_id
        )


    return {
        "file_path": file_path,
        "extension": extension,
        "uuid": unique_id,
        "success": True,
        "error_msg": ''
    }


##########################
# ENDPOINTS
##########################
@app.route('/ich/dcm/', methods=["POST"])
def upload_file():
    result = save_file(
        request,
        app.config['upload_folder'],
        app.config['allowed_image_extensions'].union(
            app.config['allowed_compressed_extensions'])
    )

    if not result['success']:
        return make_response(json.dumps({'error': result['error_msg']}), 400)

    if result['extension'] == ".zip":
        return make_response(json.dumps({
            "app": "ich",
            "uuid": result["uuid"],
        }), 201)


    return make_response(json.dumps({
        "app": "ich",
        "uuid": result["uuid"],
        "file": f"http://{request.host}/data/dicom/{result['uuid']}{result['extension']}",
    }), 201)


@app.route('/data/dicom/<filename>', methods=["GET"])
def show_uploaded_img(filename):
    return send_from_directory(
            app.config['upload_folder'],
            filename,
            as_attachment=True)


@app.route('/ich/models/latest/predict', methods=["POST"])
def add_dcm_to_queue():
    case_id = request.json['case']
    threshold = request.json['threshold']
    if isinstance(case_id, list):
        missing_dicoms = list()
        for dicom in case_id:
            dicom['file_path'] = f"{app.config['upload_folder']}/{dicom['dicom']}.dcm"
            if not Path(dicom['file_path']).is_file():
                missing_dicoms.append(dicom['dicom'])

        if len(missing_dicoms) > 0:
            result = json.dumps({
                "status": 400,
                "message": "The following images were not found",
                "missing_images": missing_dicoms
            })
            return make_response(result, 400)

        task = process_file.delay(
            case_id, app.config['model'], app.config['input_size'], threshold)
        
        result = {
            "uuid": task.id,
            "case": case_id,
            "threshold": threshold,
            "status": "SUCCESS"
        }
    elif isinstance(case_id, str):
        file_list = list()
        files = Path(f"{app.config['upload_folder']}/{case_id}/").rglob("*.dcm")
        for file in files:
            file_list.append({ "file_path": str(file) })

        task = process_file.delay(
            file_list, app.config['model'], app.config['input_size'], threshold)
        
        result = {
            "uuid": task.id,
            "case": case_id,
            "threshold": threshold,
            "status": "SUCCESS"
        }

    return make_response(result, 200)


@app.route('/ich/predictions/<task_id>/score', methods=["GET"])
@app.route('/ich/predictions/<task_id>/score/<raw>', methods=["GET"])
def get_prediction(task_id, raw=None):
    response = dict()
    task = AsyncResult(task_id, app=papp)

    if task.ready():
        predictions = task.get()
        sum = 0
        num_images = len(predictions)

        for dicom in predictions:
            dicom.pop('file_path')
            sum += dicom['prediction']

        if raw:
            return make_response(json.dumps(predictions), 200)

        result = {
            "score": {
                "brain_hemorrhage": 10*(sum/num_images)
            }
        }
        return make_response(json.dumps(result), 200)

    else:
        return make_response({"status": task.state}, 400)


##########################
# STARTING POINT
##########################

if __name__ == "__main__":
    args = parse_command_line_args()

    # app.config['device'] = get_device()
    # app.config['model'] = load_model(args.model, app.config['device'])
    app.config['model'] = args.model
    app.config['upload_folder'] = "./tmp_uploads/"
    # app.config['allowed_image_extensions'] = {'.png', '.dcm'}
    app.config['allowed_image_extensions'] = {'.dcm'}
    app.config['allowed_compressed_extensions'] = {'.zip'}
    app.config['input_size'] = args.input_size
    app.config['host'] = args.host
    app.config['port'] = args.port

    mkdirs_if_not_exists(Path(app.config['upload_folder']))

    #######################
    # From this point onwards, the endpoints will be receiving messsages.
    #######################
    print(f" * Model: {args.model}.")
    print(f" * Starting server at http://{args.host}:{args.port}.")
    app.run(host=args.host, port=args.port)