from django.urls import reverse
from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question


def create_question(question_text,days):
        time = timezone.now()+datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text,pub_date=time)


class QuestionModelTests(TestCase):  
    def test_was_published_recently_with_future_question(self):
        """
        return false if the question pub_date in  the future
        """
        future_question = create_question(question_text='future_question',days=30)
        self.assertIs(future_question.was_published_recently(),False)
    def test_was_published_recently_with_old_question(self):
        """
        return false if the question pub_date in  the older then one day
        """
        old_question = create_question(question_text='old_question',days=-30)
        self.assertIs(old_question.was_published_recently(),False)
    def test_was_published_recently_with_recent_question(self):
        """
        return false if the question pub_date in  within the last day
        """
        time = timezone.now() + datetime.timedelta(hours=-23)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(),True)

class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """
        if there is no question message will appear
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No Polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])
    def test_past_question(self):
        """
        the pas question will appear
        """
        old_question = create_question(question_text='old_question',days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,old_question.question_text)
        self.assertQuerysetEqual(response.context['latest_question_list'],[old_question])
    def test_future_question(self):
        """
        the pas question will appear
        """
        future_question = create_question(question_text='old_question',days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No Polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])
    
    def test_past_question_and_future_question(self):
        """
        the pas question will appear
        """
        future_question = create_question(question_text='old_question',days=30)
        old_question = create_question(question_text='old_question',days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,old_question.question_text)
        self.assertQuerysetEqual(response.context['latest_question_list'],[old_question])
    
    def test_two_past_questions(self):
        """
        the two past question will appear
        """
        old_question_1 = create_question(question_text='old_question',days=-30)
        old_question_2= create_question(question_text='old_question',days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,old_question_1.question_text)
        self.assertContains(response,old_question_2.question_text)
        self.assertQuerysetEqual(response.context['latest_question_list'],[old_question_2,old_question_1])

class QuestionDetailViewTests(TestCase):
    def test_past_question(self):
        """
        the past question will appear
        """
        old_question = create_question(question_text='old_question',days=-30)
        response = self.client.get(reverse('polls:detail',args=(old_question.id,)))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,old_question.question_text)
    def test_future_question(self):
        """
        the future question doesnt appear
        """
        future_question = create_question(question_text='old_question',days=30)
        response = self.client.get(reverse('polls:detail',args=(future_question.id,)))
        self.assertEqual(response.status_code,404)
