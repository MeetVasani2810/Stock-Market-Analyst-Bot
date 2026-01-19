import sys
import unittest
from unittest.mock import MagicMock, patch

# Adjust path to import from app
sys.path.append('.')

from app.bot.utils import parse_timeframe
from app.pipeline.fetcher import fetch_market_data

class TestTimeframeSupport(unittest.TestCase):
    
    def test_parse_timeframe_valid(self):
        # Minutes
        self.assertEqual(parse_timeframe('1min'), ('1min', '1 Minute', True))
        self.assertEqual(parse_timeframe('15m'), ('15min', '15 Minutes', True))
        
        # Hours
        self.assertEqual(parse_timeframe('1hour'), ('1h', '1 Hour', True))
        self.assertEqual(parse_timeframe('4h'), ('4h', '4 Hours', True))
        
        # Days
        self.assertEqual(parse_timeframe('1d'), ('1day', 'Daily', True))
        
        # Weeks
        self.assertEqual(parse_timeframe('1w'), ('1week', 'Weekly', True))

    def test_parse_timeframe_invalid(self):
        self.assertEqual(parse_timeframe('7min'), (None, None, False))
        self.assertEqual(parse_timeframe('blah'), (None, None, False))
        self.assertEqual(parse_timeframe(''), (None, None, False))

    @patch('app.pipeline.fetcher.requests.get')
    def test_fetch_market_data_with_interval(self, mock_get):
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "values": [{"datetime": "2023-01-01", "open": "100", "high": "110", "low": "90", "close": "105", "volume": "1000"}]
        }
        mock_get.return_value = mock_response
        
        # Call with specific interval
        result = fetch_market_data('BTC/USD', interval='15min')
        
        # Verify result structure
        self.assertEqual(result['interval'], '15min')
        self.assertEqual(result['symbol'], 'BTC/USD')
        
        # Verify API call params
        args, kwargs = mock_get.call_args
        self.assertEqual(kwargs['params']['interval'], '15min')

if __name__ == '__main__':
    unittest.main()
