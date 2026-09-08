import unittest

from fastapi.testclient import TestClient

from src.app import app


class MangaManiacsActivityTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_activity_present(self):
        response = self.client.get("/activities")

        self.assertEqual(response.status_code, 200)

        activities = response.json()
        self.assertIn("Manga Maniacs", activities)

        activity = activities["Manga Maniacs"]
        self.assertEqual(
            activity["description"],
            "Explore the fantastic stories of the most interesting characters "
            "from Japanese Manga(graphic novels).",
        )
        self.assertEqual(activity["schedule"], "Tuesdays at 7pm")
        self.assertEqual(activity["max_participants"], 15)
        self.assertEqual(activity["participants"], [])

    def test_signup_for_activity(self):
        email = "manga-fan@mergington.edu"

        response = self.client.post(
            "/activities/Manga%20Maniacs/signup",
            params={"email": email},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["message"],
            f"Signed up {email} for Manga Maniacs",
        )

        cleanup = self.client.delete(
            "/activities/Manga%20Maniacs/unregister",
            params={"email": email},
        )
        self.assertEqual(cleanup.status_code, 200)
