from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        return false if the question pub_date in  the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)
    def test_was_published_recently_with_old_question(self):
        """
        return false if the question pub_date in  the older then one day
        """
        time = timezone.now() + datetime.timedelta(days=-30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)
    def test_was_published_recently_with_recent_question(self):
        """
        return false if the question pub_date in  within the last day
        """
        time = timezone.now() + datetime.timedelta(hours=-23)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(),True)


    