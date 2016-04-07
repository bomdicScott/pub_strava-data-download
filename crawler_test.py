#-​*- coding: utf-8 -*​-
import pytest
from support_function import  *

@pytest.fixture()
def table():
    return read_table("C:/Users\sean/Desktop/bOMDIC/Eric.Lin/activities_table.csv")

def test_read_table(table):
    type(table) == type([])
    if ( table != [] ):
        for id in table:
            type(int(id)) == type(1)

def test_analysis_data():
    None