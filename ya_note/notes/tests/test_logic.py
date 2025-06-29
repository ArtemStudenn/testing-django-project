# news/tests/test_logic.py
from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .base import TestBase, NOTES_ADD, NOTES_DELETE, NOTES_EDIT


class TestLogic(TestBase):
    def test_anonymous_user_cant_create_note(self):
        notes_count_before = Note.objects.count()
        self.client.post(NOTES_ADD, data=self.form_data)
        self.assertEqual(Note.objects.count(), notes_count_before)

    def test_user_can_create_note(self):
        Note.objects.all().delete()
        self.author_client.post(NOTES_ADD, data=self.form_data)
        self.assertEqual(Note.objects.count(), 1)
        created_note = Note.objects.get()
        self.assertEqual(created_note.title, self.form_data['title'])
        self.assertEqual(created_note.text, self.form_data['text'])
        self.assertEqual(created_note.slug, self.form_data['slug'])
        self.assertEqual(created_note.author, self.author)

    def test_not_unique_slug(self):
        notes_count_before = Note.objects.count()
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(NOTES_ADD, data=self.form_data)
        form = response.context['form']
        self.assertFormError(form, 'slug', errors=(self.note.slug + WARNING))
        self.assertEqual(Note.objects.count(), notes_count_before)

    def test_empty_slug(self):
        Note.objects.all().delete()
        self.form_data.pop('slug')
        self.author_client.post(NOTES_ADD, data=self.form_data)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, expected_slug)
        self.assertEqual(new_note.author, self.author)

    def test_author_can_delete_note(self):
        notes_count_before = Note.objects.count()
        self.author_client.delete(NOTES_DELETE)
        self.assertEqual(Note.objects.count(), notes_count_before - 1)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_other_user_cant_delete_note(self):
        notes_count_before = Note.objects.count()
        response = self.reader_client.delete(NOTES_DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), notes_count_before)

    def test_author_can_edit_note(self):
        self.author_client.post(NOTES_EDIT, data=self.form_data)
        edited_note = Note.objects.get(id=self.note.id)
        self.assertEqual(edited_note.title, self.form_data['title'])
        self.assertEqual(edited_note.text, self.form_data['text'])
        self.assertEqual(edited_note.slug, self.form_data['slug'])
        self.assertEqual(edited_note.author, self.author)

    def test_other_user_cant_edit_note(self):
        response = self.reader_client.post(NOTES_EDIT, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        not_edited_note = Note.objects.get(id=self.note.id)
        self.assertEqual(not_edited_note.title, self.note.title)
        self.assertEqual(not_edited_note.text, self.note.text)
        self.assertEqual(not_edited_note.slug, self.note.slug)
        self.assertEqual(not_edited_note.author, self.note.author)
