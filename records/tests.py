from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Record


class DashboardViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='user1', password='pass12345')
        self.other = get_user_model().objects.create_user(username='user2', password='pass12345')

    def test_login_required(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_only_owner_records_visible(self):
        Record.objects.create(title='내 데이터', category='A', amount=100, note='', owner=self.user)
        Record.objects.create(title='남의 데이터', category='B', amount=200, note='', owner=self.other)

        self.client.login(username='user1', password='pass12345')
        response = self.client.get(reverse('dashboard'))

        self.assertContains(response, '내 데이터')
        self.assertNotContains(response, '남의 데이터')

    def test_filter_and_sort(self):
        Record.objects.create(title='가', category='영업', amount=Decimal('100.00'), note='', owner=self.user)
        Record.objects.create(title='나', category='영업', amount=Decimal('50.00'), note='', owner=self.user)
        Record.objects.create(title='다', category='개발', amount=Decimal('70.00'), note='', owner=self.user)

        self.client.login(username='user1', password='pass12345')
        response = self.client.get(
            reverse('dashboard'),
            {
                'category': '영업',
                'min_amount': '60',
                'sort_by': 'amount',
                'sort_order': 'asc',
            },
        )

        records = list(response.context['records'])
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].title, '가')

    def test_create_edit_delete_record(self):
        self.client.login(username='user1', password='pass12345')

        create_response = self.client.post(
            reverse('dashboard'),
            {'title': '신규', 'category': '운영', 'amount': '12.50', 'note': '비고'},
            follow=True,
        )
        self.assertEqual(create_response.status_code, 200)
        record = Record.objects.get(title='신규')
        self.assertEqual(record.owner, self.user)

        edit_response = self.client.post(
            reverse('edit_record', kwargs={'record_id': record.id}),
            {'title': '수정', 'category': '운영', 'amount': '99.99', 'note': '변경'},
            follow=True,
        )
        self.assertEqual(edit_response.status_code, 200)
        record.refresh_from_db()
        self.assertEqual(record.title, '수정')

        delete_response = self.client.post(
            reverse('delete_record', kwargs={'record_id': record.id}),
            follow=True,
        )
        self.assertEqual(delete_response.status_code, 200)
        self.assertFalse(Record.objects.filter(id=record.id).exists())
