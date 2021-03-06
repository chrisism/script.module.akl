import unittest, os

import logging

from lib.akl.utils import text, io

logger = logging.getLogger(__name__)
logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG) 

class Test_utilstests(unittest.TestCase):
  
    def test_when_getting_url_extension_it_returns_the_correct_extension(self):

        # arrange
        url = 'http://wwww.somesite.com/with/somepicture.jpg'
        expected = 'jpg'

        # act
        actual = io.get_URL_extension(url)

        # assert
        assert actual == expected

    def test_when_getting_url_extension_of_an_url_without_an_extension_it_will_return_empty(self):

        
        # arrange
        url = 'http://wwww.somesite.com/with/somepicture'
        expected = ''

        # act
        actual = io.get_URL_extension(url)

        # assert
        assert actual == expected
        
    def test_when_getting_image_url_extension_it_returns_the_correct_extension(self):

        # arrange
        url = 'http://wwww.somesite.com/with/somepicture.png'
        expected = 'png'

        # act
        actual = io.get_image_URL_extension(url)

        # assert
        assert actual == expected
                      
    def test_when_getting_image_url_extension_of_an_url_without_an_extension_it_will_return_jpg(self):

        # arrange
        url = 'http://wwww.somesite.com/with/somepicture'
        expected = 'jpg'

        # act
        actual = io.get_image_URL_extension(url)

        # assert
        assert actual == expected


if __name__ == '__main__':
    unittest.main()
