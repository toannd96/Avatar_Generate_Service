import os
import unittest
import tempfile
import shutil
from flask_testing import TestCase
from app import create_app, db
from app.models import User, Picture
from app.views import (allowed_file, mkdir_upload_image,
                       mkdir_edit_folder_default, mkdir_edit_folder_name_pic)
from config import Config, TestingConfig
from hashlib import md5


class TestAllowedFile(unittest.TestCase):
    """
    Kiem tra kieu duoi file upload
    """

    def test_type_file(self):
        self.assertFalse(allowed_file("test"))
        self.assertFalse(allowed_file("test.txt"))
        self.assertTrue(allowed_file("test.png"))
        self.assertTrue(allowed_file("test.jpg"))
        self.assertTrue(allowed_file("test.jpeg"))


class TestUploadImg(unittest.TestCase):
    """
    Kiem tra ham tao folder UPLOAD_IMAGE
    """

    def test_mkdir_upload_image(self):
        upload_image = os.path.join(self.path, Config.UPLOAD_IMAGE)
        result, folder_path = mkdir_upload_image(upload_image)
        self.assertTrue(result)
        self.assertEqual(folder_path, upload_image)

    def setUp(self):
        self.path = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.path)


class TestEditImgDefault(unittest.TestCase):
    """
    Kiem tra ham tao folder EDIT_IMAGE/DEAULT
    """

    def test_mkdir_edit_image_default(self):
        edit_folder_default = os.path.join(
            self.path, os.path.join(Config.EDIT_IMAGE, 'DEFAULT'))
        result, folder_path = mkdir_edit_folder_default(edit_folder_default)
        self.assertTrue(result)
        self.assertEqual(folder_path, edit_folder_default)

    def setUp(self):
        self.path = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.path)


class TestBase(TestCase):
    def create_app(self):
        app = create_app()
        app.config.update(SQLALCHEMY_DATABASE_URI=
                          'mysql://dt_admin:dt_admin@localhost/avatar_test')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestModels(TestBase):
    """
    Kiem tra so luong ban ghi trong bang User, Picture
    """

    def test_user_model(self):
        user = User(
            email="test@gmail.com",
            email_md5=md5('test@gmail.com'.encode('utf-8')).hexdigest())
        db.session.add(user)
        db.session.commit()

        self.assertEqual(User.query.count(), 1)

    def test_picture_model(self):
        pic = Picture(name_picture="test")
        db.session.add(pic)
        db.session.commit()

        self.assertEqual(Picture.query.count(), 1)


class TestEditByNamePic(TestCase):
    """
    Kiem tra ham tao folder EDIT_IMAGE/test
    """

    def create_app(self):
        app = create_app()
        app.config.update(SQLALCHEMY_DATABASE_URI=
                          'mysql://dt_admin:dt_admin@localhost/avatar_test')
        return app

    def test_mkdir_edit_image_by_name(self):
        pic = Picture(name_picture="test")
        db.session.add(pic)
        db.session.commit()

        edit_folder_name_pic = os.path.join(
            self.path, os.path.join(Config.EDIT_IMAGE, pic.name_picture))
        result, folder_path = mkdir_edit_folder_name_pic(edit_folder_name_pic)
        self.assertTrue(result)
        self.assertEqual(folder_path, edit_folder_name_pic)

    def setUp(self):
        db.create_all()
        self.path = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.path)
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
