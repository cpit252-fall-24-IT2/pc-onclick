import unittest
from unittest.mock import patch, MagicMock
from User.user_preferences import UserPreferences
from User.Memento import Memento

## We used CHATGPT
class TestUserPreferences(unittest.TestCase):

    @patch('User.user_preferences.AIAgent')
    def setUp(self, MockAIAgent):
        self.mock_agent = MockAIAgent.return_value
        self.user_preferences = UserPreferences()

    def test_save_build(self):
        build = MagicMock()
        with patch('builtins.input', side_effect=['yes']):
            self.user_preferences.save_build(build)
            self.assertIn(build, self.user_preferences.builds)

    def test_save_build_to_memento(self):
        build = MagicMock()
        with patch('builtins.input', side_effect=['no']):
            self.user_preferences.save_build(build)
            self.assertIn(build, self.user_preferences.Memento_list)

    def test_view_saved_build(self):
        build = MagicMock()
        self.user_preferences.builds.append(build)
        with patch('builtins.print') as mock_print:
            self.user_preferences.view_saved_build()
            mock_print.assert_called()

    def test_restore_pc_state_valid_index(self):
        pc_mock = MagicMock()
        memento = Memento(pc_mock)
        self.user_preferences.Memento_list.append(memento)

        restored_pc = self.user_preferences.restore_pc_state(0)
        self.assertEqual(restored_pc, memento)
        self.assertNotIn(memento, self.user_preferences.Memento_list)

    def test_restore_pc_state_invalid_index(self):
        self.user_preferences.Memento_list = []
        with patch('builtins.print') as mock_print:
            restored_pc = self.user_preferences.restore_pc_state(0)
            self.assertIsNone(restored_pc)
            mock_print.assert_called_with("No saved PC builds to restore.")

    def test_user_choice_restore_previous_build(self):
        pc_mock = MagicMock()
        memento = Memento(pc_mock)
        self.user_preferences.Memento_list.append(memento)

    # Mock enough inputs for all the input calls
        with patch('builtins.input', side_effect=['3', '1', 'yes', '4']), patch('builtins.print') as mock_print:
          with self.assertRaises(SystemExit):  # '4' will trigger the exit
               self.user_preferences.user_choice_()

        # Verify that the restore logic was triggered
        mock_print.assert_any_call("Restored Build:\n")
    def test_user_choice_exit(self):
        with patch('builtins.input', side_effect=['4']), self.assertRaises(SystemExit):
            self.user_preferences.user_choice_()

    def test_view_saved_pc_states_empty(self):
        self.user_preferences.Memento_list = []
        with patch('builtins.print') as mock_print:
            self.user_preferences.view_saved_pc_states()
            mock_print.assert_called_with("\nNo saved memento  found.")

    def test_view_saved_pc_states_with_data(self):
        pc_mock = MagicMock()
        memento = Memento(pc_mock)
        self.user_preferences.Memento_list.append(memento)

        with patch('builtins.print') as mock_print:
            self.user_preferences.view_saved_pc_states()
            mock_print.assert_called()

    def test_loading_animation(self):
        stop_event = MagicMock()
        stop_event.is_set.side_effect = [False, False, True]  # Stop after 3 iterations
        with patch('time.sleep'), patch('builtins.print') as mock_print:
            self.user_preferences.loading_animation(stop_event)
            self.assertTrue(mock_print.called)

    def test_get_user_preferences(self):
     with patch('builtins.input', side_effect=["Gaming", "1500", "yes"]), \
          patch('threading.Thread.start'), \
          patch('threading.Thread.join'):
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
        self.assertEqual(self.user_preferences.use_case, "Gaming")
        self.assertEqual(self.user_preferences.budget, 1500.0)

if __name__ == "__main__":
    unittest.main()