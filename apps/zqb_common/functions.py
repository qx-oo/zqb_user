# -*- coding: utf-8 -*-

# version: 1.0
# author: shawn

import qiniu
from django.conf import settings
import uuid
import urlparse


class SaveImage(object):
    '''
    Upload image and return image url
    '''
    def __init__(self, file_stream, file_name=None, file_type=".png"):
        '''
        binary image upload
        '''
        if not file_name:
            file_name = str(uuid.uuid1()) + file_type
        q = qiniu.Auth(settings.QINIU_ACCESSKEY, settings.QINIU_SECRETKEY)
        token = q.upload_token(settings.QINIU_BUCKET_NAME, file_name, 3600)
        ret, info = qiniu.put_data(token, file_name, file_stream)
        if info.status_code != 200:
            raise Exception("Upload fail.")
        self.url = ret['key']

    def get_image_url(self):
        '''
        return upload url
        '''
        return urlparse.urljoin(settings.QINIU_IMAGE_URL, self.url)
