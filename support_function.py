#-​*- coding: utf-8 -*​-
import requests,time,unicodecsv as csv

def streams_requests(streams_id,com_url,header):
    """
    This function requests streams data from STRAVA API and return the part of data

    Parameters:
        - streams_id (int):  The number of activities.
        - com_url (str): The API common path
        - header (dict): Include user's token

    Returns:
        - requests_data (dict): Include 10 types element of activities data

    Raises:
        - AttributeError
        - KeyError

    A really simple function. Really!

    >>> streams_id = activities ID
    >>> com_url = 'https://www.strava.com/api/v3/'
    >>> header = {'Authorization': 'Bearer ' + user token  }
    >>> streams_requests(streams_id,com_url,header)

    """
    requests_list = ['time','latlng','distance','altitude','velocity_smooth','heartrate','cadence','watts','temp','grade_smooth']
    requests_dict = {}
    requests_data = {}
    for types in requests_list:
        try:
            while(True):
                requests_dict[types] = requests.get(com_url+"activities/"+str(streams_id)+"/streams/"+types, headers=header).json()
                error = requests_dict[types]["errors"] #成功則表示requests達到上限
                print("Streams requests occur Rate limit , wait 180 second")
                time.sleep(180)
        except:
            None
        requests_data[types] = None
        for info in requests_dict[types]: # 將requests結果中的data部分分解出來
            if info['type'] == types:
                requests_data[types] = info["data"]
    return requests_data

def read_table(table_path):
    """
    Read activities_table.csv and return it.

    Parameters:
        - table_path (str):  The path of activities_table.csv, different user has different table_path

    Returns:
        - table (list): Include the activities ID which is finished download

    Raises:
        - AttributeError
        - KeyError

    A really simple function. Really!

    >>> table_path = "C:/../../"+ user name + "/" + "activities_table.csv"
    >>> read_table(table_path)

    """
    table = [] #table初始化，若檔案開啟失敗，表示尚未建檔，則回傳此空集合
    try:
        activities_table = open(table_path,"r+b")
        for table in csv.reader(activities_table,encoding='utf-8'):
            activities_table.close()
    except:
        None
    return table

def analysis_data(id,requests_data):
    """
    Disaggregated data in the order then parse into json and csv format

    Parameters:
        - id (int):  The number of activities.
        - requests_data (dict): Include 10 types element of activities data

    Returns:
        - streams_json_list (list): data in json format
        - streams_csv_list (list): data in csv format

    Raises:
        - AttributeError
        - KeyError

    A really simple function. Really!

    >>> id = `activities ID`
    >>> com_url = 'https://www.strava.com/api/v3/'
    >>> header = {'Authorization': 'Bearer ' + `user token` }
    >>> requests_data = streams_requests(id,com_url,header)
    >>> analysis_data(id,requests_data)

    """
    streams_json_list = []
    streams_csv_list = []
    requests_list = ['time','latlng','distance','altitude','velocity_smooth','heartrate','cadence','watts','temp','grade_smooth']
    for count in range(0,len(requests_data["time"])):
        streams_json_temp = {}
        streams_csv_temp = []
        streams_json_temp["id"] = id
        for type in requests_list:
            if requests_data[type] != None:
                if type == "latlng":
                    streams_json_temp["lat"] = requests_data[type][count][0]
                    streams_json_temp["lng"] = requests_data[type][count][1]
                    streams_csv_temp += [requests_data[type][count][0],requests_data[type][count][1]]
                else:
                    if type == "velocity_smooth":
                        streams_json_temp["velocity_smooth"] = requests_data["velocity_smooth"][count]*3.6
                        streams_csv_temp += [requests_data["velocity_smooth"][count]*3.6]
                    else:
                        streams_json_temp[type] = requests_data[type][count]
                        streams_csv_temp += [requests_data[type][count]]
            else:
                if type == "latlng":
                    streams_json_temp["lat"] = "Null"
                    streams_json_temp["lng"] = "Null"
                    streams_csv_temp += [0,0]
                else:
                    streams_json_temp[type] = "Null"
                    streams_csv_temp += [0]
        streams_csv_list += eval('['+str(streams_csv_temp)+']')
        streams_json_list += eval('['+str(streams_json_temp)+']')
    return streams_json_list,streams_csv_list