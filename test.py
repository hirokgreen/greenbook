from app import app
import  unittest

class FlaskTestCase(unittest.TestCase):
#ensure that, flask setup is correct/////
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login',content_type='html/text')
        self.assertEqual(response.status_code, 200)

#ensure that, login page loads correctly/////
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login',content_type='html/text')
        self.assertTrue('please login' in response.data)

if __name__ == '__main__':
    unittest.main()