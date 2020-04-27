# -*- coding: utf-8 -*-
from imgurpython import ImgurClient
from helpers import read_json
from tqdm import tqdm

import requests
import io
import os


class ImgurDownloader:
    """This class downloads images from imgur website.

    Can handle albums and solo images.

    >>> from imgur import ImgurDownloader
    >>> ImgurDownloader('https://imgur.com/a/nUDhP', 'amanda-cerny').__call__()

    """
    def __init__(self, imgur_url, filename):
        self.credentials = read_json('settings.json')
        self.imgur_url = imgur_url
        self.filename = filename
        self.path = os.path.abspath('../data/{}'.format(self.filename))
        self.checkpoint = 0

        self.client = self.authenticate()
        self.id, self.is_album = self.check_and_parse_url()
        self.check_directory()

    # used in __init__
    def authenticate(self):
        """This function authenticates into imgur api.

        Returns
        -------
        ImgurClient: imgurpython.client.ImgurClient
            The imgur connection instance.

        """
        return ImgurClient(**self.credentials)

    # used in __init__
    def check_and_parse_url(self):
        """This function checks if the given url is an album or a solo image.

        Returns
        -------
        spliced_url : str
            Solo image/Album id.

        True, False : bool
            True if is an album, False otherwise.

        """
        spliced_url = self.imgur_url.split('/')
        if spliced_url[3] is 'a':
            return spliced_url[-1], True
        return spliced_url[-1].split('.')[0], False

    # used in __init__
    def check_directory(self):
        """This function checks if on the given path the directory exists. If
        exists add it into the self.checkpoint the index of the most recent
        file - For not overwriting images. Otherwise, create the directory.

        Returns
        -------

        """
        if os.path.exists(self.path):
            try:
                self.checkpoint += len(os.listdir(self.path))
            except TypeError:
                self.checkpoint += 0
            except IndexError:
                self.checkpoint += 0
        else:
            os.makedirs(self.path)

    # used in download_image_list
    @staticmethod
    def requesting_images(url_):
        """Make GET submissions on the given url.

        Parameters
        ----------
        url_ : str
            Image url.

        Returns
        -------
        requests : bytes
            The website content.

        """
        return requests.get(url_).content

    # used in download_image_list
    def filename_format(self, idx, extension):
        """This function formats the filepath by adding its abspath and
        extension.

        Parameters
        ----------
        idx : int
            The image index - For not overwriting.
        extension : str
            Image extension.

        Returns
        -------
        formatted_filepath : str
            The formatted filepath.

        """
        return self.path + '/' + self.filename + '-{}.{}'. \
            format(idx + self.checkpoint, extension)

    # used in download_image_list
    @staticmethod
    def get_extension(img):
        """This function gets the image extension (jpg, png and others).

        Parameters
        ----------
        img : imgurpython.imgur.models.image.Image()
            The imgur image.

        Returns
        -------
        ext : str
            The image extension

        """
        return img.link.split('.')[-1]

    # used in __call__
    def get_image_list(self):
        """This function retrieves the list of images from imgur url.

        Returns
        -------
        img_list : iterator
            The images list.

        """
        if self.is_album:
            return self.client.get_album_images(self.id)
        return [self.client.get_image(self.id)]

    # used in __call__
    def download_image_list(self, image_list):
        """This function iterates through the image list.

        Parameters
        ----------
        image_list : iterator
            The images list.

        Returns
        -------

        """
        for idx, img in tqdm(enumerate(image_list, 1), total=len(image_list)):
            filename = self.filename_format(idx, self.get_extension(img))
            image_bytes = self.requesting_images(img.link)

            with io.open(filename, 'wb') as file:
                file.write(image_bytes)

    def __call__(self, *args, **kwargs):
        self.download_image_list(self.get_image_list())


if __name__ == '__main__':
    list_ = [
        'TfPx5mn',
    ]
    for _ in list_:
        ImgurDownloader('https://imgur.com/a/{}'.format(_),
                        'lis-giolito').__call__()
