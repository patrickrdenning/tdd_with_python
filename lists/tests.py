from django.test import TestCase

from lists.models import Item

from lists.sql_wrappers import get_all_items, create_items

from django.db import connection


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_only_saves_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):
    def setUp(self):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO lists_item (text) VALUES (%s)", ["itemey 1"])
            cursor.execute("INSERT INTO lists_item (text) VALUES (%s)", ["itemey 2"])

    def test_displays_all_list_items(self):
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")

    def test_uses_list_template(self):
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertTemplateUsed(response, "list.html")


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertRedirects(response, "/lists/the-only-list-in-the-world/")


class SQLWrappersTest(TestCase):
    def setUp(self):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO lists_item (text) VALUES (%s)", ["test_text_1"])
            cursor.execute("INSERT INTO lists_item (text) VALUES (%s)", ["test_text_2"])

    def test_can_get_all_items_with_text_field(self):
        items = get_all_items()
        self.assertEqual(len(items), 2)
        assert all(item.text in ["test_text_1", "test_text_2"] for item in items)

    def test_can_insert_new_item(self):
        create_items(["test_text"])
        assert "test_text" in [item.text for item in get_all_items()]

    def test_can_insert_multiple_items(self):
        text_values = ["text_text_1", "test_text2"]
        create_items(text_values)
        all_items = get_all_items()
        for value in text_values:
            assert value in [item.text for item in all_items]
