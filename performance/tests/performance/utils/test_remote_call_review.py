import unittest

from performance.src.performance.utils.remote_call_review import extract_reviews


class TestRemoteCallReviews(unittest.TestCase):
    def test_extract_reviews_success(self):
        reviews = extract_reviews(n_reviews="5", col_sep=',', file_path='../../sentiment-model/data/reviews.csv')
        self.assertEqual(len(reviews), 5, 'Expected length of reviews to be 5')

        for review in reviews:
            print(20 * "=" + "REVIEW" + 20 * "=")
            print(review)
