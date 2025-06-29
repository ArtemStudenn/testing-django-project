from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .base import TestBase, NOTES_ADD, NOTES_DELETE, NOTES_EDIT


class TestLogic(TestBase):
    def test_anonymous_user_cant_create_note(self):
        notes = set(Note.objects.all())
        self.client.post(NOTES_ADD, data=self.form_data)
        self.assertEqual(set(Note.objects.all()), notes)

    def test_user_can_create_note(self):
        Note.objects.all().delete()
        self.author_client.post(NOTES_ADD, data=self.form_data)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.author)

    def test_not_unique_slug(self):
        notes = set(Note.objects.all())
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(NOTES_ADD, data=self.form_data)
        form = response.context['form']
        self.assertFormError(form, 'slug', errors=(self.note.slug + WARNING))
        self.assertEqual(set(Note.objects.all()), notes)

    def test_empty_slug(self):
        Note.objects.all().delete()
        self.form_data.pop('slug')
        self.author_client.post(NOTES_ADD, data=self.form_data)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, slugify(self.form_data['title']))
        self.assertEqual(note.author, self.author)

    def test_author_can_delete_note(self):
        notes = Note.objects.count()
        self.author_client.post(NOTES_DELETE)
        self.assertEqual(Note.objects.count(), notes - 1)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_other_user_cant_delete_note(self):
        notes = set(Note.objects.all())
        response = self.reader_client.post(NOTES_DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(set(Note.objects.all()), notes)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_author_can_edit_note(self):
        self.author_client.post(NOTES_EDIT, data=self.form_data)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.note.author)

    def test_other_user_cant_edit_note(self):
        response = self.reader_client.post(NOTES_EDIT, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)
