import unittest
import helper
import json

class ListTestCase(unittest.TestCase):
    def setUp(self):
        # Create User w/ List
        helper.create_user(username='unittest1', password='unittest1')
        helper.lists_create(username='unittest1', password='unittest1', name='test', description='test')
        
        # Create User w/o List
        helper.create_user(username='unittest2', password='unittest2')

    def test_lists_get_non_empty(self):
        response = helper.lists_get(username='unittest1', password='unittest1')
        print(json.dumps(response.json(), indent=2))

        assert response.json()[0]['name'] == 'test'
        assert response.json()[0]['description'] == 'test'

    def test_lists_get_empty(self):
        response = helper.lists_get(username='unittest2', password='unittest2' )
        assert response.json() == []

    def test_lists_create(self):
        response = helper.lists_create(username='unittest1', password='unittest1', name='test2', description='test2')
        assert response.status_code == 200
        helper.lists_delete(username='unittest1', password='unittest1',name='test2')


    #def test_lists_delete(self):
    #    assert helper.lists_delete(username='unittest1', password='unittest1', name='test').json() == True

    def tearDown(self):
        # Delete List
        helper.lists_delete(username='unittest1', password='unittest1', name='test')

        # Delete Users
        helper.delete_user(username='unittest1', password='unittest1')


if __name__ == '__main__':
    ltc = ListTestCase()
    ltc.setUp()

    ltc.test_lists_get_non_empty()
    #ltc.test_lists_get_empty()
    #ltc.test_lists_get_by_up_id()
    #ltc.test_lists_get_empty_by_up_id()
    #ltc.test_lists_create()
    #ltc.test_lists_create_by_up_id()
    #ltc.test_lists_delete()
    #ltc.test_lists_delete_by_up_id
    #ltc.tearDown()
