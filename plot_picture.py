import matplotlib.pyplot as plt

def plot_picture(X,Y1,Y2,Xlim,Ylim1,Ylim2,xlable,Y1lable,Y2lable,Title,position,figure,IO_door):
    picture = figure.add_subplot(position)
    picture.plot(X, Y1)
    picture.set_xlabel(xlable)
    #picture.set_title(Title)
    picture.set_ylabel(Y1lable)
    #picture.legend(loc='upper right')
    if Xlim > 0:
        picture.set_xlim(0, Xlim)
    else:
        picture.set_xlim(0, 5)
    if Ylim1 > 0:
        picture.set_ylim(0, Ylim1)
    else:
        picture.set_ylim(0, 5)
    if IO_door == "outdoor":
        ax2 = picture.twinx()
        ax2.fill_between(X, 0, Y2, color='c', alpha= 0.5)
        ax2.set_ylabel(Y2lable)
        if Xlim > 0:
            ax2.set_xlim(0, Xlim)
        else:
            ax2.set_xlim(0, 5)
        if Ylim2 > 0:
            ax2.set_ylim(0, Ylim2)
        else:
            ax2.set_ylim(0, 5)

def plot_data(plot_data_list,savepath):
    figure1 = plt.figure(1,figsize=[20,10])
    figure2 = plt.figure(2,figsize=[20,10])
    figure1.subplots_adjust(top = 0.95 , bottom = 0.05)
    figure2.subplots_adjust(top = 0.95 , bottom = 0.05)

    if plot_data_list["altitude"] == None or plot_data_list["altitude"] == []:
        IO_door = "indoor"
        altitude_limit = 250
    else:
        IO_door = "outdoor"
        if max(plot_data_list["altitude"]) < 250:
            altitude_limit = 250
        else:
            altitude_limit = max(plot_data_list["altitude"])*1.1

    if plot_data_list["time"] == None or plot_data_list["time"] == []:
        time_exist = False
    else:
        time_exist = True
        time_limit = max(plot_data_list["time"])

    if plot_data_list["distance"] == None or plot_data_list["distance"] == []:
        distance_exist = False
    else:
        distance_exist = True
        for x in range(0,len(plot_data_list["distance"])):
            plot_data_list["distance"][x] /= 1000
        distance_limit = max(plot_data_list["distance"])

    if plot_data_list["heartrate"] != None and plot_data_list["heartrate"] != []:
        heartrate_limit = 220
        if time_exist:
            plot_picture(plot_data_list["time"],plot_data_list["heartrate"],plot_data_list["altitude"],time_limit,heartrate_limit,altitude_limit,"Time(sec)","Heartrate(bpm)","Altitude(m)","HR(bpm) + Altitude(m)",311,figure1,IO_door)
        if distance_exist:
            plot_picture(plot_data_list["distance"],plot_data_list["heartrate"],plot_data_list["altitude"],distance_limit,heartrate_limit,altitude_limit,"Distance(km)","Heartrate(bpm)","Altitude(m)","HR(bpm) + Altitude(m)",311,figure2,IO_door)
    if plot_data_list["velocity_smooth"] != None and plot_data_list["velocity_smooth"] != []:
        for x in range(0,len(plot_data_list["velocity_smooth"])):
            plot_data_list["velocity_smooth"][x] *= 3.6
        speed_limit = max(plot_data_list["velocity_smooth"])*1.1
        if time_exist:
            plot_picture(plot_data_list["time"],plot_data_list["velocity_smooth"],plot_data_list["altitude"],time_limit,speed_limit,altitude_limit,"Time(sec)","Speed(km/hr)","Altitude(m)","Speed(km/hr) + Altitude(m)",312,figure1,IO_door)
        if distance_exist:
            plot_picture(plot_data_list["distance"],plot_data_list["velocity_smooth"],plot_data_list["altitude"],distance_limit,speed_limit,altitude_limit,"Distance(km)","Speed(km/hr)","Altitude(m)","Speed(km/hr) + Altitude(m)",312,figure2,IO_door)
    if plot_data_list["grade_smooth"] != None and plot_data_list["grade_smooth"] != []:
        grade_smooth_limit = max(plot_data_list["grade_smooth"])*1.1
        if time_exist:
            plot_picture(plot_data_list["time"],plot_data_list["grade_smooth"],plot_data_list["altitude"],time_limit,grade_smooth_limit,altitude_limit,"Time(sec)","grade_smooth(%)","Altitude(m)","grade_smooth(%) + Altitude(m)",313,figure1,IO_door)
        if distance_exist:
            plot_picture(plot_data_list["distance"],plot_data_list["grade_smooth"],plot_data_list["altitude"],distance_limit,grade_smooth_limit,altitude_limit,"Distance(km)","grade_smooth(%)","Altitude(m)","grade_smooth(%) + Altitude(m)",313,figure2,IO_door)
    if plot_data_list["cadence"] != None or plot_data_list["temp"] != None or plot_data_list["watts"] != None:
        figure3 = plt.figure(3,figsize=[20,10])
        figure4 = plt.figure(4,figsize=[20,10])
        figure3.subplots_adjust(top = 0.95 , bottom = 0.05)
        figure4.subplots_adjust(top = 0.95 , bottom = 0.05)
        if plot_data_list["cadence"] != None and plot_data_list["cadence"] != []:
            cadence_limit = max(plot_data_list["cadence"])*1.1
            if time_exist:
                plot_picture(plot_data_list["time"],plot_data_list["cadence"],plot_data_list["altitude"],time_limit,cadence_limit,altitude_limit,"Time(sec)","cadence(rpm)","Altitude(m)","cadence(rpm) + Altitude(m)",311,figure3,IO_door)
            if distance_exist:
                plot_picture(plot_data_list["distance"],plot_data_list["cadence"],plot_data_list["altitude"],distance_limit,cadence_limit,altitude_limit,"Distance(km)","cadence(rpm)","Altitude(m)","cadence(rpm) + Altitude(m)",311,figure4,IO_door)
        if plot_data_list["temp"] != None and plot_data_list["temp"] != []:
            temp_limit = max(plot_data_list["temp"])*1.1
            if time_exist:
                plot_picture(plot_data_list["time"],plot_data_list["temp"],plot_data_list["altitude"],time_limit,temp_limit,altitude_limit,"Time(sec)","Temperature(C)","Altitude(m)","Temperature(C) + Altitude(m)",312,figure3,IO_door)
            if distance_exist:
                plot_picture(plot_data_list["distance"],plot_data_list["temp"],plot_data_list["altitude"],distance_limit,temp_limit,altitude_limit,"Distance(km)","Temperature(C)","Altitude(m)","Temperature(C) + Altitude(m)",312,figure4,IO_door)
        if plot_data_list["watts"] != None and plot_data_list["watts"] != []:
            for x in range(0,len(plot_data_list["watts"])):
                if plot_data_list["watts"][x] == None:
                    plot_data_list["watts"][x] = -10
            watts_limit = max(plot_data_list["watts"])*1.1
            if time_exist:
                plot_picture(plot_data_list["time"],plot_data_list["watts"],plot_data_list["altitude"],time_limit,watts_limit,altitude_limit,"Time(sec)","Watts(W)","Altitude(m)","Watts(W)  + Altitude(m)",313,figure3,IO_door)
            if distance_exist:
                plot_picture(plot_data_list["distance"],plot_data_list["watts"],plot_data_list["altitude"],distance_limit,watts_limit,altitude_limit,"Distance(km)","Watts(W)","Altitude(m)","Watts(W)  + Altitude(m)",313,figure4,IO_door)
        figure3.savefig(savepath+"/Time_pic2.png",dpi=300,format="png")
        figure4.savefig(savepath+"/Distance_pic2.png",dpi=300,format="png")
        plt.close(3)
        plt.close(4)
    figure1.savefig(savepath+"/Time_pic.png",dpi=300,format="png")
    figure2.savefig(savepath+"/Distance_pic.png",dpi=300,format="png")
    plt.close(1)
    plt.close(2)