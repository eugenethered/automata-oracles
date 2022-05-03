import unittest

from core.exchange.InstrumentExchange import InstrumentExchange
from core.number.BigFloat import BigFloat
from exchange.rate.InstantRate import InstantRate

from oracle.tools.delta_calc import calc_delta, calc_delta_prediction


class DeltaCalcTestCase(unittest.TestCase):

    def test_should_compute_instant_rate_delta(self):
        rate = InstantRate(2, BigFloat('150.00'))
        other_rate = InstantRate(1, BigFloat('100.00'))
        delta = calc_delta(rate, other_rate)
        self.assertEqual(delta, BigFloat('50.00'))

    def test_should_compute_negative_instant_rate_delta(self):
        rate = InstantRate(2, BigFloat('100.00'))
        other_rate = InstantRate(1, BigFloat('150.00'))
        delta = calc_delta(rate, other_rate)
        self.assertEqual(delta, BigFloat('-50.00'))

    def test_should_compute_delta_prediction(self):
        rate = InstantRate(2, BigFloat('150.00'))
        other_rate = InstantRate(1, BigFloat('100.00'))
        instrument_exchange = InstrumentExchange('OTC', 'GBP')
        delta_prediction = calc_delta_prediction(rate, other_rate, instrument_exchange)
        self.assertEqual(delta_prediction.outcome, ['OTC', 'GBP'])
        self.assertEqual(delta_prediction.profit, BigFloat('50.00'))

    def test_should_compute_negative_delta_prediction(self):
        rate = InstantRate(2, BigFloat('100.00'))
        other_rate = InstantRate(1, BigFloat('150.00'))
        instrument_exchange = InstrumentExchange('OTC', 'GBP')
        delta_prediction = calc_delta_prediction(rate, other_rate, instrument_exchange)
        self.assertEqual(delta_prediction.outcome, ['OTC', 'GBP'])
        self.assertEqual(delta_prediction.profit, BigFloat('-50.00'))

    def test_should_not_compute_delta_prediction_when_either_instant_rate_is_none(self):
        rate = InstantRate(2, BigFloat('100.00'))
        instrument_exchange = InstrumentExchange('OTC', 'GBP')
        delta_prediction = calc_delta_prediction(rate, None, instrument_exchange)
        self.assertIsNone(delta_prediction)
        delta_prediction = calc_delta_prediction(None, rate, instrument_exchange)
        self.assertIsNone(delta_prediction)



if __name__ == '__main__':
    unittest.main()
