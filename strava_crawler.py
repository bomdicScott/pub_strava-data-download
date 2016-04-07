#-​*- coding: utf-8 -*​-
import os,json
from plot_picture import *
from support_function import *

com_filepath = "C:/users/sean/desktop/bOMDIC/" #檔案讀存路徑
user_file = open(com_filepath+"strava_user.csv","rb") #讀取使用者資訊
com_url = 'https://www.strava.com/api/v3/' # API路徑
user = []#將user ID放入,可指定使用者,空白視為全選

for people in csv.reader(user_file,encoding='utf-8'):
    if ( user == [] or people[10] in user ):# 判斷此user是否在限制名單內,若名單為空則視為不限制user
        print("User ID: " + people[10] + " START")

        header = {'Authorization': 'Bearer '+people[1]} #將token加在header中
        try:#處理Requests上限問題
            while(True):
                activities_mes = requests.get(com_url+"activities", headers=header).json()
                error = activities_mes["errors"] #這行成功則表示Requests達到上限,錯誤則表示Requests正常,跳到except執行
                print("Rate limit , wait 180 second")
                time.sleep(180)
        except:
            None

        user_path = com_filepath+people[2]+"."+people[3]
        if not os.path.exists(user_path): #建立使用者專屬資料夾
            os.makedirs(user_path)

        table = read_table(user_path+"/activities_table.csv") #讀取使用者 activities_table 中的資料

        for activities in activities_mes:
            id = activities["id"]
            if(id not in table): # 判斷此筆activities資料是否已經存在
                average_speed = activities["average_speed"]*3.6 # 將 公尺/秒 轉換為 公里/小時
                distance  = activities["distance"]/100 # 將 m 轉換為 km
                type_name = activities["type"]
                filepath = user_path+"/"+type_name+"_"+str(id)+"_"+str('%.2f' % distance)+"_"+str('%.2f' % average_speed) # 資料夾命名規則 type_id_distance_speed
                if not os.path.exists(filepath):
                    os.makedirs(filepath)

                requests_list = ['time','latlng','distance','altitude','velocity_smooth','heartrate','cadence','watts','temp','grade_smooth']
                requests_data = streams_requests(id,requests_list,com_url,header) # 依照requests_list中的參數依序requests得到結果並回傳資料

                streams_data_list,streams_data_list_csv = analysis_data(id,requests_data) # 將requests得到的資料分解成 .json 格式並回傳,同時將其寫入到.csv 檔中

                plot_data(requests_data,filepath) # 繪製圖表並輸出成.png檔案

                #以下為檔案輸出部分
                csv_header = ['time','lat','lng','distance','altitude','velocity_smooth','heartrate','cadence','watts','temp','grade_smooth']
                with open(filepath+"/"+str(id)+"_streams.csv","ab") as streams_csv:
                    csv.writer(streams_csv).writerow(csv_header) # 將header寫入到.csv檔中
                    csv.writer(streams_csv).writerows(streams_data_list_csv)#將分解完的資料存入.csv中
                    streams_csv.close()
                with open(filepath+"/activities.json","w") as activities_json:#將單筆 activities 的資料寫入 .json 檔中
                    json.dump(activities,activities_json)
                    activities_json.close()
                with open(filepath+"/"+str(id)+"_streams.json","w") as streams_json:#將分解完的資料存入 .json 檔中
                    json.dump(streams_data_list,streams_json)
                    streams_json.close()
                with open(user_path+"/direct_table.csv","ab") as activities_direct:#建立direct_table.csv
                    csv.writer(activities_direct).writerow([id,filepath])#紀錄檔案路徑,以後讀取檔案時使用
                    activities_direct.close()
                table += [id] #在table中加入最新的 activities ID
                with open(user_path+"/activities_table.csv","w+b") as activities_table:
                    csv.writer(activities_table).writerow(table)#將table寫入檔案中
                    activities_table.close()

                print("ID : " + str(id) + " date finished download") # YA!!! 下載完了
user_file.close()