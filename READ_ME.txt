To use this, create a folder in TBAnalyzed that will contain the games for a certain team. 

./parser <folder name>
--This will go through all games in the folder and create/add to a folder of that same name in "ProcessedGames"
--The html files will be deleted once all the important info is stripped (not deleting yet in case i want more info)


./reader <folder name>
--This will go through the games in said folder and create a game summary of the team in "Game_Profiles"
--The battle file will not be deleted, in case the game summary becomes updated

From here, use the python script(to be created) to process the summaries and create a way to guess the leads