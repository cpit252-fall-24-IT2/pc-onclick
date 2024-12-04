import unittest
from unittest.mock import patch, MagicMock
from User.user_preferences import UserPreferences
from LLM.AIagent import AIAgent

class TestUserPreferences(unittest.TestCase):

    @patch('User.user_preferences.AIAgent')
    def setUp(self, MockAIAgent):
        self.mock_agent = MockAIAgent.return_value
        self.user_preferences = UserPreferences()

    def test_user_choice_start_new_build(self):
        with patch('builtins.input', side_effect=['1', 'Gaming', '1500', 'yes', '3']):
            with patch('threading.Thread.start'), patch('threading.Thread.join'):
                self.mock_agent.fetch_component.return_value = ({}, "")
                self.mock_agent.get_full_component_details.return_value = {
                    'CPU': {'name': 'Intel i9', 'price': 500, 'core_count': 8},
                    'GPU': {'name': 'NVIDIA RTX 3080', 'price': 700, 'chipset': 'NVIDIA'},
                    'Motherboard': {'name': 'ASUS ROG', 'price': 300, 'socket': 'LGA1200'},
                    'PSU': {'name': 'Corsair 750W', 'price': 100, 'efficiency': 'Gold',
                            'wattage': 750, 'modular': True},
                    'RAM': {'name': 'Corsair Vengeance', 'price': 150, 'capacity': 32,
                            'speed': 3200},
                    'Storage': {'name': 'Samsung 970 EVO', 'price': 200, 'capacity': 1000}
                }
                with self.assertRaises(SystemExit):
                    self.user_preferences.user_choice_()
                self.assertEqual(self.user_preferences.use_case, 'Gaming')
                self.assertEqual(self.user_preferences.budget, 1500.0)

    def test_user_choice_view_saved_build(self):
        with patch('builtins.input', side_effect=['2', '3']):
            with patch('User.user_preferences.UserPreferences.view_saved_build') as mock_view_saved_build:
                with self.assertRaises(SystemExit):
                    self.user_preferences.user_choice_()
                mock_view_saved_build.assert_called_once()

    def test_user_choice_exit(self):
        with patch('builtins.input', side_effect=['3']):
            with self.assertRaises(SystemExit):
                self.user_preferences.user_choice_()

    def test_get_user_preferences(self):
        with patch('builtins.input', side_effect=['Gaming', '1500', 'yes']):
            with patch('threading.Thread.start'), patch('threading.Thread.join'):
                self.mock_agent.fetch_component.return_value = ({}, "")
                self.mock_agent.get_full_component_details.return_value = {
                    'CPU': {'name': 'Intel i9', 'price': 500, 'core_count': 8},
                    'GPU': {'name': 'NVIDIA RTX 3080', 'price': 700, 'chipset': 'NVIDIA'},
                    'Motherboard': {'name': 'ASUS ROG', 'price': 300, 'socket': 'LGA1200'},
                    'PSU': {'name': 'Corsair 750W', 'price': 100, 'efficiency': 'Gold',
                            'wattage': 750, 'modular': True},
                    'RAM': {'name': 'Corsair Vengeance', 'price': 150, 'capacity': 32,
                            'speed': 3200},
                    'Storage': {'name': 'Samsung 970 EVO', 'price': 200, 'capacity': 1000}
                }
                self.user_preferences.get_user_preferences()
                self.assertEqual(self.user_preferences.use_case, 'Gaming')
                self.assertEqual(self.user_preferences.budget, 1500.0)

    def test_save_build(self):
        build = MagicMock()
        with patch('builtins.input', side_effect=['yes']):
            self.user_preferences.save_build(build)
            self.assertIn(build, self.user_preferences.builds)

    def test_view_saved_build(self):
        build = MagicMock()
        self.user_preferences.builds.append(build)
        with patch('builtins.print'):
            self.user_preferences.view_saved_build()

if __name__ == '__main__':
    unittest.main()