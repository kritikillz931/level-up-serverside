from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from levelupapi.models import GameType, Game

class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new Gamer, collect the auth Token, and create a sample GameType
        """

        # Define the URL path for registering a Gamer
        url = '/register'

        # Define the Gamer properties
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
        response = self.client.post(url, data, format='json')
        self.token = response.data['token']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        game_type = GameType()
        game_type.label = "Board game"
        game_type.save()

    def test_create_game(self):
        url = '/games'
        data = {
            "name": "Clue",
            "maker": "Milton Bradley",
            "numberOfPlayers": 6,
            "gameType": 1,
            "description": "Big Yeetzy"
        }

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'],data['name'])
        self.assertEqual(response.data['maker'],data['maker'])
        self.assertEqual(response.data['description'],data['description'])
        self.assertEqual(response.data['number_of_players'],data['numberOfPlayers'])


    def test_get_game(self):
        """
        Ensure we can GET an existing game.
        """

        # Create a new instance of Game
        game = Game()
        game.gamer_id = 1
        game.name = "Monopoly"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.game_type_id = 1
        game.description = "Real-Estate, and Finance, and Bankruptcy, OH MY!"

        # Save the Game to the testing database
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.get(f'/games/{game.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        self.assertEqual(response.data["name"], game.name)
        self.assertEqual(response.data["maker"], game.maker)
        self.assertEqual(response.data["number_of_players"], game.number_of_players)
        self.assertEqual(response.data["description"], game.description)

    def test_update_game(self):
        """
        Ensure we can change an existing game.
        """

        # Create a new instance of Game
        game = Game()
        game.game_type_id = 1
        game.name = "Sorry"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.gamer_id = 1
        game.description = "Not Sorry!"

        # Save the Game to the testing database
        game.save()

        # Define the URL path for updating an existing Game

        # Define NEW Game properties
        data = {
            "name": "Sorry",
            "maker": "Hasbro",
            "numberOfPlayers": 4,
            "gameTypeId": 1,
            "description": game.description
        }

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.put(f'/games/{game.id}', data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Initiate PUT request and capture the response

        # Assert that the response status code is 204 (NO CONTENT)

        # Initiate GET request and capture the response
        response = self.client.get(f'/games/{game.id}')

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data["name"], data['name'])
        self.assertEqual(response.data["maker"], data['maker'])
        self.assertEqual(
            response.data["number_of_players"], data['numberOfPlayers'])
        self.assertEqual(response.data["description"], data['description'])



    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """

        # Create a new instance of Game
        game = Game()
        game.gamer_id = 1
        game.name = "Sorry"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.game_type_id = 1
        game.description = "It's too late to apologize."

        # Save the Game to the testing database
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        url = f'/games/{game.id}'
        response = self.client.delete(url)

        # Define the URL path for deleting an existing Game

        # Initiate DELETE request and capture the response

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Initiate GET request and capture the response
        response = self.client.get(url)

        # Assert that the response status code is 404 (NOT FOUND)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)