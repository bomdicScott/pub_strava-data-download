#-​*- coding: utf-8 -*​-
import pytest
from support_function import  *


com_url = 'https://www.strava.com/api/v3/' # API路徑
header = {'Authorization': 'Bearer 00723d7cd94ea9b197d28ae36f887f956be6afc8'}
id = 520652338
requests_list = ['time','latlng','distance','altitude','velocity_smooth','heartrate','cadence','watts','temp','grade_smooth']

@pytest.fixture()
def table():
    return read_table("C:/Users\sean/Desktop/bOMDIC/Eric.Lin/activities_table.csv")

@pytest.fixture()
def streams():
    return streams_requests(id,com_url,header)

def test_read_table(table):
    assert type(table) == type([])

    if ( table != [] ):
        for id in table:
            assert type(int(id)) == type(1)

    assert read_table("wefewf2+6+") == []
    assert read_table("52295959") == []

def test_streams_requests(streams):
    for data in streams:
        if ( streams[data] != None ):
            assert type(streams[data]) == type([])