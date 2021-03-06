#-​*- coding: utf-8 -*​-
import pytest
import sys
sys.path.append("../")
from support_function import  *
from plot_picture import *

com_filepath = "C:/users/sean/desktop/strava_raw_data/"
com_url = 'https://www.strava.com/api/v3/' # API路徑
header = {'Authorization': 'Bearer 00723d7cd94ea9b197d28ae36f887f956be6afc8'}
activity_id = 520652338
user_id = 7162913
requests_list = ['time','latlng','distance','altitude','velocity_smooth','heartrate','cadence','watts','temp','grade_smooth']

@pytest.fixture(scope='module')
def table():
    return read_table(com_filepath+"Eric.Lin/activities_table.csv")

@pytest.fixture(scope='module')
def streams():
    return streams_requests(activity_id,com_url,header)

def test_read_table(table):
    assert type(table) == type([])

    if ( table != [] ):
        for id in table:
            assert type(int(id)) == type(1)

    assert read_table("wefewf2+6+") == []
    assert read_table("52295959") == []

def test_read_id():
    id_list = read_id(com_filepath+str(user_id)+"_list.csv")
    assert type(id_list) == type([])
    assert read_id("dsfejfrgrg") == []

def test_streams_requests(streams):
    for data in streams:
        assert type(streams[data]) == type([]) or streams[data] == None
    assert type(streams) == type({})
    assert len(streams) == 10
    for types in requests_list:
        if (streams[types] != None):
            assert len(streams["time"]) == len(streams[types])

def test_analysis_data(streams):
    json_list,csv_list = analysis_data(activity_id,streams)
    assert len(json_list) == len(csv_list)
    for count in range(0,len(json_list)):
        assert type(json_list[0]) == type(json_list[count])
        assert type(csv_list[0]) == type(csv_list[count])
        assert len(json_list[0]) == len(json_list[count])
        assert len(csv_list[0]) == len(csv_list[count])