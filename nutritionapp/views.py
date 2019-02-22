from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *

from datetime import date
import math
import json
import pandas as pd
import numpy as np
import os
# Create your views here.
# powerplay_strikers_dict={}
# death_strikers_dict={}
# powerplay_heat_dict={}
# death_heat_dict={}
# powerplay_hurricanes_dict={}
# death_hurricanes_dict={}
# powerplay_renegades_dict={}
# death_renegades_dict={}
# powerplay_stars_dict={}
# death_stars_dict={}
# powerplay_scorchers_dict={}
# death_scorchers_dict={}
# powerplay_thunders_dict={}
# death_thunders_dict={}
# powerplay_sixers_dict={}
# death_sixers_dict={}
# dmode_strikers_dict={}
# dmode_heat_dict={}
# dmode_hurricanes_dict={}
# dmode_renegades_dict={}
# dmode_stars_dict={}
# dmode_scorchers_dict={}
# dmode_thunders_dict={}
# dmode_sixers_dict={}
# point6matrix=[]
# ballmatrix=[]
# matchmatrix=[]
#
# disbowltype_strikers_dict={}
# disbowltype_heat_dict={}
# disbowltype_hurricanes_dict={}
# disbowltype_renegades_dict={}
# disbowltype_stars_dict={}
# disbowltype_scorchers_dict={}
# disbowltype_thunders_dict={}
# disbowltype_sixers_dict={}
#
# strikers=[]
# heat=[]
# hurricanes=[]
# renegades=[]
# stars=[]
# scorchers=[]
# thunders=[]
# sixers=[]
# datapath= '/Users/sahiljajodia/nse-ml-hack/data.csv'
# datapath='C:\Users\Sarvesh\Desktop\Django Miniprojects\freefolkpro\nutritionapp\ballByball.csv'
# datapath2='C:\Users\Sarvesh\Desktop\Django Miniprojects\freefolkpro\nutritionapp\Match1.csv'

def index(request):
    return render(request, 'index.html')

def processing(request):
    # print(os.path.dirname(os.path.abspath(__file__)))
    datapath=os.path.dirname(os.path.abspath(__file__))+'\\Match1.csv'
    datapath2=os.path.dirname(os.path.abspath(__file__))+'\\ballByball.csv'
    datapath3=os.path.dirname(os.path.abspath(__file__))+'\\Player.csv'
    balldf=pd.read_csv(datapath2)
    matchdf=pd.read_csv(datapath)

    global ballmatrix
    ballmatrix=balldf.iloc[0:8271,[0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]]
    global matchmatrix
    matchmatrix=matchdf.iloc[:,[1,2,3,4,5,6,7,8,9,10]]

    ballmatrix['wicket_fielders']=ballmatrix['wicket_fielders'].fillna("")
    ballmatrix['wicket_player_out']=ballmatrix['wicket_player_out'].fillna("")

    for index,rows in ballmatrix.iterrows():
        fname=rows['Striker'].split()[0]
        lname=rows['Striker'].split()[1]
        fname=fname[0]
        name=fname+' '+lname
        ballmatrix.loc[index,'Striker']=name

        fname=rows['Bowler'].split()[0]
        lname=rows['Bowler'].split()[1]
        fname=fname[0]
        name=fname+' '+lname
        ballmatrix.loc[index,'Bowler']=name

        fname=rows['non_striker'].split()[0]
        lname=rows['non_striker'].split()[1]
        fname=fname[0]
        name=fname+' '+lname
        ballmatrix.loc[index,'non_striker']=name

        if(rows['wicket_fielders']!= ''):
            fname=rows['wicket_fielders'].split()[0]
            lname=rows['wicket_fielders'].split()[1]
            fname=fname[0]
            name=fname+' '+lname
            ballmatrix.loc[index,'wicket_fielders']=name

            if(rows['wicket_player_out']!=''):
                fname=rows['wicket_player_out'].split()[0]
                lname=rows['wicket_player_out'].split()[1]
                fname=fname[0]
                name=fname+' '+lname
                ballmatrix.loc[index,'wicket_player_out']=name

    playersdf=pd.read_csv(datapath3)

    updateballmatrix=ballmatrix
    updateballmatrix['Over']=updateballmatrix['Over'].apply(np.ceil)

    global strikers
    strikers=[rows['Player'] for index,rows in playersdf.iterrows() if rows['Team']=='Adelaide Strikers']
    global heat
    heat=[rows['Player'] for index,rows in playersdf.iterrows() if rows['Team']=='Brisbane Heat']
    global hurricanes
    hurricanes=[rows['Player'] for index,rows in playersdf.iterrows() if rows['Team']=='Hobart Hurricanes']
    global renegades
    renegades=[rows['Player'] for index,rows in playersdf.iterrows() if rows['Team']=='Melbourne Renegades']
    global stars
    stars=[rows['Player'] for index,rows in playersdf.iterrows() if rows['Team']=='Melbourne Stars']
    global scorchers
    scorchers=[rows['Player'] for index,rows in playersdf.iterrows() if rows['Team']=='Perth Scorchers']
    global thunders
    thunders=[rows['Player'] for index,rows in playersdf.iterrows() if rows['Team']=='Sydney Thunders']
    global sixers
    sixers=[rows['Player'] for index,rows in playersdf.iterrows() if rows['Team']=='Sydney Sixers']

    global powerplay_strikers_dict
    powerplay_strikers_dict={}
    for player in strikers:
        current_dict={'runs':0,'balls_faced':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker'] and rows['Over'] in [1,2,3,4,5,6]:
                current_dict['runs']+=rows['runs_batsman']
                current_dict['balls_faced']+=1
                if(current_dict['balls_faced']!=0):
                    current_dict['strike_rate']=(current_dict['runs']/current_dict['balls_faced'])*100
                else:
                    current_dict['strike_rate']=0
                    powerplay_strikers_dict[player]=current_dict

    global death_strikers_dict
    death_strikers_dict={}
    for player in strikers:
        current_dict={'runs':0,'balls_faced':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker'] and rows['Over'] in [16,17,18,19,20]:
                current_dict['runs']+=rows['runs_batsman']
                current_dict['balls_faced']+=1
        if(current_dict['balls_faced']!=0):
            current_dict['strike_rate']=(current_dict['runs']/current_dict['balls_faced'])*100
        else:
            current_dict['strike_rate']=0
        death_strikers_dict[player]=current_dict

    global powerplay_heat_dict
    powerplay_heat_dict={}
    for player in heat:
        current_dict={'runs':0,'balls_faced':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker'] and rows['Over'] in [1,2,3,4,5,6]:
                current_dict['runs']+=rows['runs_batsman']
                current_dict['balls_faced']+=1
        if(current_dict['balls_faced']!=0):
            current_dict['strike_rate']=(current_dict['runs']/current_dict['balls_faced'])*100
        else:
            current_dict['strike_rate']=0
        powerplay_heat_dict[player]=current_dict

    global death_heat_dict
    death_heat_dict={}
    for player in heat:
        current_dict={'runs':0,'balls_faced':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker'] and rows['Over'] in [16,17,18,19,20]:
                current_dict['runs']+=rows['runs_batsman']
                current_dict['balls_faced']+=1
        if(current_dict['balls_faced']!=0):
            current_dict['strike_rate']=(current_dict['runs']/current_dict['balls_faced'])*100
        else:
            current_dict['strike_rate']=0
        death_heat_dict[player]=current_dict

    global powerplay_hurricanes_dict
    powerplay_hurricanes_dict={}
    for player in hurricanes:
        current_dict={'runs':0,'balls_faced':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker'] and rows['Over'] in [1,2,3,4,5,6]:
                current_dict['runs']+=rows['runs_batsman']
                current_dict['balls_faced']+=1
        if(current_dict['balls_faced']!=0):
            current_dict['strike_rate']=(current_dict['runs']/current_dict['balls_faced'])*100
        else:
            current_dict['strike_rate']=0
        powerplay_hurricanes_dict[player]=current_dict

    global death_hurricanes_dict
    death_hurricanes_dict={}
    for player in hurricanes:
        current_dict={'runs':0,'balls_faced':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker'] and rows['Over'] in [16,17,18,19,20]:
                current_dict['runs']+=rows['runs_batsman']
                current_dict['balls_faced']+=1
        if(current_dict['balls_faced']!=0):
            current_dict['strike_rate']=(current_dict['runs']/current_dict['balls_faced'])*100
        else:
            current_dict['strike_rate']=0
        death_hurricanes_dict[player]=current_dict

    global powerplay_renegades_dict
    powerplay_renegades_dict={}
    for player in renegades:
        current_dict={'runs':0,'balls_faced':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker'] and rows['Over'] in [1,2,3,4,5,6]:
                current_dict['runs']+=rows['runs_batsman']
                current_dict['balls_faced']+=1
        if(current_dict['balls_faced']!=0):
            current_dict['strike_rate']=(current_dict['runs']/current_dict['balls_faced'])*100
        else:
            current_dict['strike_rate']=0
        powerplay_renegades_dict[player]=current_dict

    global death_renegades_dict
    death_renegades_dict={}
    for player in renegades:
        current_dict={'runs':0,'balls_faced':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker'] and rows['Over'] in [16,17,18,19,20]:
                current_dict['runs']+=rows['runs_batsman']
                current_dict['balls_faced']+=1
        if(current_dict['balls_faced']!=0):
            current_dict['strike_rate']=(current_dict['runs']/current_dict['balls_faced'])*100
        else:
            current_dict['strike_rate']=0
        death_renegades_dict[player]=current_dict

    global powerplay_stars_dict
    powerplay_stars_dict={}
    for player in stars:
        current_dict={'runs':0,'balls_faced':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker'] and rows['Over'] in [1,2,3,4,5,6]:
                current_dict['runs']+=rows['runs_batsman']
                current_dict['balls_faced']+=1
        if(current_dict['balls_faced']!=0):
            current_dict['strike_rate']=(current_dict['runs']/current_dict['balls_faced'])*100
        else:
            current_dict['strike_rate']=0
        powerplay_stars_dict[player]=current_dict

    global death_stars_dict
    death_stars_dict={}
    for player in stars:
        current_dict={'runs':0,'balls_faced':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker'] and rows['Over'] in [16,17,18,19,20]:
                current_dict['runs']+=rows['runs_batsman']
                current_dict['balls_faced']+=1
        if(current_dict['balls_faced']!=0):
            current_dict['strike_rate']=(current_dict['runs']/current_dict['balls_faced'])*100
        else:
            current_dict['strike_rate']=0
        death_stars_dict[player]=current_dict

    global powerplay_scorchers_dict
    powerplay_scorchers_dict={}
    for player in scorchers:
        current_dict={'runs':0,'balls_faced':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker'] and rows['Over'] in [1,2,3,4,5,6]:
                current_dict['runs']+=rows['runs_batsman']
                current_dict['balls_faced']+=1
        if(current_dict['balls_faced']!=0):
            current_dict['strike_rate']=(current_dict['runs']/current_dict['balls_faced'])*100
        else:
            current_dict['strike_rate']=0
        powerplay_scorchers_dict[player]=current_dict

    global death_scorchers_dict
    death_scorchers_dict={}
    for player in scorchers:
        current_dict={'runs':0,'balls_faced':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker'] and rows['Over'] in [16,17,18,19,20]:
                current_dict['runs']+=rows['runs_batsman']
                current_dict['balls_faced']+=1
        if(current_dict['balls_faced']!=0):
            current_dict['strike_rate']=(current_dict['runs']/current_dict['balls_faced'])*100
        else:
            current_dict['strike_rate']=0
        death_scorchers_dict[player]=current_dict

    global powerplay_thunders_dict
    powerplay_thunders_dict={}
    for player in thunders:
        current_dict={'runs':0,'balls_faced':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker'] and rows['Over'] in [1,2,3,4,5,6]:
                current_dict['runs']+=rows['runs_batsman']
                current_dict['balls_faced']+=1
        if(current_dict['balls_faced']!=0):
            current_dict['strike_rate']=(current_dict['runs']/current_dict['balls_faced'])*100
        else:
            current_dict['strike_rate']=0
        powerplay_thunders_dict[player]=current_dict

    global death_thunders_dict
    death_thunders_dict={}
    for player in thunders:
        current_dict={'runs':0,'balls_faced':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker'] and rows['Over'] in [16,17,18,19,20]:
                current_dict['runs']+=rows['runs_batsman']
                current_dict['balls_faced']+=1
        if(current_dict['balls_faced']!=0):
            current_dict['strike_rate']=(current_dict['runs']/current_dict['balls_faced'])*100
        else:
            current_dict['strike_rate']=0
        death_thunders_dict[player]=current_dict

    global powerplay_sixers_dict
    powerplay_sixers_dict={}
    for player in sixers:
        current_dict={'runs':0,'balls_faced':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker'] and rows['Over'] in [1,2,3,4,5,6]:
                current_dict['runs']+=rows['runs_batsman']
                current_dict['balls_faced']+=1
        if(current_dict['balls_faced']!=0):
            current_dict['strike_rate']=(current_dict['runs']/current_dict['balls_faced'])*100
        else:
            current_dict['strike_rate']=0
        powerplay_sixers_dict[player]=current_dict

    global death_sixers_dict
    death_sixers_dict={}
    for player in sixers:
        current_dict={'runs':0,'balls_faced':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker'] and rows['Over'] in [16,17,18,19,20]:
                current_dict['runs']+=rows['runs_batsman']
                current_dict['balls_faced']+=1
        if(current_dict['balls_faced']!=0):
            current_dict['strike_rate']=(current_dict['runs']/current_dict['balls_faced'])*100
        else:
            current_dict['strike_rate']=0
        death_sixers_dict[player]=current_dict

    ###point 5: mode of dismissal dict###
    dismissal_mode=updateballmatrix['wicket_kind'].unique()
    print(dismissal_mode)

    global dmode_strikers_dict
    dmode_strikers_dict={}
    for player in strikers:
        current_dict={'caught':0,'lbw':0,'bowled':0,'run out':0,'stumped':0,'hit wicket':0,'caught and bowled':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker']:
                if not (pd.isnull(rows['wicket_kind'])):
                    current_dict[rows['wicket_kind']]+=1
        dmode_strikers_dict[player]=current_dict

    global dmode_heat_dict
    dmode_heat_dict={}
    for player in heat:
        current_dict={'caught':0,'lbw':0,'bowled':0,'run out':0,'stumped':0,'hit wicket':0,'caught and bowled':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker']:
                if not (pd.isnull(rows['wicket_kind'])):
                    current_dict[rows['wicket_kind']]+=1
        dmode_heat_dict[player]=current_dict

    global dmode_hurricanes_dict
    dmode_hurricanes_dict={}
    for player in hurricanes:
        current_dict={'caught':0,'lbw':0,'bowled':0,'run out':0,'stumped':0,'hit wicket':0,'caught and bowled':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker']:
                if not (pd.isnull(rows['wicket_kind'])):
                    current_dict[rows['wicket_kind']]+=1
        dmode_hurricanes_dict[player]=current_dict

    global dmode_renegades_dict
    dmode_renegades_dict={}
    for player in renegades:
        current_dict={'caught':0,'lbw':0,'bowled':0,'run out':0,'stumped':0,'hit wicket':0,'caught and bowled':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker']:
                if not (pd.isnull(rows['wicket_kind'])):
                    current_dict[rows['wicket_kind']]+=1
        dmode_renegades_dict[player]=current_dict

    global dmode_stars_dict
    dmode_stars_dict={}
    for player in stars:
        current_dict={'caught':0,'lbw':0,'bowled':0,'run out':0,'stumped':0,'hit wicket':0,'caught and bowled':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker']:
                if not (pd.isnull(rows['wicket_kind'])):
                    current_dict[rows['wicket_kind']]+=1
        dmode_stars_dict[player]=current_dict

    global dmode_scorchers_dict
    dmode_scorchers_dict={}
    for player in scorchers:
        current_dict={'caught':0,'lbw':0,'bowled':0,'run out':0,'stumped':0,'hit wicket':0,'caught and bowled':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker']:
                if not (pd.isnull(rows['wicket_kind'])):
                    if not rows['wicket_kind']=='retired hurt':
                        current_dict[rows['wicket_kind']]+=1
        dmode_scorchers_dict[player]=current_dict

    global dmode_thunders_dict
    dmode_thunders_dict={}
    for player in thunders:
        current_dict={'caught':0,'lbw':0,'bowled':0,'run out':0,'stumped':0,'hit wicket':0,'caught and bowled':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker']:
                if not (pd.isnull(rows['wicket_kind'])):
                    if not rows['wicket_kind']=='retired hurt':
                        current_dict[rows['wicket_kind']]+=1
        dmode_thunders_dict[player]=current_dict

    global dmode_sixers_dict
    dmode_sixers_dict={}
    for player in sixers:
        current_dict={'caught':0,'lbw':0,'bowled':0,'run out':0,'stumped':0,'hit wicket':0,'caught and bowled':0}
        for index,rows in updateballmatrix.iterrows():
            if player == rows['Striker']:
                if not (pd.isnull(rows['wicket_kind'])):
                    current_dict[rows['wicket_kind']]+=1
        dmode_sixers_dict[player]=current_dict

    ###Point6- most dismissals against bowler type###
    global point6matrix
    point6matrix=updateballmatrix
    point6matrix['bowling_hand']=''
    temp_dict={}
    for index,player in playersdf.iterrows():
        for ind,rows in point6matrix.iterrows():
            if(rows['Bowler']==player['Player']):
                #rows['bowling_hand']=player['bowling_hand']
                point6matrix.loc[ind,'bowling_hand']=player['bowling_hand']

    point6matrix['bowler_type']=''
    temp_dict={}
    for index,player in playersdf.iterrows():
        for ind,rows in point6matrix.iterrows():
            if(rows['Bowler']==player['Player']):
                #rows['bowling_hand']=player['bowling_hand']
                point6matrix.loc[ind,'bowler_type']=player['bowler_type']


    global disbowltype_strikers_dict
    disbowltype_strikers_dict={}
    for player in strikers:
        current_dict={'left_spin':0,'left_pace':0,'right_spin':0,'right_pace':0}
        for index,rows in point6matrix.iterrows():
            if player==rows['Striker']:
                if(rows['wicket_player_out'] != ''):
                    if(rows['bowling_hand'=='L']):
                        if(rows['bowler_type']=='S'):
                            current_dict['left_spin']+=1
                        elif(rows['bowler_type']=='P'):
                            current_dict['left_pace']+=1
                    elif(rows['bowling_hand'=='R']):
                        if(rows['bowler_type']=='S'):
                            current_dict['right_spin']+=1
                        elif(rows['bowler_type']=='P'):
                            current_dict['right_pace']+=1
        disbowltype_strikers_dict[player]=current_dict

    global disbowltype_heat_dict
    disbowltype_heat_dict={}
    for player in heat:
        current_dict={'left_spin':0,'left_pace':0,'right_spin':0,'right_pace':0}
        for index,rows in point6matrix.iterrows():
            if player==rows['Striker']:
                if(rows['wicket_player_out'] != ''):
                    if(rows['bowling_hand'=='L']):
                        if(rows['bowler_type']=='S'):
                            current_dict['left_spin']+=1
                        elif(rows['bowler_type']=='P'):
                            current_dict['left_pace']+=1
                    elif(rows['bowling_hand'=='R']):
                        if(rows['bowler_type']=='S'):
                            current_dict['right_spin']+=1
                        elif(rows['bowler_type']=='P'):
                            current_dict['right_pace']+=1
        disbowltype_heat_dict[player]=current_dict

    global disbowltype_hurricanes_dict
    disbowltype_hurricanes_dict={}
    for player in hurricanes:
        current_dict={'left_spin':0,'left_pace':0,'right_spin':0,'right_pace':0}
        for index,rows in point6matrix.iterrows():
            if player==rows['Striker']:
                if(rows['wicket_player_out'] != ''):
                    if(rows['bowling_hand'=='L']):
                        if(rows['bowler_type']=='S'):
                            current_dict['left_spin']+=1
                        elif(rows['bowler_type']=='P'):
                            current_dict['left_pace']+=1
                    elif(rows['bowling_hand'=='R']):
                        if(rows['bowler_type']=='S'):
                            current_dict['right_spin']+=1
                        elif(rows['bowler_type']=='P'):
                            current_dict['right_pace']+=1
        disbowltype_hurricanes_dict[player]=current_dict

    global disbowltype_renegades_dict
    disbowltype_renegades_dict={}
    for player in renegades:
        current_dict={'left_spin':0,'left_pace':0,'right_spin':0,'right_pace':0}
        for index,rows in point6matrix.iterrows():
            if player==rows['Striker']:
                if(rows['wicket_player_out'] != ''):
                    if(rows['bowling_hand'=='L']):
                        if(rows['bowler_type']=='S'):
                            current_dict['left_spin']+=1
                        elif(rows['bowler_type']=='P'):
                            current_dict['left_pace']+=1
                    elif(rows['bowling_hand'=='R']):
                        if(rows['bowler_type']=='S'):
                            current_dict['right_spin']+=1
                        elif(rows['bowler_type']=='P'):
                            current_dict['right_pace']+=1
        disbowltype_renegades_dict[player]=current_dict

    global disbowltype_stars_dict
    disbowltype_stars_dict={}
    for player in stars:
        current_dict={'left_spin':0,'left_pace':0,'right_spin':0,'right_pace':0}
        for index,rows in point6matrix.iterrows():
            if player==rows['Striker']:
                if(rows['wicket_player_out'] != ''):
                    if(rows['bowling_hand'=='L']):
                        if(rows['bowler_type']=='S'):
                            current_dict['left_spin']+=1
                        elif(rows['bowler_type']=='P'):
                            current_dict['left_pace']+=1
                    elif(rows['bowling_hand'=='R']):
                        if(rows['bowler_type']=='S'):
                            current_dict['right_spin']+=1
                        elif(rows['bowler_type']=='P'):
                            current_dict['right_pace']+=1
        disbowltype_stars_dict[player]=current_dict

    global disbowltype_scorchers_dict
    disbowltype_scorchers_dict={}
    for player in scorchers:
        current_dict={'left_spin':0,'left_pace':0,'right_spin':0,'right_pace':0}
        for index,rows in point6matrix.iterrows():
            if player==rows['Striker']:
                if(rows['wicket_player_out'] != ''):
                    if(rows['bowling_hand'=='L']):
                        if(rows['bowler_type']=='S'):
                            current_dict['left_spin']+=1
                        elif(rows['bowler_type']=='P'):
                            current_dict['left_pace']+=1
                    elif(rows['bowling_hand'=='R']):
                        if(rows['bowler_type']=='S'):
                            current_dict['right_spin']+=1
                        elif(rows['bowler_type']=='P'):
                            current_dict['right_pace']+=1
        disbowltype_scorchers_dict[player]=current_dict

    global disbowltype_thunders_dict
    disbowltype_thunders_dict={}
    for player in thunders:
        current_dict={'left_spin':0,'left_pace':0,'right_spin':0,'right_pace':0}
        for index,rows in point6matrix.iterrows():
            if player==rows['Striker']:
                if(rows['wicket_player_out'] != ''):
                    if(rows['bowling_hand'=='L']):
                        if(rows['bowler_type']=='S'):
                            current_dict['left_spin']+=1
                        elif(rows['bowler_type']=='P'):
                            current_dict['left_pace']+=1
                    elif(rows['bowling_hand'=='R']):
                        if(rows['bowler_type']=='S'):
                            current_dict['right_spin']+=1
                        elif(rows['bowler_type']=='P'):
                            current_dict['right_pace']+=1
        disbowltype_thunders_dict[player]=current_dict

    global disbowltype_sixers_dict
    disbowltype_sixers_dict={}
    for player in sixers:
        current_dict={'left_spin':0,'left_pace':0,'right_spin':0,'right_pace':0}
        for index,rows in point6matrix.iterrows():
            if player==rows['Striker']:
                if(rows['wicket_player_out'] != ''):
                    if(rows['bowling_hand'=='L']):
                        if(rows['bowler_type']=='S'):
                            current_dict['left_spin']+=1
                        elif(rows['bowler_type']=='P'):
                            current_dict['left_pace']+=1
                    elif(rows['bowling_hand'=='R']):
                        if(rows['bowler_type']=='S'):
                            current_dict['right_spin']+=1
                        elif(rows['bowler_type']=='P'):
                            current_dict['right_pace']+=1
        disbowltype_sixers_dict[player]=current_dict



    return HttpResponse('hello')


def strikersview(request):
    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\death_strikers_dict.json'
    with open(datapath) as json_file:
        death_strikers_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\powerplay_strikers_dict.json'
    with open(datapath) as json_file:
        powerplay_strikers_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\dmode_strikers_dict.json'
    with open(datapath) as json_file:
        dmode_strikers_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\disbowltype_strikers_dict.json'
    with open(datapath) as json_file:
        disbowltype_strikers_dict=json.load(json_file)

    powerplay_strikers_dict=json.dumps(powerplay_strikers_dict)
    death_strikers_dict=json.dumps(death_strikers_dict)
    dmode_strikers_dict=json.dumps(dmode_strikers_dict)
    disbowltype_strikers_dict=json.dumps(disbowltype_strikers_dict)

    datapath2=os.path.dirname(os.path.abspath(__file__))+'\\Complete.csv'
    complete=pd.read_csv(datapath2)
    print(complete)

    return render(request, 'strikers.html',context={'powerplay_strikers_dict':powerplay_strikers_dict,
                                                    'death_strikers_dict':death_strikers_dict,
                                                    'dmode_strikers_dict':dmode_strikers_dict,
                                                    'disbowltype_strikers_dict':disbowltype_strikers_dict})

def heatview(request):
    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\death_heat_dict.json'
    with open(datapath) as json_file:
        death_heat_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\powerplay_heat_dict.json'
    with open(datapath) as json_file:
        powerplay_heat_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\dmode_heat_dict.json'
    with open(datapath) as json_file:
        dmode_heat_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\disbowltype_heat_dict.json'
    with open(datapath) as json_file:
        disbowltype_heat_dict=json.load(json_file)

    powerplay_heat_dict=json.dumps(powerplay_heat_dict)
    death_heat_dict=json.dumps(death_heat_dict)
    dmode_heat_dict=json.dumps(dmode_heat_dict)
    disbowltype_heat_dict=json.dumps(disbowltype_heat_dict)

    return render(request, 'heat.html',context={'powerplay_heat_dict':powerplay_heat_dict,
                                                    'death_heat_dict':death_heat_dict,
                                                    'dmode_heat_dict':dmode_heat_dict,
                                                    'disbowltype_heat_dict':disbowltype_heat_dict})

def hurricanesview(request):
    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\death_hurricanes_dict.json'
    with open(datapath) as json_file:
        death_hurricanes_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\powerplay_hurricanes_dict.json'
    with open(datapath) as json_file:
        powerplay_hurricanes_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\dmode_hurricanes_dict.json'
    with open(datapath) as json_file:
        dmode_hurricanes_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\disbowltype_hurricanes_dict.json'
    with open(datapath) as json_file:
        disbowltype_hurricanes_dict=json.load(json_file)

    powerplay_hurricanes_dict=json.dumps(powerplay_hurricanes_dict)
    death_hurricanes_dict=json.dumps(death_hurricanes_dict)
    dmode_hurricanes_dict=json.dumps(dmode_hurricanes_dict)
    disbowltype_hurricanes_dict=json.dumps(disbowltype_hurricanes_dict)

    return render(request, 'hurricanes.html',context={'powerplay_hurricanes_dict':powerplay_hurricanes_dict,
                                                    'death_hurricanes_dict':death_hurricanes_dict,
                                                    'dmode_hurricanes_dict':dmode_hurricanes_dict,
                                                    'disbowltype_hurricanes_dict':disbowltype_hurricanes_dict})

def renegadesview(request):
    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\death_renegades_dict.json'
    with open(datapath) as json_file:
        death_renegades_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\powerplay_renegades_dict.json'
    with open(datapath) as json_file:
        powerplay_renegades_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\dmode_renegades_dict.json'
    with open(datapath) as json_file:
        dmode_renegades_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\disbowltype_renegades_dict.json'
    with open(datapath) as json_file:
        disbowltype_renegades_dict=json.load(json_file)

    powerplay_renegades_dict=json.dumps(powerplay_renegades_dict)
    death_renegades_dict=json.dumps(death_renegades_dict)
    dmode_renegades_dict=json.dumps(dmode_renegades_dict)
    disbowltype_renegades_dict=json.dumps(disbowltype_renegades_dict)

    return render(request, 'renegades.html',context={'powerplay_renegades_dict':powerplay_renegades_dict,
                                                    'death_renegades_dict':death_renegades_dict,
                                                    'dmode_renegades_dict':dmode_renegades_dict,
                                                    'disbowltype_renegades_dict':disbowltype_renegades_dict})

def starsview(request):
    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\death_stars_dict.json'
    with open(datapath) as json_file:
        death_stars_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\powerplay_stars_dict.json'
    with open(datapath) as json_file:
        powerplay_stars_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\dmode_stars_dict.json'
    with open(datapath) as json_file:
        dmode_stars_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\disbowltype_stars_dict.json'
    with open(datapath) as json_file:
        disbowltype_stars_dict=json.load(json_file)

    powerplay_stars_dict=json.dumps(powerplay_stars_dict)
    death_stars_dict=json.dumps(death_stars_dict)
    dmode_stars_dict=json.dumps(dmode_stars_dict)
    disbowltype_stars_dict=json.dumps(disbowltype_stars_dict)

    return render(request, 'stars.html',context={'powerplay_stars_dict':powerplay_stars_dict,
                                                    'death_stars_dict':death_stars_dict,
                                                    'dmode_stars_dict':dmode_stars_dict,
                                                    'disbowltype_stars_dict':disbowltype_stars_dict})

def scorchersview(request):
    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\death_scorchers_dict.json'
    with open(datapath) as json_file:
        death_scorchers_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\powerplay_scorchers_dict.json'
    with open(datapath) as json_file:
        powerplay_scorchers_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\dmode_scorchers_dict.json'
    with open(datapath) as json_file:
        dmode_scorchers_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\disbowltype_scorchers_dict.json'
    with open(datapath) as json_file:
        disbowltype_scorchers_dict=json.load(json_file)

    powerplay_scorchers_dict=json.dumps(powerplay_scorchers_dict)
    death_scorchers_dict=json.dumps(death_scorchers_dict)
    dmode_scorchers_dict=json.dumps(dmode_scorchers_dict)
    disbowltype_scorchers_dict=json.dumps(disbowltype_scorchers_dict)

    return render(request, 'scorchers.html',context={'powerplay_scorchers_dict':powerplay_scorchers_dict,
                                                    'death_scorchers_dict':death_scorchers_dict,
                                                    'dmode_scorchers_dict':dmode_scorchers_dict,
                                                    'disbowltype_scorchers_dict':disbowltype_scorchers_dict})

def thundersview(request):
    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\death_thunders_dict.json'
    with open(datapath) as json_file:
        death_thunders_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\powerplay_thunders_dict.json'
    with open(datapath) as json_file:
        powerplay_thunders_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\dmode_thunders_dict.json'
    with open(datapath) as json_file:
        dmode_thunders_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\disbowltype_thunders_dict.json'
    with open(datapath) as json_file:
        disbowltype_thunders_dict=json.load(json_file)

    powerplay_thunders_dict=json.dumps(powerplay_thunders_dict)
    death_thunders_dict=json.dumps(death_thunders_dict)
    dmode_thunders_dict=json.dumps(dmode_thunders_dict)
    disbowltype_thunders_dict=json.dumps(disbowltype_thunders_dict)

    return render(request, 'thunders.html',context={'powerplay_thunders_dict':powerplay_thunders_dict,
                                                    'death_thunders_dict':death_thunders_dict,
                                                    'dmode_thunders_dict':dmode_thunders_dict,
                                                    'disbowltype_thunders_dict':disbowltype_thunders_dict})

def sixersview(request):
    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\death_thunders_dict.json'
    with open(datapath) as json_file:
        death_thunders_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\powerplay_thunders_dict.json'
    with open(datapath) as json_file:
        powerplay_thunders_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\dmode_thunders_dict.json'
    with open(datapath) as json_file:
        dmode_thunders_dict=json.load(json_file)

    datapath=os.path.dirname(os.path.abspath(__file__))+'\\jsonfiles'+'\\disbowltype_thunders_dict.json'
    with open(datapath) as json_file:
        disbowltype_thunders_dict=json.load(json_file)

    powerplay_thunders_dict=json.dumps(powerplay_thunders_dict)
    death_thunders_dict=json.dumps(death_thunders_dict)
    dmode_thunders_dict=json.dumps(dmode_thunders_dict)
    disbowltype_thunders_dict=json.dumps(disbowltype_thunders_dict)

    return render(request, 'sixers.html',context={'powerplay_thunders_dict':powerplay_thunders_dict,
                                                    'death_thunders_dict':death_thunders_dict,
                                                    'dmode_thunders_dict':dmode_thunders_dict,
                                                    'disbowltype_thunders_dict':disbowltype_thunders_dict})
