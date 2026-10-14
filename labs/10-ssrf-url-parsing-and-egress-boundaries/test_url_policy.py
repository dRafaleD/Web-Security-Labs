import unittest
from url_policy import check_url

class PolicyTests(unittest.TestCase):
    def test_approved(self):
        self.assertTrue(check_url("https://reports.example.test/daily").allowed)
        self.assertTrue(check_url("https://status.example.test:443/health").allowed)
    def test_denied(self):
        denied=[
            "http://reports.example.test/a",
            "https://reports.example.test.evil.test/",
            "https://127.0.0.1/",
            "https://[::1]/",
            "https://reader@reports.example.test/",
            "https://reports.example.test:8080/",
            "https://reports.example.test./",
            "https://reports.example.test\\@evil.test/",
            "https://reports.example.test:bad/",
            "file:///etc/passwd",
            "//reports.example.test/",
            "https://reports.example.test/#fragment",
            "",
        ]
        for url in denied:
            with self.subTest(url=url):
                self.assertFalse(check_url(url).allowed)
if __name__=="__main__":
    unittest.main()
