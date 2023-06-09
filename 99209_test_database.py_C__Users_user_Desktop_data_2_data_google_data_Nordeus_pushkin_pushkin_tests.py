'''
The MIT License (MIT)
Copyright (c) 2016 Nordeus LLC

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import pytest
from pushkin.database import database
import datetime
from pushkin import context

from pushkin import test_config_ini_path
context.setup_configuration(test_config_ini_path)

@pytest.fixture
def setup_database():
    database.init_db()
    database.create_database()



def test_devices(setup_database):
    database.process_user_login(login_id=12345, language_id=7, platform_id=1, device_id='qwe', device_token='123',
                                application_version=1007)
    assert list(database.get_device_tokens(login_id=12345)) == [(1, '123')]
    database.process_user_login(login_id=12345, language_id=7, platform_id=1, device_id=None, device_token='123',
                                application_version=1007)
    database.process_user_login(login_id=12345, language_id=7, platform_id=1, device_id='qwe', device_token=None,
                                application_version=1007)
    assert list(database.get_device_tokens(login_id=12345)) == [(1, '123')]
    database.process_user_login(login_id=12345, language_id=7, platform_id=1, device_id='qwe', device_token='124',
                                application_version=1007)
    assert list(database.get_device_tokens(login_id=12345)) == [(1, '124')]
    database.process_user_login(login_id=12345, language_id=7, platform_id=1, device_id='qwr', device_token='125',
                                application_version=1007)
    assert list(database.get_device_tokens(login_id=12345)) == [(1, '124'), (1, '125')]


def test_message(setup_database):
    # user using serbian language
    database.process_user_login(login_id=12345, language_id=7, platform_id=1, device_id='qwe', device_token='123',
                                application_version=1007)

    # message with english only translation
    message_1 = database.add_message(message_name='test', language_id=1, message_title='title en',
                                      message_text='text en')
    localized_message = database.get_localized_message(login_id=12345, message_id=message_1.message_id)
    assert localized_message.message_title == 'title en'
    assert localized_message.message_text == 'text en'
    assert localized_message.language_id == 1
    assert localized_message.message.screen == ''

    # adding other translation different from serbian
    message_2 = database.add_message(message_name='test', language_id=0, message_title='title other',
                                      message_text='text other')
    localized_message = database.get_localized_message(login_id=12345, message_id=message_2.message_id)
    assert localized_message.message_title == 'title en'
    assert localized_message.message_text == 'text en'
    assert localized_message.language_id == 1
    assert localized_message.message.screen == ''

    # adding serbian translation
    message_3 = database.add_message(message_name='test', language_id=7, message_title='title sr',
                                      message_text='text sr')
    localized_message = database.get_localized_message(login_id=12345, message_id=message_3.message_id)
    assert localized_message.message_title == 'title sr'
    assert localized_message.message_text == 'text sr'
    assert localized_message.language_id == 7
    assert localized_message.message.screen == ''

    # message with no english neither serbian translation
    bad_message = database.add_message(message_name='test_bad', language_id=0, message_title='title bad',
                                      message_text='text bad')
    localized_message = database.get_localized_message(login_id=12345, message_id=bad_message.message_id)
    assert localized_message is None

    # user doesn't exist
    localized_message = database.get_localized_message(login_id=12346, message_id=message_3.message_id)
    assert localized_message is None

    # delete a message
    database.delete_message(message_1.message)
    assert database.get_message('test') is None

def test_user(setup_database):
    login = database.upsert_login(12345, 7)
    assert login == database.get_login(12345)

    device = database.upsert_device(login_id=login.id, platform_id=1, device_id='qwe', device_token='123',
                                    application_version=1001, unregistered_ts=datetime.datetime.now())
    assert device == login.devices[0]

    database.delete_device(device)
    assert len(login.devices) == 0

    database.delete_login(login)
    assert database.get_login(12345) is None

def test_unregistered_device(setup_database):
    login = database.upsert_login(12345, 7)
    device = database.upsert_device(login_id=login.id, platform_id=1, device_id='qwe', device_token='123',
                                    application_version=1001)
    assert len(database.get_device_tokens(12345).all()) == 1

    database.update_unregistered_devices([{'login_id': device.login_id, 'device_token': device.device_token}])
    assert len(database.get_device_tokens(12345).all()) == 0
