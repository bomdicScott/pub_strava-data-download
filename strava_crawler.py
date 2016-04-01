import requests, unicodecsv as csv,os,json,time
from plot_picture import *

com_filepath = "C:/users/sean/desktop/bOMDIC/" #檔案讀存路徑
user_file = open(com_filepath+"strava_user.csv","rb") #讀取使用者資訊
com_url = 'https://www.strava.com/api/v3/' # API路徑
user = set([])#將user ID放入,可指定使用者,空白視為全選

def streams_requests(requests_list):
    requests_dict = {}
    for types in requests_list:
        try:
            while(True):
                requests_dict[types] = requests.get(com_url+"activities/"+str(id)+"/streams/"+types, headers=header).json()
                error = requests_dict[types]["errors"]
                print("Rate limit , wait 180 second")
                time.sleep(180)
        except:
            None
        for info in requests_dict[types]:
            if info['type'] == types:
                requests_dict[types] = info["data"]
    return requests_dict

for people in csv.reader(user_file,encoding='utf-8'):
    user_id_set = set(eval("['"+str(people[10])+"']"))
    if(user & user_id_set == user_id_set or user == set([]) ):
        print(people[2]+people[3]+" START")
        header = {'Authorization': 'Bearer '+people[1]}
        try:#處理Requests上限問題
            while(True):
                activities_mes = requests.get(com_url+"activities", headers=header).json()
                error = activities_mes["errors"] #這行成功則表示Requests達到上限,錯誤則表示Requests正常,跳到except執行
                print("Rate limit , wait 180 second")
                time.sleep(180)
        except:
            None
        user_path = com_filepath+people[2]+"."+people[3]
        if not os.path.exists(user_path):#建立使用者專屬資料夾
            os.makedirs(user_path)
        table_path = user_path+"/activities_table.csv"
        activities_table = open(table_path,"a") #初次建檔時，檔案不存在則創建新檔案
        activities_table.close()
        activities_table = open(table_path,"r+b")
        table = set([]) #table初始化
        for table in csv.reader(activities_table,encoding='utf-8'):
            table = set(table)#轉換為SET形式
        activities_table.close()
        for activities in activities_mes:
            id = activities["id"]
            id_set = set(eval("['"+str(id)+"']")) #轉換id成set形式
            if(table & id_set == set([])):
                average_speed = activities["average_speed"]*3.6
                distance  = activities["distance"]/100
                type_name = activities["type"]
                filepath = user_path+"/"+type_name+"_"+str(id)+"_"+str('%.2f' % distance)+"_"+str('%.2f' % average_speed)
                if not os.path.exists(filepath):
                    os.makedirs(filepath)
                with open(filepath+"/activities.json","w") as activities_json:
                    json.dump(activities,activities_json)

                requests_list = ['time','latlng','distance','altitude','velocity_smooth','heartrate','cadence','watts','temp','grade_smooth']
                requests_dict = streams_requests(requests_list)
                print(requests_dict)
                streams_data_list = []
                streams_data_list_csv = []
                streams_csv = open(filepath+"/"+str(id)+"_streams.csv","ab")
                csv_header = ['time','lat','lng','distance','altitude','velocity_smooth','heartrate','cadence','watts','temp','grade_smooth']
                csv.writer(streams_csv,encoding='UTF-8').writerow(csv_header)
                for count in range(0,len(requests_dict["time"])):
                    streams_data_temp = {}
                    streams_data_temp_csv = []
                    streams_data_temp["id"] = id
                    for type in requests_list:
                        if requests_dict[type] != None:
                            if type == "latlng":
                                streams_data_temp["lat"] = requests_dict[type][count][0]
                                streams_data_temp["lng"] = requests_dict[type][count][1]
                                streams_data_temp_csv += [requests_dict[type][count][0],requests_dict[type][count][1]]
                            else:
                                if type == "velocity_smooth":
                                    streams_data_temp["velocity_smooth"] = requests_dict["velocity_smooth"][count]*3.6
                                    streams_data_temp_csv += [requests_dict["velocity_smooth"][count]*3.6]
                                else:
                                    streams_data_temp[type] = requests_dict[type][count]
                                    streams_data_temp_csv += [requests_dict[type][count]]
                        else:
                            if type == "latlng":
                                streams_data_temp["lat"] = "Null"
                                streams_data_temp["lng"] = "Null"
                                streams_data_temp_csv += [0,0]
                            else:
                                streams_data_temp[type] = "Null"
                                streams_data_temp_csv += [0]
                    csv.writer(streams_csv,encoding='UTF-8').writerow(streams_data_temp_csv)
                    streams_data_list += eval('['+str(streams_data_temp)+']')

                with open(filepath+"/"+str(id)+"_streams.json","w") as streams_json:
                    json.dump(streams_data_list,streams_json)
                    streams_json.close()

                table = table | id_set
                plot_data(requests_dict,filepath)
                activities_direct = open(user_path+"/direct_table.csv","ab")#建立direct_table.csv
                csv.writer(activities_direct,encoding='UTF-8').writerow([id,filepath])
                activities_direct.close()
                activities_table = open(table_path,"w+b")
                csv.writer(activities_table,encoding='UTF-8').writerow(list(table))
                activities_table.close()
                streams_csv.close()
                print(people[2]+" "+people[3]+" 編號 : "+str(id)+" 的資料下載完成了唷～")
user_file.close()