from django.test import TestCase

from settings.models import Help


class HelpTest(TestCase):
    def setUp(self) -> None:
        self.help = Help.objects.create(title='Test', body='Test Body')

    def test_title_label(self):
        field_label = self.help._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Наименование')

    def test_body_label(self):
        field_label = self.help._meta.get_field('body').verbose_name
        self.assertEqual(field_label, 'Текст')
