# -*- coding: utf-8 -*-
"""
.. module:: strava_crawler
   :synopsis: 此為用來全自動抓取 STRAVA 上使用者資料的程式。

.. moduleauthor:: Sean Hsu

"""
import os,json
from plot_picture import *
from support_function import *

def main():
    """
    此為主程式，主要功能如下:

        1. 抓取某使用者之 activities 資料，並分筆儲存成 activities.json 檔案
        2. 由 1. 所得之 activities ID 抓取該筆 activities 之 streams 資料分解並儲存為 ID_streams.csv , ID_streams.json 檔案
        3. 由 streams 分解出之資料繪製成圖 ( Distance 為 x 軸 - Distance_pic.png , Time 為 x 軸 - Time_pic.png )

    注意 : 以上所有功能所儲存之檔案，均儲存於同一資料夾，且該資料夾之路徑為 -- 使用者名稱 / type_id_distance_speed \n
            例 : Judith.Hsiang / Run_455904370_4.58km_8.41kmph_143bpm
                 曉春.賴 / Ride_452655005_49.87km_16.12kmph

    """
    com_filepath = "C:/Users/sean/desktop/strava_raw_data/" #檔案讀存路徑
    user_file = open(com_filepath+"strava_user.csv","rb") #讀取使用者資訊
    com_url = 'https://www.strava.com/api/v3/' # API路徑
    user = []  # 將user ID放入,可指定使用者,空白視為全選
    # user = ["523691"]  # scott

    for people in csv.reader(user_file,encoding='utf-8'):
        if ( user == [] or people[10] in user ):# 判斷此user是否在限制名單內,若名單為空則視為不限制user
            print("User ID: " + people[10] + " START")

            header = {'Authorization': 'Bearer '+people[1]} #將token加在header中
            try:#處理Requests上限問題
                while(True):
                    activities_mes = requests.get(com_url+"activities", headers=header).json()
                    error = activities_mes["errors"] #這行成功則表示Requests達到上限,錯誤則表示Requests正常,跳到except執行
                    print("Activities requests occur Rate limit , wait 180 second")
                    time.sleep(180)
            except:
                None

            user_path = com_filepath+people[2]+"."+people[3]
            if not os.path.exists(user_path): #建立使用者專屬資料夾
                os.makedirs(user_path)

            table = read_table(user_path+"/activities_table.csv") #讀取使用者 activities_table 中的資料

            for activities in activities_mes:

                id = activities["id"]
                if(str(id) not in table): # 判斷此筆activities資料是否已經存在
                    time_start = time.time()
                    average_speed = activities["average_speed"]*3.6 # 將 公尺/秒 轉換為 公里/小時
                    distance  = activities["distance"]/1000 # 將 m 轉換為 km
                    type_name = activities["type"]

                    if (activities["has_heartrate"] == True):
                        average_heartrate = activities["average_heartrate"]
                        filepath = user_path+"/"+type_name+"_"+str(id)+"_"+str('%.2f' % distance)+"km_"+str('%.2f' % average_speed)+"kmph_"+str('%d' % average_heartrate)+"bpm" # 資料夾命名規則 type_id_distance_speed
                    else:
                        filepath = user_path+"/"+type_name+"_"+str(id)+"_"+str('%.2f' % distance)+"km_"+str('%.2f' % average_speed)+"kmph"

                    if not os.path.exists(filepath):
                        os.makedirs(filepath)

                    requests_data = streams_requests(id,com_url,header) # 依照ID編號 Requests 該 Streams 的所有資料並分解出Data部分再回傳

                    streams_json_list,streams_csv_list = analysis_data(id,requests_data) # 將requests得到的資料分解成 .json 格式並回傳,同時將其寫入到.csv 檔中

                    data_plot(requests_data,filepath) # 繪製圖表並輸出成.png檔案

                    #以下為檔案輸出部分
                    csv_header = ['time','lat','lng','distance','altitude','velocity_smooth','heartrate','cadence','watts','temp','grade_smooth']
                    with open(filepath+"/"+str(id)+"_streams.csv","ab") as streams_csv:
                        csv.writer(streams_csv).writerow(csv_header) # 將header寫入到.csv檔中
                        csv.writer(streams_csv).writerows(streams_csv_list)#將分解完的資料存入.csv中
                        streams_csv.close()
                    with open(filepath+"/activities.json","w") as activities_json:#將單筆 activities 的資料寫入 .json 檔中
                        json.dump(activities,activities_json)
                        activities_json.close()
                    with open(filepath+"/"+str(id)+"_streams.json","w") as streams_json:#將分解完的資料存入 .json 檔中
                        json.dump(streams_json_list,streams_json)
                        streams_json.close()
                    with open(filepath+"/"+"strava_stream.json","w") as streams_json:#compatible with louie's format
                        json.dump(streams_json_list,streams_json)
                        streams_json.close()
                    with open(user_path+"/direct_table.csv","ab") as activities_direct:#建立direct_table.csv
                        csv.writer(activities_direct).writerow([id,filepath])#紀錄檔案路徑,以後讀取檔案時使用
                        activities_direct.close()
                    table += [id] #在table中加入最新的 activities ID
                    with open(user_path+"/activities_table.csv","w+b") as activities_table:
                        csv.writer(activities_table).writerow(table)#將table寫入檔案中
                        activities_table.close()
                    time_stop = time.time()
                    if (activities["has_heartrate"] == True):
                        print("ID : " + str(id) + " finished download   COST: "+str('%.2f' % (float(time_stop-time_start)%180))+" second, has_heartrate")
                    else:
                        print("ID : " + str(id) + " finished download   COST: "+str('%.2f' % (float(time_stop-time_start)%180))+" second")
    user_file.close()

main()