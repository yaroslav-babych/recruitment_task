from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from recruitment_task.utils.testing import BaseTestCase, AnyValue


class TestDynamicModelApi(BaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.api_client = APIClient()
        self.base_route = "/api/table/"

        # Create initial models
        player_model_data = {
            "model_name": "Player",
            "fields": {
                "name": "string",
                "won_champions_league": "boolean",
                "goals": "number"
            }
        }
        resp_player = self.api_client.post(self.base_route, data=player_model_data, format="json")
        self.player_model_id = resp_player.data["id"]

    def test_model_create(self):
        resp: Response = self.api_client.post(
            self.base_route,
            data={
                "model_name": "FootballTeam",
                "fields": {
                    "name": "string",
                    "won_champions_league": "boolean",
                    "year_established": "number"
                }
            },
            format="json"
        )
        self.assertEqual(status.HTTP_201_CREATED, resp.status_code)
        self.assertDictEqual(
            {
                "id": AnyValue(int),
                "model_name": "FootballTeam",
                "fields": {
                    "name": "string",
                    "won_champions_league": "boolean",
                    "year_established": "number"
                }
            },
            resp.data
        )

    def test_model_create_invalid_fields(self):
        resp: Response = self.api_client.post(
            self.base_route,
            data={
                "model_name": "InvalidTeam",
                "fields": {
                    "name": "INVALID_FIELD_TYPE",
                    "won_champions_league": "boolean",
                    "year_established": "number"
                }
            },
            format="json"
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, resp.status_code)

    def test_model_create_duplicate_model(self):
        resp: Response = self.api_client.post(
            self.base_route,
            data={
                "model_name": "Player",
                "fields": {
                    "name": "string",
                    "won_champions_league": "boolean",
                    "goals": "number"
                }
            },
            format="json"
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, resp.status_code)

    def test_structure_update(self):
        resp: Response = self.api_client.put(
            f"{self.base_route}/{self.player_model_id}",
            data={
                "model_name": "Player",
                "fields": {
                    "full_name": "string",
                    "t_shirt_number": "number",
                    "retired": "bool",
                }
            },
            format="json"
        )
        # Rest of the test_structure_update method remains the same

    def test_structure_update_invalid_fields(self):
        resp: Response = self.api_client.put(
            f"{self.base_route}/{self.player_model_id}",
            data={
                "model_name": "Player",
                "fields": {
                    "full_name": "INVALID_FIELD_TYPE",
                    "t_shirt_number": "number",
                    "retired": "bool",
                }
            },
            format="json"
        )
        # Rest of the test_structure_update_invalid_fields method remains the same

    def test_model_list(self):
        resp: Response = self.api_client.get(self.base_route)
        self.assertEqual(status.HTTP_200_OK, resp.status_code)
        self.assertEqual(len(resp.data), 1)  # One model was created in setUp

