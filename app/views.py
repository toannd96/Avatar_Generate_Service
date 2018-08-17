import os
import errno
import uuid
import magic
import shutil
from flask import request, make_response, g
from werkzeug import secure_filename
from flask_restful import (reqparse, Resource, fields, marshal_with, marshal)
from config import Config
from app import db, create_app
from models import User, Picture
from urlparse import urlparse
from PIL import Image

info_user = {'email': fields.String, 'email_md5': fields.String}

uri = {'uri': fields.Url('user', absolute=True)}


def allowed_file(filename):
    return '.' in filename and \
        filename.split('.')[-1].lower() in Config.ALLOWED_EXTENSIONS


def mkdir_upload_image(upload_image):
    try:
        os.makedirs(upload_image)
        return True, upload_image

    except OSError as e:
        if e.errno == errno.EEXIST:
            return True, upload_image
        else:
            return False, str(e)

    except Exception as e:
        return False, str(e)


def mkdir_edit_folder_default(edit_folder_default):
    try:
        os.makedirs(edit_folder_default)
        return True, edit_folder_default

    except OSError as e:
        if e.errno == errno.EEXIST:
            return True, edit_folder_default
        else:
            return False, str(e)

    except Exception as e:
        return False, str(e)


def mkdir_edit_folder_name_pic(edit_folder_name_pic):
    try:
        os.makedirs(edit_folder_name_pic)
        return True, edit_folder_name_pic

    except OSError as e:
        if e.errno == errno.EEXIST:
            return True, edit_folder_name_pic
        else:
            return False, str(e)

    except Exception as e:
        return False, str(e)


def generator_pic_default():
    size = request.args.get('s')
    edit_folder_default = os.path.join(Config.EDIT_IMAGE, 'DEFAULT')
    path_picture_default = os.path.abspath(
        os.path.join('DEFAULT_IMAGE', 'default.jpg'))
    with open(path_picture_default) as f:
        file_content = f.read()
    response = make_response(file_content)
    response.headers["Content-Disposition"] = "inline; filename=default.jpg"
    response.headers['Content-Type'] = 'image/png'
    if size is None:
        return response

    if size != '':
        if size.isdigit():
            base_width = int(size)
            if base_width == 0:
                return {
                    'status': '500',
                    'message': 'Size must be different 0'
                }, 500

            if base_width > 1000:
                base_width = 1000
            pic = Image.open(path_picture_default)
            pic = pic.resize((base_width, base_width), Image.ANTIALIAS)
            name_picture_edit = "default-{}.jpg".format(base_width)
            ok, edit_folder_default = mkdir_edit_folder_default(
                edit_folder_default)
            if not ok:
                return {
                    'status': '500',
                    'message': 'System error, can not create folder'
                }, 500

            picture_edit = pic.save(
                os.path.join(edit_folder_default, name_picture_edit))
            path_picture_edit = os.path.abspath(
                os.path.join(edit_folder_default, name_picture_edit))

            with open(path_picture_edit) as f:
                file_content = f.read()
            response = make_response(file_content)
            response.headers[
                "Content-Disposition"] = "inline; filename={}".format(
                    name_picture_edit)
            response.headers['Content-Type'] = 'image/png'
            return response
        return {'status': '500', 'message': 'size must be an integer'}, 500

    return response


def generator_pic_user(picture):
    size = request.args.get('s')
    edit_folder_name_pic = os.path.join(Config.EDIT_IMAGE,
                                        picture.name_picture)
    path_picture = os.path.abspath(
        os.path.join(Config.UPLOAD_IMAGE, picture.name_picture))
    with open(path_picture) as f:
        file_content = f.read()
    response = make_response(file_content)
    response.headers["Content-Disposition"] = "inline; filename={}".format(
        picture.name_picture)
    response.headers['Content-Type'] = 'image/png'
    if size is None:
        return response

    if size != '':
        if size.isdigit():
            base_width = int(size)
            if base_width == 0:
                return {
                    'status': '500',
                    'message': 'Size must be different 0'
                }, 500

            if base_width > 1000:
                base_width = 1000
            pic = Image.open(path_picture)
            pic = pic.resize((base_width, base_width), Image.ANTIALIAS)
            name_picture_edit = str(
                base_width) + '-' + picture.name_picture + '.png'
            ok, edit_folder_name_pic = mkdir_edit_folder_name_pic(
                edit_folder_name_pic)
            if not ok:
                return {
                    'status': '500',
                    'message': 'System error, can not create folder'
                }, 500

            picture_edit = pic.save(
                os.path.join(edit_folder_name_pic, name_picture_edit))
            path_picture_edit = os.path.abspath(
                os.path.join(edit_folder_name_pic, name_picture_edit))

            with open(path_picture_edit) as f:
                file_content = f.read()
            response = make_response(file_content)
            response.headers[
                "Content-Disposition"] = "inline; filename={}".format(
                    name_picture_edit)
            response.headers['Content-Type'] = 'image/png'
            return response
        return {'status': '500', 'message': 'size must be an integer'}, 500

    return response


class PictureUpload(Resource):
    def post(self):
        upload_image = Config.UPLOAD_IMAGE
        if 'file' not in request.files:
            return {'status': '400', 'message': 'No file found'}, 400

        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(str(uuid.uuid4()))

            ok, upload_image = mkdir_upload_image(upload_image)
            if not ok:
                return {'status': '500', 'message': 'System error'}, 500

            file_path = os.path.join(upload_image, filename)
            try:
                file.save(file_path)
                if magic.from_file(
                        file_path, mime=True) in Config.CONTENT_TYPE:
                    user = User.query.filter(User.email == g.email).first()
                    picture = Picture.query.join(User).filter(
                        Picture.user_id == user.id).first()
                    if not picture:
                        picture = Picture(
                            name_picture=filename, user_id=user.id)
                        db.session.add(picture)
                        db.session.commit()
                        return {
                            'status':
                            '200',
                            'message':
                            "upload image {} success".format(
                                picture.name_picture)
                        }, 200

                    os.remove(os.path.join(upload_image, picture.name_picture))
                    shutil.rmtree(
                        os.path.join(
                            os.path.join(Config.EDIT_IMAGE,
                                         picture.name_picture)))
                    db.session.delete(picture)
                    db.session.commit()

                    picture = Picture(name_picture=filename, user_id=user.id)
                    db.session.add(picture)
                    db.session.commit()

                    return {
                        'status':
                        '200',
                        'message':
                        "upload image {} success".format(picture.name_picture)
                    }, 200

                else:
                    os.remove(file_path)
                    return {
                        'status':
                        '404',
                        'message':
                        "Please upload file format ({})".format(
                            (', ').join(Config.ALLOWED_EXTENSIONS))
                    }, 404

            except Exception as e:
                return {
                    'status': '500',
                    'message': 'System error, unable to upload file'
                }, 500

            else:
                return {
                    'status':
                    '404',
                    'message':
                    "Please upload file format ({})".format(
                        (', ').join(Config.ALLOWED_EXTENSIONS))
                }, 404
        else:
            return {
                'status':
                '404',
                'message':
                "Please upload file format ({})".format(
                    (', ').join(Config.ALLOWED_EXTENSIONS))
            }, 404


class GetCookies(Resource):
    @marshal_with(info_user)
    def post(self):
        user = User.query.filter(User.email == g.email).first()
        if not user:
            user = User(email=g.email)
            user.set_email(g.email)
            db.session.add(user)
            db.session.commit()
        return user, 200


class PictureGenerator(Resource):
    def get(self, email_md5):
        md5 = urlparse(request.url).path.split('/')[2]
        user = db.session.query(User).filter(User.email_md5 == md5).first()
        if not user:
            return generator_pic_default()

        picture = Picture.query.join(User).filter(
            Picture.user_id == user.id).first()
        if not picture:
            return generator_pic_default()

        return generator_pic_user(picture)
