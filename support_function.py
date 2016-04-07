#-​*- coding: utf-8 -*​-
import requests,time,unicodecsv as csv

def streams_requests(streams_id,com_url,header):
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
    table = [] #table初始化，若檔案開啟失敗，表示尚未建檔，則回傳此空集合
    try:
        activities_table = open(table_path,"r+b")
        for table in csv.reader(activities_table,encoding='utf-8'):
            activities_table.close()
    except:
        None
    return table

def analysis_data(id,requests_data):
    streams_data_list = []
    streams_data_list_csv = []
    requests_list = ['time','latlng','distance','altitude','velocity_smooth','heartrate','cadence','watts','temp','grade_smooth']
    for count in range(0,len(requests_data["time"])):
        streams_data_temp = {}
        streams_data_temp_csv = []
        streams_data_temp["id"] = id
        for type in requests_list:
            if requests_data[type] != None:
                if type == "latlng":
                    streams_data_temp["lat"] = requests_data[type][count][0]
                    streams_data_temp["lng"] = requests_data[type][count][1]
                    streams_data_temp_csv += [requests_data[type][count][0],requests_data[type][count][1]]
                else:
                    if type == "velocity_smooth":
                        streams_data_temp["velocity_smooth"] = requests_data["velocity_smooth"][count]*3.6
                        streams_data_temp_csv += [requests_data["velocity_smooth"][count]*3.6]
                    else:
                        streams_data_temp[type] = requests_data[type][count]
                        streams_data_temp_csv += [requests_data[type][count]]
            else:
                if type == "latlng":
                    streams_data_temp["lat"] = "Null"
                    streams_data_temp["lng"] = "Null"
                    streams_data_temp_csv += [0,0]
                else:
                    streams_data_temp[type] = "Null"
                    streams_data_temp_csv += [0]
        streams_data_list_csv += eval('['+str(streams_data_temp_csv)+']')
        streams_data_list += eval('['+str(streams_data_temp)+']')
    return streams_data_list,streams_data_list_csv