import unittest
from unittest.mock import AsyncMock, MagicMock
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User, Contact
from src.schemas import ContactCreateModel, ContactUpdateModel
from src.repository.contacts import get_contact, put_contact, create_contact, get_all_contacts


class TestAsync(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.user = User(id=1, email="test@tes.com", password="qwerty", confirmed=True)

    async def test_get_todos(self):
        limit = 10
        offset = 0
        expected_todos = [Contact(), Contact(), Contact(), Contact()]

        mock_todos = MagicMock()
        mock_todos.scalars.return_value.all.return_value = expected_todos
        self.session.execute.return_value = mock_todos

        result = await get_all_contacts(limit, offset, self.session)  # Use get_all_contacts instead of get_contact

        self.assertEqual(result, expected_todos)

    async def test_create_todo(self):
        body = ContactCreateModel(title="Test", description="QWERTY")
        result = await create_contact(body, self.session, self.user)
        self.assertEqual(result.title, body.title)
        self.assertEqual(result.description, body.description)
        self.assertTrue(hasattr(result, "completed"))

    async def test_update_todo(self):
        body = ContactUpdateModel(title="Test", description="QWERTY", completed=True)
        todo = Contact(title="Test old", description="QWERTY old", completed=False, user_id=self.user.id)

        mock_todo = MagicMock()
        mock_todo.scalar_one_or_none.return_value = todo
        self.session.execute.return_value = mock_todo

        result = await put_contact(todo.id, body, self.session, self.user)

        self.assertEqual(result.title, body.title)
        self.assertEqual(result.description, body.description)
        self.assertTrue(result.completed, True)