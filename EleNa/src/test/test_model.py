from EleNa.src.app.data_model import data_model
import os
import sys

sys.path.append('../../')
os.chdir('../')


def test_model_availability():
    dm = data_model.DataModel('Amherst, MA')
    assert dm.G != {}


def test_config_value():
    d = data_model.DataModel('Amherst, MA')
    assert d.config != {}
