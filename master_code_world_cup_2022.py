import pandas as pd
import numpy as np
import sys

import random

import os
cwd = os.getcwd()

path_and_filename =  cwd+'\\key info.xlsx' # path to file + file name
participants = 'participants' # sheet name or sheet number or list of sheet numbers and names

#--------
#
#--------

##
# get participants
##

df_participants = pd.read_excel(path_and_filename, sheet_name = participants)

# set index to column
df_participants['id_participants'] = df_participants.index

# reorder cols
df_participants = df_participants[['id_participants','Nombre']]

# get number of participants
no_participants = df_participants.shape[0]



##
# get teams
##
# teams = 'teams'
# df_teams = pd.read_excel(path_and_filename, sheet_name = teams)


list_teams = [
'Qatar'
,'Ecuador'
,'Senegal'
,'Netherlands'
,'England'
,'IR Iran'
,'USA'
,'Wales' 
,'Argentina'
,'Saudi Arabia'
,'Mexico'
,'Poland' 
,'France'
,'Australia'
,'Denmark'
,'Tunisia'  
,'Spain'
,'Costa Rica'
,'Germany'
,'Japan' 
,'Belgium'
,'Canada'
,'Morocco'
,'Croatia' 
,'Brazil'
,'Serbia'
,'Switzerland'
,'Cameroon' 
,'Portugal'
,'Ghana'
,'Uruguay'
,'Korea Republic']

# list columns
columns = ['Equipo']

# create df
df_teams = pd.DataFrame(data = list_teams, columns = columns)

# set index to column
df_teams['id_team'] = df_teams.index

# reorder cols
df_teams = df_teams[['id_team','Equipo']]

# get number of teams
no_teams = df_teams.shape[0]

#-------
#
#-------


##
# for each participant
#
# get random number from 1 to 32 (there are 32 teams in the World Cup)
##



# generate empty list to save random numbers on it
random_list = []

# generate list that will count how many times a random number has appeared in the list. only needed when there are more participants than teams
count_random_numbers_list = []

# if #participants < #teams then there will be teams without participant. Else, there will be participants without teams

# initialise counter that will increment every time we get a new participant 
count_participant = 0

# initialise counter that will increment every time we have a multiple of 32
j = 0

# if there are less participants than teams
if no_participants <= 32: 
    # loop through number of participants
    for i in range(no_participants):

        # generate random number
        random_number = random.randint(0,no_teams-1)

        ##
        # check whether the random_number is in the list
        ##

        # if it is NOT in the list, append
        if random_number not in random_list:
            random_list.append(random_number)


        # else, shuffle and try again
        else:
            random_number = random.randint(0,no_teams-1)

            # while random number is in the list, shuffle
            while random_number in random_list:
                random_number = random.randint(0,no_teams-1)


            random_list.append(random_number)

# more participants than teams
if no_participants > 32:

    # loop through number of teams
    for i in range(no_participants):

        # print participant name
        print( df_participants.loc[count_participant,'Nombre'] )

        # increment counter
        count_participant = count_participant + 1
        print(f"participant id:{count_participant}")

       

        # increment this counter every time we hit a multiple of 32
        if count_participant % 32 == 0:
            
            j = j + 1
            print(f"multiple of 32: j = {j}")
            


        # generate random number 
        random_number = random.randint(0,no_teams-1)

        ##
        # check whether the random_number is in the list
        ##

        ##
        # case when we are in the first 32 participants
        ##

        
        # if it is NOT in the list, append. only check if it is in the required slice of the list
        if ( random_number not in random_list[ 32*j:count_participant ] ): #  and ( count_participant > 32 * (j-1) ) and ( count_participant <=32 * j ):
            random_list.append(random_number)
            print(random_list[ 32*j:count_participant ])

        # if it is IN the list, then find one that it is not and append. only check if it is in the required slice of the list
        elif ( random_number in random_list[ (32*j):count_participant ] ): # and ( count_participant > 32 * (j-1) ) and ( count_participant <=32 * j ):
            
            print(f"we entered a repeated number {random_number}")
            random_number = random.randint(0,no_teams-1)
            

            # while random number is in the list, shuffle
            while random_number in random_list[ 32*j:count_participant ]:
                random_number = random.randint(0,no_teams-1)
                print(f"searching for a non-repeated number {random_number}")
                


            random_list.append(random_number)
            
            print(f"non repeated number found: {random_number}")
            print(random_list[ 32*j:count_participant ])

        print(random_number)
        print("\n")

        # when we are between 33 and 64 participants, we know all numbers have appeared at least once. Then, allow only the number to appear at most 2 times
        

            
 
# add a column called random number
df_participants['random_team_id'] = random_list

#--------
#
#--------

##
# Join dataframes so that we get a random the team by participant
##

df_participants_and_random_teams = pd.merge(df_participants,
                                            df_teams,
                                            left_on = 'random_team_id',
                                            right_on = 'id_team',
                                            how = 'left')

df_participants_and_random_teams.drop(columns = 'id_team', inplace = True)

#----
#
#----
# data to excel quick!

df_participants_and_random_teams.to_excel("London_Bulls_WC2022_game1.xlsx",
            sheet_name='Sheet_name_1',index = False)  


#-------
#
#-------

##
# If less than 32 participants
##

if no_participants < 32:
    ##
    # What happen to the teams that are not chosen?
    # get the index of teams that are not chosen
    ##

    # list of random numbers
    list_random_team_id = df_participants_and_random_teams['random_team_id'].to_list()

    df_teams_not_chosen_index = [number for number in range(1,no_teams) if number not in list_random_numbers ]

    # get teams that are not choosen from df_teams
    mask = df_teams['id_team'].isin(df_teams_not_chosen_index)

    df_teams_not_chosen = df_teams.loc[mask]

    ##
    # some participants are lucky and get two teams.
    # if no participants exceed 32 then we need to look at two paticipants having the same team
    #
    # For these teams, we generate a random number. Then, we match the random number to the participant id
    #
    # Example: Let's say Germany hasn't been a match. We generate a random number, say 6. Then whoever has 6 as Id will get Germany
    ##

    # how many teams do we have left?
    no_teams_left = df_teams_not_chosen.shape[0]

    # generate empty list
    random_list = []

    # loop through number of teams left
    for i in range(no_teams_left):

        # generate random number.
        random_number = random.randint(0,no_participants-1)

        ##
        # check whether the random_number is in the list - we want different random numbers
        ##

        # if it is NOT in the list, append
        if random_number not in random_list:
            random_list.append(random_number)


        # else, shuffle and try again
        else:
            random_number = random.randint(0,no_participants-1)

            # while random number is in the list, shuffle
            while random_number in random_list:
                random_number = random.randint(0,no_participants-1)


            random_list.append(random_number)

    ##
    # once random list of indexes has been generated, add as column to the dataframe that contains all teams that we didn't match to a participant
    ##
    df_teams_not_chosen.loc[:,'id_participants'] = random_list


    #-------
    #
    #-------

    ##
    # Join df_participants_and_random_teams and df_teams_not_chosen to get the final table: a table where the participants will have at least a team, and some of them will have two 
    ##
    df_participants_and_random_teams_merged = pd.merge(df_participants_and_random_teams,
                                                df_teams_not_chosen,
                                                left_on = 'id_participants', # joining on index
                                                right_on = 'id_participants',
                                                how = 'left')

    df_participants_and_random_teams_merged.drop(columns = ['id_participants','random_team_id','id_team_x','id_team_y'], inplace = True)

    df_participants_and_random_teams_merged.rename(columns = {'Equipo_x':'Equipo 1',
                                                        'Equipo_xy':'Equipo 2'},
                                                        inplace = True)

    # data to excel quick!

    df_participants_and_random_teams_merged.to_excel("London_Bulls_WC2022_game1.xlsx",
                sheet_name='Sheet_name_1',index = False)  