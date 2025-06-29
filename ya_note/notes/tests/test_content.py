from notes.forms import NoteForm
from notes.models import Note
from .base import TestBase, NOTES_ADD, NOTES_EDIT, NOTES_LIST


class TestContent(TestBase):
    def test_note_in_author_list(self):
        self.assertIn(
            self.note,
            self.author_client.get(NOTES_LIST).context['object_list']
        )
        note_to_see = Note.objects.get(id=self.note.id)
        self.assertEqual(note_to_see.title, self.note.title)
        self.assertEqual(note_to_see.text, self.note.text)
        self.assertEqual(note_to_see.slug, self.note.slug)
        self.assertEqual(note_to_see.author, self.note.author)

    def test_note_not_in_reader_list(self):
        self.assertNotIn(
            self.note,
            self.reader_client.get(NOTES_LIST).context['object_list']
        )

    def test_create_edit_have_forms(self):
        urls = (NOTES_ADD, NOTES_EDIT)
        for url in urls:
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.author_client.get(url).context.get('form'), NoteForm
                )
