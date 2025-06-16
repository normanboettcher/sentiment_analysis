import unittest

from scripts.performance.src.remote_call_review import extract_reviews


class TestRemoteCallReviews(unittest.TestCase):
    def test_extract_reviews_success(self):
        reviews = extract_reviews(n=5, sep=',', path='../../../sentiment-model/data/reviews.csv')
        self.assertEqual(len(reviews), 5, 'Expected length of reviews to be 5')

        for review in reviews:
            print(20 * "=" + "REVIEW" + 20 * "=")
            print(review)
