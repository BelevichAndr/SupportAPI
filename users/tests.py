from typing import Optional

from django.test import TestCase
from rest_framework.test import APITestCase
class MyTestCase(APITestCase):

    def test_some_stuff(self, arg1: Optional[str]=None, arg2: Optional[int]=None):
        print('Test is working')
        print(arg1, arg2)

