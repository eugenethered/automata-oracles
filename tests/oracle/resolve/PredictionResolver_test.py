import unittest
from typing import Optional

from core.number.BigFloat import BigFloat
from core.oracle.Prediction import Prediction

from oracle.Oracle import Oracle
from oracle.resolve.PredictionResolver import PredictionResolver


class PredictionResolverTestCase(unittest.TestCase):

    def test_should_collect_a_prediction_from_oracles(self):
        class SimpleOracle(Oracle):
            def predict(self, instrument, exchanged_from, instant) -> Optional[Prediction]:
                return Prediction(['OTC', 'GBP'], BigFloat('100.00'))

        resolver = PredictionResolver([SimpleOracle()])
        prediction = resolver.resolve('OTC', None, None, None)
        self.assertEqual(prediction.outcome, ['OTC', 'GBP'])
        self.assertEqual(prediction.percent, BigFloat('100.00'))

    def test_should_have_no_prediction_from_oracles(self):
        class SimpleOracle(Oracle):
            def predict(self, instrument, exchanged_from, instant) -> Optional[Prediction]:
                return None

        resolver = PredictionResolver([SimpleOracle()])
        prediction = resolver.resolve('OTC', None, None, None)
        self.assertIsNone(prediction)

    def test_should_obtain_best_prediction_from_oracles(self):
        class SimpleOracle(Oracle):
            def predict(self, instrument, exchanged_from, instant) -> Optional[Prediction]:
                return Prediction(['OTC', 'GBP'], BigFloat('10.00'))

        class SimpleGreaterOracle(Oracle):
            def predict(self, instrument, exchanged_from, instant) -> Optional[Prediction]:
                return Prediction(['OTC', 'GBP'], BigFloat('25.00'), forced=True)

        resolver = PredictionResolver([SimpleOracle(), SimpleGreaterOracle()])
        prediction = resolver.resolve('OTC', None, None, None)
        self.assertEqual(prediction.outcome, ['OTC', 'GBP'])
        self.assertEqual(prediction.percent, BigFloat('25.00'))

    def test_should_obtain_best_prediction_as_forced_prioritized_from_oracles(self):
        class SimpleOracle(Oracle):
            def predict(self, instrument, exchanged_from, instant) -> Optional[Prediction]:
                return Prediction(['OTC', 'GBP'], BigFloat('10.00'))

        class SimpleForcedOracle(Oracle):
            def predict(self, instrument, exchanged_from, instant) -> Optional[Prediction]:
                return Prediction(None, BigFloat('0.00'), forced=True)

        resolver = PredictionResolver([SimpleOracle(), SimpleForcedOracle()])
        prediction = resolver.resolve('OTC', None, None, None)
        self.assertEqual(prediction.outcome, None)
        self.assertEqual(prediction.percent, BigFloat('0.00'))
        self.assertTrue(prediction.forced)

    def test_should_obtain_forced_prediction_from_oracles(self):
        class SimpleOracle(Oracle):
            def predict(self, instrument, exchanged_from, instant) -> Optional[Prediction]:
                return Prediction(['OTC', 'GBP'], BigFloat('10.00'))

        class SimpleForcedOracle(Oracle):
            def predict(self, instrument, exchanged_from, instant) -> Optional[Prediction]:
                return Prediction(['GBP', 'OTC'], BigFloat('0.00'), forced=True)

        resolver = PredictionResolver([SimpleOracle(), SimpleForcedOracle()])
        prediction = resolver.resolve('OTC', None, None, None)
        self.assertEqual(prediction.outcome, ['GBP', 'OTC'])
        self.assertEqual(prediction.percent, BigFloat('0.00'))
        self.assertTrue(prediction.forced)


if __name__ == '__main__':
    unittest.main()
