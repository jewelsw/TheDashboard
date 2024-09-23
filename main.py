import PySimpleGUI as sg
import math

sg.change_look_and_feel('DarkBlue')

# Window 1 layout
layout = [
            [sg.Text('Dashboard',size=(20,1),font=('Helvetica',20)), sg.Text('      ', key='-OUTPUT-')],
            [sg.Button('Trip Computer',size=(15,2),font=('Helvetica',25)), sg.Button('Radio',size=(15,2),font=('Helvetica',25)), sg.Button('Weather',size=(15,2),font=('Helvetica',25)), sg.Button('Clock',size=(15,2),font=('Helvetica',25))],
            [sg.Text(' ')],
            [sg.Button('Temperature Control',size=(15,2),font=('Helvetica',25)), sg.Button('Music Player',size=(15,2),font=('Helvetica',25)), sg.Button('Garage Door',size=(15,2),font=('Helvetica',25)), sg.Button('Exit',size=(15,2),font=('Helvetica',25))]

         ]

window = sg.Window('Car', layout, grab_anywhere=True, location=(80,60))
win2_active = False
i=0
while True:             # Event Loop
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
        break
    if event != sg.TIMEOUT_KEY:
        print(i, event, values)
    if event == 'Exit':
        window.close()
    elif event == 'Popup':
        sg.popup('This is a BLOCKING popup','all windows remain inactive while popup active', grab_anywhere=True)
    i+=1
    if event == 'Temperature Control':     # only run if not already showing a window2
        win2_active = True
        # window 2 layout - note - must be "new" every time a window is created
        layout2 = [[sg.Text('Temperature(F°)',size=(20,1),font=('Helvetica',20)), sg.Text('', key='-OUTPUT-')],
          [sg.T('60',size=(4,1), key='-LEFT-'),
           [sg.Text(" ")],
           sg.Slider((60,90), key='-SLIDER-', orientation='h', enable_events=True, disable_number_display=True),
           sg.T('90', size=(4,1), key='-RIGHT-')],
            [sg.Text(" ")],
            [sg.Text(" ")],
          [sg.Button('Show'), sg.Button('Exit')]
                ]
        window2 = sg.Window('Window 2', layout2, grab_anywhere=True)
    # Read window 2's events.  Must use timeout of 0
    if win2_active:
        # print("reading 2")
        event, values = window2.read(timeout=100)
        # print("win2 ", event)
        if event != sg.TIMEOUT_KEY:
            print("win2 ", event)
        if event == 'Exit' or event is None:
            # print("Closing window 2", event)
            win2_active = False
            window2.close()
        if event == 'Show':
            sg.popup('The temperature is:', values["-SLIDER-"])
    if event == 'Music Player':
        from pygame import mixer
        import PySimpleGUI as sg
        import os
        import sys

        mixer.init()

        path = os.path.join(sys.path[0], 'Songs')


        def play_song(song):
            mixer.music.load(path + '/' + song)
            mixer.music.play()


        def stop_song():
            mixer.music.stop()


        def pause_song():
            mixer.music.pause()


        def resume_song():
            mixer.music.unpause()


        def change_volume(volume):
            volume /= 100
            mixer.music.set_volume(volume)


        songs = []

        for root, dirs, files in os.walk(path):
            for file in files:
                songs.append(file)

        # Sample PySimpleGUI code from their website. Will be edited later.
        sg.theme('Black')

        layout = [[sg.Text('Song: '), sg.Listbox(songs, size=(90, len(songs)), key='LISTBOX'), sg.Button('Play/Pause')],
                  [sg.Slider(range=(0, 100), default_value=100, orientation='horizontal', key='SLIDER')],
                  [sg.Button('Exit'), sg.Button('Previous Song'), sg.Button('Rewind'), sg.Button('Next Song'),
                   sg.Button('Stop')]]

        window_music = sg.Window('Music Player', layout, finalize=True)
        listbox = window_music['LISTBOX']

        status = 'n'
        current_song = ''
        previous_songs = []

        listbox.update(set_to_index=[0], scroll_to_index=0)  # Default to first item in list.
        current_volume = 100.0
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window_music.read()

            if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
                break
            elif event == 'Play/Pause' and status == 'n':  # Plays first song.
                current_song = values['LISTBOX'][0]
                play_song(current_song)
                status = 'playing'
                continue
            elif event == 'Play/Pause' and status == 'playing':  # Pauses current song.
                if values['LISTBOX'][0] != current_song:
                    stop_song()
                    previous_songs.append(current_song)
                    current_song = values['LISTBOX'][0]
                    play_song(values['LISTBOX'][0])
                    status = 'playing'
                    continue
                else:
                    pause_song()
                    status = 'paused'
                    continue
            elif event == 'Play/Pause' and status == 'paused':  # Resumes song.
                if values['LISTBOX'][0] != current_song:
                    stop_song()
                    previous_songs.append(current_song)
                    current_song = values['LISTBOX'][0]
                    play_song(current_song)
                    status = 'playing'
                    continue
                else:
                    resume_song()
                    status = 'playing'
                    continue

            elif event == 'Previous Song' and previous_songs:  # Plays the previously played song.
                stop_song()
                current_song = previous_songs.pop()
                listbox.update(set_to_index=songs.index(current_song), scroll_to_index=songs.index(current_song))
                if status == 'playing':
                    play_song(current_song)

            elif event == 'Rewind':  # Rewinds the current song.
                play_song(current_song)

            elif event == 'Next Song' and songs.index(current_song) + 1 < len(
                    songs):  # Selects the next song in the list.
                stop_song()
                previous_songs.append(current_song)
                listbox.update(set_to_index=songs.index(current_song) + 1)
                window.refresh()
                current_song = songs[songs.index(current_song) + 1]
                if status == 'playing':
                    play_song(current_song)

            elif event == 'Stop':  # Stops current song.
                stop_song()
                status = 'n'
                continue

            change_volume(values['SLIDER'])
            if event == 'Exit' or event is None:
                # print("Closing window 2", event)
                win2_active = False
                window2.close()

        window_music.close()

    if event == 'Garage Door':
        def garagedoorGUI():
            automatic_button = 'realautomatic.png'
            manual_button = 'realmanual.png'
            image_exit = 'Newexitbutton.png'

            def manual():
                open_button = 'newopen.png'
                close_button = 'newclose.png'

                status = sg.Text('status closed')
                layout = [[sg.Text('ManualMode', size=(17, 1), font=("Helvetica", 25))],
                          [sg.Button(image_filename=open_button, image_size=(250, 250), image_subsample=1, key='OPEN'),
                           sg.Button(image_filename=close_button, image_size=(250, 250), image_subsample=1,
                                     key='CLOSE'),
                           [status]]]
                window = sg.Window('ManualMode', layout)
                while True:
                    event, values = window.read()
                    if event == sg.WIN_CLOSED:
                        break
                    if event == 'OPEN':
                        status.update('status open')
                    if event == 'CLOSE':
                        status.update('status closed')

            def automatic():
                on_button = 'newon.png'
                off_button = 'newoff.png'
                exit_button = 'Newexitbutton.png'
                lnow = [2, 3]  # the location now
                lthen = [4, 5]  # the location 5 seconds ago
                x = lnow[0]
                y = lnow[1]
                x1 = lthen[0]
                y1 = lthen[1]

                lnowvalue = x + y
                lthenvalue = x1 + y1
                housepresetlocation = 0
                locationfromhouse = housepresetlocation + math.sqrt(x ** 2 + y ** 2)
                status = sg.Text('status closed')

                layout = [[sg.Text('Automatic', size=(17, 1), font=("Helvetica", 25))],
                          [sg.Button(image_filename=on_button, image_size=(250, 250), image_subsample=1, key='on'),
                           sg.Button(image_filename=off_button, image_size=(250, 250), image_subsample=1, key='off'),
                           [status]]]

                window = sg.Window('Automatic', layout)
                while True:
                    event, values = window.read()
                    if event == sg.WIN_CLOSED:
                        break
                    if event == 'on' and locationfromhouse <= 15:
                        if lnowvalue - lthenvalue < 0:
                            status.update('status open')
                        else:
                            status.update('status close')
                    if event == 'off':
                        manual()

            layout = [[sg.Text('Garage Door', size=(10, 1), font=("Helvetica", 45))],
                      [sg.Button(image_filename=manual_button, image_size=(175, 150), image_subsample=1,
                                 key='open manual GUI'),
                       sg.Button(image_filename=automatic_button, image_size=(175, 150), image_subsample=1,
                                 key='open automatic GUI'),
                       sg.Button(image_filename=image_exit, image_size=(175, 150), image_subsample=1, key='Exit1')]]

            window_garage = sg.Window('Garage Door', layout)
            while True:
                event, values = window_garage.read()
                if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
                    break
                if event == 'open manual GUI':
                    manual()
                if event == 'open automatic GUI':
                    automatic()
                if event == 'Exit1' or event is None:
                    window_garage.close()


        garagedoorGUI()
    if event == 'Trip Computer':
        import PySimpleGUI as sg

        sg.change_look_and_feel('LightBlue')

        # import threading
        # file/source to get distances traveled from car
        fp_dis = open('trip_total_distance.txt', 'r')

        # file/source to get fuel used from car
        fp_fuel = open('trip_fuel.txt', 'r')

        # file/source to total time from car
        fp_time = open('trip_total_time.txt', 'r')

        # working variables
        init_distance = int(fp_dis.readline())  # track trip distance read from file in miles
        trip_fuel = int(fp_fuel.readline())  # track fuel consumption read from file in gal
        trip_time_min = int(fp_time.readline())  # track time in mins
        toggle_metric_standard = 1  # boolean to track status - 0 is metric 1 is standard
        trip_fuel_unit = "gal"  # set initial unit to standard/gal
        trip_dist_unit = "miles"  # set initial unit to standard/mi

        # conversion constants
        conv_mile_km = 1.61
        conv_gal_lt = 3.79

        # calculations
        total_distance: int = init_distance
        trip_distance: int = total_distance
        trip_time_min: int = trip_time_min / 60

        layout = [[sg.Text('TRIP COMPUTER\n', font=('Helvetica', 30), text_color=('dark blue'))],
                  [sg.Text(f'FUEL ECONOMY:     {int(trip_fuel)} gal\n', size=(40, 3), font=('Helvetica', 25),
                           text_color=('black'), key='-FUEL-')],
                  [sg.Text(f'TOTAL DISTANCE:   {int(total_distance)} miles\n', size=(40, 3), font=('Helvetica', 25),
                           text_color=('black'), key='-TOTAL_DISTANCE-')],
                  [sg.Text(f'TRIP DISTANCE:    {int(trip_distance)} miles\n', size=(40, 3), font=('Helvetica', 25),
                           text_color=('black'), key='-TRIP_DISTANCE-')],
                  [sg.Text(f'TOTAL TIME:    {int(trip_time_min)} hours\n', size=(40, 3), font=('Helvetica', 25),
                           text_color=('black'), key='-TOTAL_TIME-')],
                  [sg.Button('RESET TRIP', size=(10, 2.5)),
                   sg.Button('TOGGLE STD-METRIC', size=(10.5, 2)),
                   sg.Button('REFRESH', size=(10, 2.5)),
                   sg.Button('DONE', size=(10, 2.5))]
                  ]

        # Create the window
        window_trip = sg.Window('Trip Computer', layout, margins=(10, 5))

        # threading

        # Create an event loop
        while True:
            event, values = window_trip.read()
            # End program if user closes window or
            # presses the DONE button
            if event == 'DONE' or event == sg.WIN_CLOSED:
                break
            elif event == 'RESET TRIP':
                trip_distance = 0
                window_trip['-TRIP_DISTANCE-'].update(f'TRIP DISTANCE:    {int(trip_distance)}\n')
            elif event == 'REFRESH':
                # threading.Timer(5.0, event).start()
                if toggle_metric_standard == 1:
                    total_distance = int(fp_dis.readline())  # track trip distance
                    trip_fuel = int(fp_fuel.readline())  # track fuel consumption
                    trip_time_min = int(fp_time.readline())  # track time in mins
                    trip_distance = total_distance - init_distance
                else:
                    total_distance = (int(fp_dis.readline()) / conv_mile_km)  # track trip distance
                    trip_fuel = (int(fp_fuel.readline()) / conv_gal_lt)  # track fuel consumption
                    trip_time_min = int(fp_time.readline())  # track time in mins
                    trip_distance = total_distance - (init_distance / conv_mile_km)
                window_trip['-FUEL-'].update(f'FUEL ECONOMY:     {int(trip_fuel)} {trip_fuel_unit}\n')
                window_trip['-TOTAL_DISTANCE-'].update(f'TOTAL DISTANCE:   {int(total_distance)} {trip_dist_unit}\n')
                window_trip['-TRIP_DISTANCE-'].update(f'TRIP DISTANCE:    {int(trip_distance)} {trip_dist_unit}\n')
                window_trip['-TOTAL_TIME-'].update(f'TOTAL TIME:     {int(int(trip_time_min) / 60)} hours')
            elif event == 'TOGGLE STD-METRIC':
                if toggle_metric_standard == 0:  # convert from metric to standard
                    toggle_metric_standard = 1
                    trip_fuel_unit = 'gal'
                    trip_dist_unit = 'miles'
                    trip_distance = trip_distance * conv_mile_km
                    trip_fuel = trip_fuel * conv_gal_lt
                    total_distance = total_distance * conv_mile_km
                    window_trip['-FUEL-'].update(f'FUEL ECONOMY:     {int(trip_fuel)} {trip_fuel_unit}\n')
                    window_trip['-TOTAL_DISTANCE-'].update(f'TOTAL DISTANCE:   {int(total_distance)} {trip_dist_unit}\n')
                    window_trip['-TRIP_DISTANCE-'].update(f'TRIP DISTANCE:    {int(trip_distance)} {trip_dist_unit}\n')
                else:  # convert from standard to metric
                    toggle_metric_standard = 0
                    trip_fuel_unit = 'liters'
                    trip_dist_unit = 'km'
                    trip_distance = trip_distance / conv_mile_km
                    trip_fuel = trip_fuel / conv_gal_lt
                    total_distance = total_distance / conv_mile_km
                    window_trip['-FUEL-'].update(f'FUEL ECONOMY:     {int(trip_fuel)} {trip_fuel_unit}\n')
                    window_trip['-TOTAL_DISTANCE-'].update(f'TOTAL DISTANCE:   {int(total_distance)} {trip_dist_unit}\n')
                    window_trip['-TRIP_DISTANCE-'].update(f'TRIP DISTANCE:    {int(trip_distance)} {trip_dist_unit}\n')

        window_trip.close()
    if event == 'Radio':
        import PySimpleGUI as sg
        import time

        fm_stations = ['97.3', '104.3', '106.5']
        am_stations = ['124.2', '212.1', '421.5']


        def update_status(status):
            if status == 'FM':
                return 'AM'
            else:
                return 'FM'


        fm_fav_1 = 0
        fm_fav_2 = 1
        fm_fav_3 = 2

        am_fav_1 = 0
        am_fav_2 = 1
        am_fav_3 = 2

        sg.theme('Black')

        layout = [[sg.Text('FM Station:', key='STATION TYPE'), sg.Text(fm_stations[0], key='STATION')],
                  [sg.Button(f'Fav 1: {fm_stations[fm_fav_1]}', key='FAV1'), sg.Button('Set Fav 1')],
                  [sg.Button(f'Fav 2: {fm_stations[fm_fav_2]}', key='FAV2'), sg.Button('Set Fav 2')],
                  [sg.Button(f'Fav 3: {fm_stations[fm_fav_3]}', key='FAV3'), sg.Button('Set Fav 3')],
                  [sg.Button('Exit'), sg.Button('AM', key='STATION UPDATE'), sg.Button('Next Station')]]

        window_radio = sg.Window('Radio', layout, finalize=True)
        current_station = window_radio['STATION']

        status = 'FM'


        def update_favorites(status):
            if status == 'FM':
                window_radio['FAV1'].update(f'Fav 1: {fm_stations[fm_fav_1]}')
                window_radio['FAV2'].update(f'Fav 2: {fm_stations[fm_fav_2]}')
                window_radio['FAV3'].update(f'Fav 3: {fm_stations[fm_fav_3]}')
            else:
                window_radio['FAV1'].update(f'Fav 1: {am_stations[am_fav_1]}')
                window_radio['FAV2'].update(f'Fav 2: {am_stations[am_fav_2]}')
                window_radio['FAV3'].update(f'Fav 3: {am_stations[am_fav_3]}')


        while True:
            event, values = window_radio.read()

            if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
                break

            elif event == 'STATION UPDATE':
                window_radio['STATION UPDATE'].update(status)
                status = update_status(status)
                window_radio['STATION TYPE'].update(f'{status} Station:')

                if status == 'FM':
                    current_station.update(fm_stations[0])
                    update_favorites(status)
                else:
                    current_station.update(am_stations[0])
                    update_favorites(status)

            elif event == 'Next Station' and status == 'FM':
                station = current_station.get()
                index = fm_stations.index(station)
                if index != len(fm_stations) - 1:
                    current_station.update(fm_stations[index + 1])
                else:
                    current_station.update(fm_stations[0])
            elif event == 'Next Station' and status == 'AM':
                station = current_station.get()
                index = am_stations.index(station)
                if index != len(am_stations) - 1:
                    current_station.update(am_stations[index + 1])
                else:
                    current_station.update(am_stations[0])

            elif event == 'FAV1':
                if status == 'FM':
                    current_station.update(fm_stations[fm_fav_1])
                else:
                    current_station.update(am_stations[am_fav_1])
            elif event == 'Set Fav 1':
                if status == 'FM':
                    fm_fav_1 = fm_stations.index(current_station.get())
                else:
                    am_fav_1 = am_stations.index(current_station.get())

            elif event == 'FAV2':
                if status == 'FM':
                    current_station.update(fm_stations[fm_fav_2])
                else:
                    current_station.update(am_stations[am_fav_2])
            elif event == 'Set Fav 2':
                if status == 'FM':
                    fm_fav_2 = fm_stations.index(current_station.get())
                else:
                    am_fav_2 = am_stations.index(current_station.get())

            elif event == 'FAV3':
                if status == 'FM':
                    current_station.update(fm_stations[fm_fav_3])
                else:
                    current_station.update(am_stations[am_fav_3])
            elif event == 'Set Fav 3':
                if status == 'FM':
                    fm_fav_3 = fm_stations.index(current_station.get())
                    window['FAV3'].update(f'Fav 3: {fm_stations[fm_fav_3]}')
                else:
                    am_fav_3 = am_stations.index(current_station.get())

            update_favorites(status)

        window_radio.close()
    if event == 'Weather':
        import PySimpleGUI as sg

        sg.theme('BlueMono')
        layout1 = [[sg.Text('Weather for November 13th to November 19th')],
                   [sg.Button('Sunday'), sg.Button('Monday'), sg.Button('Tuesday'), sg.Button('Wednesday'),
                    sg.Button('Thursday'), sg.Button('Friday'), sg.Button('Saturday')],
                   [sg.Button('Close')]]
        window_weather = sg.Window('Weather Application', layout1)
        while True:
            event, values = window_weather.read()
            if event == 'Sunday':
                sg.theme('BlueMono')
                layout = [[sg.Text('Weather for Sunday, November 13th')],
                          [sg.Text('High of 10.5°C (51°F), and a Low of 1.1°C (34°F), With a 0% Chance of Rain')],
                          [sg.Text(
                              'Wind Speeds of 14-23 Kph (9-14 Mph) During the Day, Slowing Down to 10-14 Kph (6-9 Mph) at Night')],
                          [sg.Text(
                              'Humidity at 80% in the Morning, Dropping to 44% Throughout the Day, Until 3pm, Where it Starts to Rise Back to 80%')],
                          [sg.Text('12am'), sg.Text('1am'), sg.Text('2am'), sg.Text('3am'), sg.Text('4am'),
                           sg.Text('5am'), sg.Text('6am'), sg.Text('7am'), sg.Text('8am'), sg.Text('9am'),
                           sg.Text('10am'), sg.Text('11am'), sg.Text('12pm'), sg.Text('1pm'), sg.Text('2pm'),
                           sg.Text('3pm'), sg.Text('4pm'), sg.Text('5pm'), sg.Text(' 6pm'), sg.Text(' 7pm'),
                           sg.Text(' 8pm'), sg.Text(' 9pm'), sg.Text('10pm'), sg.Text('11pm'), ],
                          [sg.Text('04°c '), sg.Text('04°c'), sg.Text('04°c'), sg.Text('03°c'), sg.Text('03°c'),
                           sg.Text('02°c'), sg.Text('02°c'), sg.Text('03°c'), sg.Text('04°c'), sg.Text('05°c'),
                           sg.Text('08°c'), sg.Text(' 09°c'), sg.Text('10°c'), sg.Text(' 10°c'), sg.Text('10°c'),
                           sg.Text(' 09°c'), sg.Text('07°c'), sg.Text('04°c'), sg.Text('03°c'), sg.Text(' 03°c'),
                           sg.Text('02°c'), sg.Text(' 01°c'), sg.Text(' 01°c'), sg.Text(' 01°c')],
                          [sg.Text('40°F'), sg.Text('40°F'), sg.Text('40°F'), sg.Text('38°F'), sg.Text('37°F'),
                           sg.Text('35°F'), sg.Text('35°F'), sg.Text('37°F'), sg.Text('40°F'), sg.Text('42°F'),
                           sg.Text('46°F'), sg.Text('48°F'), sg.Text('50°F'), sg.Text('51°F'), sg.Text('51°F'),
                           sg.Text('49°F'), sg.Text('45°F'), sg.Text('40°F'), sg.Text('38°F'), sg.Text('37°F'),
                           sg.Text('36°F'), sg.Text(' 34°F'), sg.Text(' 34°F'), sg.Text(' 33°F')],
                          [sg.Button('Close')]]
                window_weather = sg.Window('Sunday Weather', layout)
            if event == 'Monday':
                sg.theme('BlueMono')
                layout = [[sg.Text('Weather for Monday, November 14th')],
                          [sg.Text('High of 15°C (59°F), and a Low of 0.6°C (33°F), With a 3% Chance of Rain')],
                          [sg.Text(
                              'Wind Speeds of 8-21 Kph (5-13 Mph) During the Day, Remaining Stagnant With 13-19 Kph (8-12 Mph) at Night')],
                          [sg.Text(
                              'Humidity at 80% in the Morning, Dropping to 50%-55% Throughout the Day, Until 4pm, Where it Starts to Rise Back to 71%')],
                          [sg.Text('12am'), sg.Text('1am'), sg.Text('2am'), sg.Text('3am'), sg.Text('4am'),
                           sg.Text('5am'), sg.Text('6am'), sg.Text('7am'), sg.Text('8am'), sg.Text('9am'),
                           sg.Text('10am'), sg.Text('11am'), sg.Text('12pm'), sg.Text('1pm'), sg.Text('2pm'),
                           sg.Text('3pm'), sg.Text('4pm'), sg.Text('5pm'), sg.Text(' 6pm'), sg.Text(' 7pm'),
                           sg.Text(' 8pm'), sg.Text(' 9pm'), sg.Text('10pm'), sg.Text('11pm'), ],
                          [sg.Text('01°c '), sg.Text('01°c'), sg.Text('01°c'), sg.Text('01°c'), sg.Text('01°c'),
                           sg.Text('01°c'), sg.Text('01°c'), sg.Text('04°c'), sg.Text('06°c'), sg.Text('08°c'),
                           sg.Text('12°c'), sg.Text(' 13°c'), sg.Text('14°c'), sg.Text(' 14°c'), sg.Text('15°c'),
                           sg.Text(' 14°c'), sg.Text('11°c'), sg.Text('11°c'), sg.Text('11°c'), sg.Text(' 11°c'),
                           sg.Text('11°c'), sg.Text(' 11°c'), sg.Text(' 11°c'), sg.Text(' 11°c')],
                          [sg.Text('33°F'), sg.Text('33°F'), sg.Text('33°F'), sg.Text('34°F'), sg.Text('34°F'),
                           sg.Text('34°F'), sg.Text('34°F'), sg.Text('39°F'), sg.Text('43°F'), sg.Text('47°F'),
                           sg.Text('53°F'), sg.Text('56°F'), sg.Text('57°F'), sg.Text('58°F'), sg.Text('59°F'),
                           sg.Text('57°F'), sg.Text('51°F'), sg.Text('51°F'), sg.Text('51°F'), sg.Text('51°F'),
                           sg.Text('51°F'), sg.Text(' 52°F'), sg.Text(' 51°F'), sg.Text(' 51°F')],
                          [sg.Button('Close')]]
                window_weather = sg.Window('Monday Weather', layout)
            if event == 'Tuesday':
                sg.theme('BlueMono')
                layout = [[sg.Text('Weather for Tuesday, November 15th')],
                          [sg.Text('High of 13.9°C (57°F), and a Low of 9.4°C (49°F), With a 94% Chance of Rain')],
                          [sg.Text(
                              'Wind Speeds of 8-16 Kph (5-10 Mph) During the Day, Increasing Up to 13-23 Kph (8-14 Mph) at Night')],
                          [sg.Text(
                              'Humidity at 94% in the Morning, Rising to 98% Throughout the Day, Until 6pm, Where it Starts to Drop to 92%')],
                          [sg.Text('12am'), sg.Text('1am'), sg.Text('2am'), sg.Text('3am'), sg.Text('4am'),
                           sg.Text('5am'),
                           sg.Text('6am'), sg.Text('7am'), sg.Text('8am'), sg.Text('9am'), sg.Text('10am'),
                           sg.Text('11am'),
                           sg.Text('12pm'), sg.Text('1pm'), sg.Text('2pm'), sg.Text('3pm'), sg.Text('4pm'),
                           sg.Text('5pm'),
                           sg.Text(' 6pm'), sg.Text(' 7pm'), sg.Text(' 8pm'), sg.Text(' 9pm'), sg.Text('10pm'),
                           sg.Text('11pm'), ],
                          [sg.Text('11°c '), sg.Text('09°c'), sg.Text('09°c'), sg.Text('09°c'), sg.Text('09°c'),
                           sg.Text('09°c'), sg.Text('10°c'), sg.Text('11°c'), sg.Text('11°c'), sg.Text('11°c'),
                           sg.Text('11°c'),
                           sg.Text(' 11°c'), sg.Text('12°c'), sg.Text(' 12°c'), sg.Text('13°c'), sg.Text(' 13°c'),
                           sg.Text('13°c'), sg.Text('13°c'), sg.Text('14°c'), sg.Text(' 13°c'), sg.Text('13°c'),
                           sg.Text(' 12°c'), sg.Text(' 10°c'), sg.Text(' 09°c')],
                          [sg.Text('51°F'), sg.Text('48°F'), sg.Text('48°F'), sg.Text('48°F'), sg.Text('49°F'),
                           sg.Text('48°F'),
                           sg.Text('50°F'), sg.Text('51°F'), sg.Text('52°F'), sg.Text('52°F'), sg.Text('52°F'),
                           sg.Text('52°F'),
                           sg.Text('54°F'), sg.Text('54°F'), sg.Text('55°F'), sg.Text('55°F'), sg.Text('55°F'),
                           sg.Text('56°F'),
                           sg.Text('57°F'), sg.Text('56°F'), sg.Text('55°F'), sg.Text(' 54°F'), sg.Text(' 50°F'),
                           sg.Text(' 49°F')],
                          [sg.Button('Close')]]
                window_weather = sg.Window('Tuesday Weather', layout)
            if event == 'Wednesday':
                sg.theme('BlueMono')
                layout = [[sg.Text('Weather for Wednesday, November 16th')],
                          [sg.Text('High of 10.5°C (51°F), and a Low of 4.4°C (40°F), With a 30% Chance of Rain')],
                          [sg.Text(
                              'Wind Speeds of 13-23 Kph (8-14 Mph) During the Day, Slowing Down to 5-13 Kph (3-8 Mph) at Night')],
                          [sg.Text(
                              'Humidity at 89% in the Morning, Dropping to 62% Throughout the Day, Until 6pm, Where it Starts to Rise Back to 76%')],
                          [sg.Text('12am'), sg.Text('1am'), sg.Text('2am'), sg.Text('3am'), sg.Text('4am'),
                           sg.Text('5am'),
                           sg.Text('6am'), sg.Text('7am'), sg.Text('8am'), sg.Text('9am'), sg.Text('10am'),
                           sg.Text('11am'),
                           sg.Text('12pm'), sg.Text('1pm'), sg.Text('2pm'), sg.Text('3pm'), sg.Text('4pm'),
                           sg.Text('5pm'),
                           sg.Text(' 6pm'), sg.Text(' 7pm'), sg.Text(' 8pm'), sg.Text(' 9pm'), sg.Text('10pm'),
                           sg.Text('11pm'), ],
                          [sg.Text('09°c '), sg.Text('08°c'), sg.Text('07°c'), sg.Text('07°c'), sg.Text('07°c'),
                           sg.Text('06°c'), sg.Text('06°c'), sg.Text('06°c'), sg.Text('05°c'), sg.Text('06°c'),
                           sg.Text('07°c'),
                           sg.Text(' 09°c'), sg.Text('10°c'), sg.Text(' 11°c'), sg.Text('10°c'), sg.Text(' 09°c'),
                           sg.Text('09°c'), sg.Text('07°c'), sg.Text('07°c'), sg.Text(' 07°c'), sg.Text('06°c'),
                           sg.Text(' 05°c'), sg.Text(' 05°c'), sg.Text(' 06°c')],
                          [sg.Text('48°F'), sg.Text('47°F'), sg.Text('46°F'), sg.Text('45°F'), sg.Text('45°F'),
                           sg.Text('43°F'),
                           sg.Text('43°F'), sg.Text('41°F'), sg.Text('40°F'), sg.Text('43°F'), sg.Text('45°F'),
                           sg.Text('48°F'),
                           sg.Text('50°F'), sg.Text('51°F'), sg.Text('50°F'), sg.Text('49°F'), sg.Text('48°F'),
                           sg.Text('45°F'),
                           sg.Text('44°F'), sg.Text('44°F'), sg.Text('43°F'), sg.Text(' 42°F'), sg.Text(' 41°F'),
                           sg.Text(' 43°F')],
                          [sg.Button('Close')]]
                window_weather = sg.Window('Wednesday Weather', layout)
            if event == 'Thursday':
                sg.theme('BlueMono')
                layout = [[sg.Text('Weather for Thursday, November 17th')],
                          [sg.Text('High of 10.0°C (50°F), and a Low of -2.2°C (28°F), With a 1% Chance of Rain')],
                          [sg.Text(
                              'Wind Speeds of 6-14 Kph (4-9 Mph) During the Day, Slowing Down to 8 Kph (5 Mph) at Night')],
                          [sg.Text(
                              'Humidity at ~83% All Day')],
                          [sg.Text('12am'), sg.Text('1am'), sg.Text('2am'), sg.Text('3am'), sg.Text('4am'),
                           sg.Text('5am'),
                           sg.Text('6am'), sg.Text('7am'), sg.Text('8am'), sg.Text('9am'), sg.Text('10am'),
                           sg.Text('11am'),
                           sg.Text('12pm'), sg.Text('1pm'), sg.Text('2pm'), sg.Text('3pm'), sg.Text('4pm'),
                           sg.Text('5pm'),
                           sg.Text(' 6pm'), sg.Text(' 7pm'), sg.Text(' 8pm'), sg.Text(' 9pm'), sg.Text('10pm'),
                           sg.Text('11pm'), ],
                          [sg.Text('03°c '), sg.Text('03°c'), sg.Text('03°c'), sg.Text('02°c'), sg.Text('02°c'),
                           sg.Text('02°c'), sg.Text('02°c'), sg.Text('03°c'), sg.Text('06°c'), sg.Text('08°c'),
                           sg.Text('09°c'),
                           sg.Text(' 10°c'), sg.Text('10°c'), sg.Text(' 10°c'), sg.Text('09°c'), sg.Text(' 08°c'),
                           sg.Text('07°c'), sg.Text('05°c'), sg.Text('04°c'), sg.Text(' 03°c'), sg.Text('02°c'),
                           sg.Text(' 02°c'), sg.Text(' 01°c'), sg.Text(' 01°c')],
                          [sg.Text('38°F'), sg.Text('37°F'), sg.Text('37°F'), sg.Text('36°F'), sg.Text('35°F'),
                           sg.Text('35°F'),
                           sg.Text('35°F'), sg.Text('38°F'), sg.Text('42°F'), sg.Text('46°F'), sg.Text('48°F'),
                           sg.Text('49°F'),
                           sg.Text('50°F'), sg.Text('49°F'), sg.Text('48°F'), sg.Text('47°F'), sg.Text('44°F'),
                           sg.Text('41°F'),
                           sg.Text('39°F'), sg.Text('37°F'), sg.Text('36°F'), sg.Text(' 35°F'), sg.Text(' 34°F'),
                           sg.Text(' 34°F')],
                          [sg.Button('Close')]]
                window_weather = sg.Window('Thursday Weather', layout)
            if event == 'Friday':
                sg.theme('BlueMono')
                layout = [[sg.Text('Weather for Friday, November 18th')],
                          [sg.Text('High of 12.8°C (55°F), and a Low of -1.1°C (30°F), With a 0% Chance of Rain')],
                          [sg.Text(
                              'Wind Speeds of 8-11 Kph (5-7 Mph) During the Day, Slowing Down to 5-10 Kph (3-6 Mph) at Night')],
                          [sg.Text(
                              'Humidity at 78% All Day')],
                          [sg.Text('12am'), sg.Text('1am'), sg.Text('2am'), sg.Text('3am'), sg.Text('4am'),
                           sg.Text('5am'),
                           sg.Text('6am'), sg.Text('7am'), sg.Text('8am'), sg.Text('9am'), sg.Text('10am'),
                           sg.Text('11am'),
                           sg.Text('12pm'), sg.Text('1pm'), sg.Text('2pm'), sg.Text('3pm'), sg.Text('4pm'),
                           sg.Text('5pm'),
                           sg.Text(' 6pm'), sg.Text(' 7pm'), sg.Text(' 8pm'), sg.Text(' 9pm'), sg.Text('10pm'),
                           sg.Text('11pm'), ],
                          [sg.Text('01°c '), sg.Text('01°c'), sg.Text('00°c'), sg.Text('01°c'), sg.Text('01°c'),
                           sg.Text('01°c'), sg.Text('00°c'), sg.Text('01°c'), sg.Text('02°c'), sg.Text('05°c'),
                           sg.Text('08°c'),
                           sg.Text(' 09°c'), sg.Text('11°c'), sg.Text(' 12°c'), sg.Text('12°c'), sg.Text(' 13°c'),
                           sg.Text('12°c'), sg.Text('09°c'), sg.Text('08°c'), sg.Text(' 06°c'), sg.Text('01°c'),
                           sg.Text(' 04°c'), sg.Text(' 04°c'), sg.Text(' 04°c')],
                          [sg.Text('34°F'), sg.Text('33°F'), sg.Text('32°F'), sg.Text('31°F'), sg.Text('31°F'),
                           sg.Text('31°F'),
                           sg.Text('30°F'), sg.Text('31°F'), sg.Text('36°F'), sg.Text('41°F'), sg.Text('46°F'),
                           sg.Text('49°F'),
                           sg.Text('52°F'), sg.Text('53°F'), sg.Text('54°F'), sg.Text('55°F'), sg.Text('53°F'),
                           sg.Text('48°F'),
                           sg.Text('46°F'), sg.Text('43°F'), sg.Text('41°F'), sg.Text(' 39°F'), sg.Text(' 40°F'),
                           sg.Text(' 40°F')],
                          [sg.Button('Close')]]
                window_weather = sg.Window('Friday Weather', layout)
            if event == 'Saturday':
                sg.theme('BlueMono')
                layout = [[sg.Text('Weather for Saturday, November 19th')],
                          [sg.Text('High of 1.7°C (35°F), and a Low of 13.3°C (56°F), With a 3% Chance of Rain')],
                          [sg.Text(
                              'Wind Speeds of 10-11 Kph (6-7 Mph) All Day')],
                          [sg.Text(
                              'Humidity at 80% in the Morning, Dropping to 42% Throughout the Day, Until 7pm, Where it Starts to Rise Back to 63%')],
                          [sg.Text('12am'), sg.Text('1am'), sg.Text('2am'), sg.Text('3am'), sg.Text('4am'),
                           sg.Text('5am'),
                           sg.Text('6am'), sg.Text('7am'), sg.Text('8am'), sg.Text('9am'), sg.Text('10am'),
                           sg.Text('11am'),
                           sg.Text('12pm'), sg.Text('1pm'), sg.Text('2pm'), sg.Text('3pm'), sg.Text('4pm'),
                           sg.Text('5pm'),
                           sg.Text(' 6pm'), sg.Text(' 7pm'), sg.Text(' 8pm'), sg.Text(' 9pm'), sg.Text('10pm'),
                           sg.Text('11pm'), ],
                          [sg.Text('04°c '), sg.Text('03°c'), sg.Text('03°c'), sg.Text('03°c'), sg.Text('02°c'),
                           sg.Text('02°c'), sg.Text('02°c'), sg.Text('06°c'), sg.Text('08°c'), sg.Text('11°c'),
                           sg.Text('12°c'),
                           sg.Text(' 13°c'), sg.Text('13°c'), sg.Text(' 13°c'), sg.Text('13°c'), sg.Text(' 11°c'),
                           sg.Text('09°c'), sg.Text('09°c'), sg.Text('08°c'), sg.Text(' 08°c'), sg.Text('08°c'),
                           sg.Text(' 08°c'), sg.Text(' 07°c'), sg.Text(' 07°c')],
                          [sg.Text('39°F'), sg.Text('38°F'), sg.Text('38°F'), sg.Text('37°F'), sg.Text('36°F'),
                           sg.Text('35°F'),
                           sg.Text('36°F'), sg.Text('42°F'), sg.Text('47°F'), sg.Text('51°F'), sg.Text('53°F'),
                           sg.Text('55°F'),
                           sg.Text('56°F'), sg.Text('56°F'), sg.Text('55°F'), sg.Text('52°F'), sg.Text('49°F'),
                           sg.Text('48°F'),
                           sg.Text('47°F'), sg.Text('47°F'), sg.Text('46°F'), sg.Text(' 46°F'), sg.Text(' 45°F'),
                           sg.Text(' 45°F')],
                          [sg.Button('Close')]]
                window_weather = sg.Window('Saturday Weather', layout)
            if event == sg.WIN_CLOSED or event == 'Close':
                break
        window_weather.close()
    if event == 'Clock':
        import PySimpleGUI as sg
        from tkinter import Tk
        from tkinter import Label
        import time
        import sys

        master = Tk()
        master.title("_")
        test_var=1

        def get_time():
            timeVar = time.strftime("%I:%M:%S %p")
            clock.config(text=timeVar)
            clock.after(1000, get_time)
            sg.theme("DefaultNoMoreNagging")
            layout = [[sg.Text(time.strftime("%I")), sg.Text(time.strftime("%M")), sg.Text(time.strftime("%S")),
                       sg.Text(time.strftime("%p")),sg.Button('Exit')]]
            window_time = sg.Window("Timer", layout)

            while True:

                event, values = window_time.read()
                if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
                    test_var = 2




        clock = Label(master, font=("Calibri", 1), bg="white", fg="white")
        clock.pack(),


        if test_var == 1:
            get_time()

        master.mainloop()

window.close()


