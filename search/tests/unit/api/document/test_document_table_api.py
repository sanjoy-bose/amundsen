import unittest

from http import HTTPStatus
from mock import patch, Mock

from search_service.api.document import DocumentTableAPI
from search_service import create_app


class TestDocumentTableAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(config_module_class='search_service.config.Config')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tear_down(self):
        self.app_context.pop()

    @patch('search_service.api.document.reqparse.RequestParser')
    @patch('search_service.api.document.get_proxy_client')
    def test_delete(self, get_proxy, RequestParser) -> None:
        mock_proxy = get_proxy.return_value = Mock()
        RequestParser().parse_args.return_value = dict(data='[]', index='fake_index')

        response = DocumentTableAPI().delete(document_id='fake id')
        self.assertEqual(list(response)[1], HTTPStatus.OK)
        mock_proxy.delete_document.assert_called_with(data=['fake id'], index='fake_index')

    def test_should_not_reach_delete_without_id(self):
        response = self.app.test_client().delete('/document_table')

        self.assertEquals(response.status_code, 405)
