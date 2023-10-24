from django.test import TestCase

from lists.sql_wrappers import get_all, create_items, ensure_table_exists_with_column

from django.db import connection


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class ListViewTest(TestCase):
    def setUp(self):
        with connection.cursor() as cursor:
            ensure_table_exists_with_column(connection, "lists_item", "text")
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
        self.assertEqual(len(get_all("item")), 1)
        new_item = get_all("item")[0]
        self.assertEqual(new_item["text"], "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertRedirects(response, "/lists/the-only-list-in-the-world/")


class SQLWrappersTest(TestCase):
    def setUp(self):
        with connection.cursor() as cursor:
            ensure_table_exists_with_column(connection, "lists_item", "text")
            cursor.execute("INSERT INTO lists_item (text) VALUES (%s)", ["test_text_1"])
            cursor.execute("INSERT INTO lists_item (text) VALUES (%s)", ["test_text_2"])

    def test_can_get_all_items_with_text_field(self):
        items = get_all("item")
        self.assertEqual(len(items), 2)
        assert all(item["text"] in ["test_text_1", "test_text_2"] for item in items)

    def test_can_create_new_item(self):
        create_items(["test_text"])
        assert "test_text" in [item["text"] for item in get_all("item")]

    def test_can_create_multiple_items(self):
        text_values = ["test_text_1", "test_text2"]
        create_items(text_values)
        all_items = get_all("item")
        for value in text_values:
            assert value in [item["text"] for item in all_items]
