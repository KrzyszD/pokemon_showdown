#ifndef READER_H
#define READER_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <dirent.h>
#include <sys/stat.h>
#include "battle.h"
#include "team.h"



size_t numBattles(char* dirn);
int fillTeamNames(team* squad, FILE* fp);
int fillLeads(battle* fight, FILE* fp);
int processBattle(battle* fight, FILE* fp);
int processFile(char* dir_name, char* filename, size_t profile_num);


const char* SOURCE_DIR = "ProcessedGames/";
const char* DESTINATION_DIR = "Game_Profiles/";



int main(int argc, char** argv) {
   if(argc != 2) { printf("Choose a team folder to process"); return 1; }
   
   char* src_dir = malloc(strlen(SOURCE_DIR) + strlen(argv[1]) + 1);
   strcpy(src_dir, SOURCE_DIR);
   strcpy(src_dir + strlen(SOURCE_DIR), argv[1]);

   struct dirent* dirn;
   DIR* dirc = opendir(src_dir);

   if(!dirc) {
      printf("Problem w/ source directoy\n");
      free(src_dir);
      return -1;
   }

   //argv[1] is the folder of which games to process
   char* dest_dir = malloc(strlen(DESTINATION_DIR) + strlen(argv[1]) + 1);
   strcpy(dest_dir, DESTINATION_DIR);
   strcpy(dest_dir + strlen(DESTINATION_DIR), argv[1]); // Yes, I should sanitize user inputs but im the only user so
   size_t start_num = numBattles(dest_dir); // Attempt to create a directory if it doesnt exist

   if(start_num < 0) { printf("Problem opening destination directory"); free(dest_dir); return -1; } 
   
   while( (dirn = readdir(dirc)) ) {
      if (strcmp(dirn->d_name, ".") && strcmp(dirn->d_name, "..")) { // Dont look at . and ..
         printf("Processing battle: %s\n", dirn->d_name);
         processFile(argv[1], dirn->d_name, start_num);
         start_num++;
      }
   }

   free(dest_dir);
   free(src_dir);
   return 0;
}



//Make this process battle or some shit
int processFile(char* dir_name, char* filename, size_t profile_num) {
   if(profile_num > 999999) { printf("battle_num is too big\n"); return -1; }
   
   //Setup src file path
   char* src_path = malloc(strlen(SOURCE_DIR) + strlen(dir_name) + 1 + strlen(filename) + 1);
   strcpy(src_path, SOURCE_DIR);
   strcpy(src_path + strlen(SOURCE_DIR), dir_name);
   src_path[strlen(SOURCE_DIR) + strlen(dir_name)] = '/';
   strcpy(src_path + strlen(SOURCE_DIR) + strlen(dir_name) + 1, filename); 
 
   battle* fight = Battle();//Make battle* here

   FILE* fp = fopen(src_path, "r");

   if(fp == NULL) {
      printf("Error opening src file\n");
      free(src_path);
      return 1;
   }

   //Setup destination filepath
   char* dest_path = malloc(strlen(DESTINATION_DIR) + strlen(dir_name) + 1 + strlen("GameProfile") + 7);
   strcpy(dest_path, DESTINATION_DIR);
   strcpy(dest_path + strlen(DESTINATION_DIR), dir_name);
   dest_path[strlen(DESTINATION_DIR) + strlen(dir_name)] = '/';
   strcpy(dest_path + strlen(DESTINATION_DIR) + strlen(dir_name) + 1, "GameProfile");

   char* number = malloc(7);
   snprintf(number, 7, "%06zu", profile_num);
   number[6] = '\0';
 
   strcpy(dest_path + strlen(DESTINATION_DIR) + strlen(dir_name) + 1 + strlen("GameProfile"), number); 

   FILE* dst_fp = fopen(dest_path, "w+");

   if(!dst_fp) {
      printf("Error creating destination file\n");
      free(src_path); free(dest_path); free(number);
      fclose(fp);
      return 1;
   }


   fillTeamNames(fight->my_team, fp);
   fillTeamNames(fight->opponent_team, fp);

   fillLeads(fight, fp);


   processBattle(fight, fp);


   //puts("Printing my team");
   printTeamInfo(fight->my_team, dst_fp);
   //puts("Printing opponent team");
   fprintf(dst_fp, "--------------------\n");

   printTeamInfo(fight->opponent_team, dst_fp); 
  
   fclose(fp);
   fclose(dst_fp);
   deleteBattle(fight);

   return 0;
}


//Fill in a team with the names
//Return 0 on success, but that doesnt mean all was read, only that one was read
int fillTeamNames(team* squad, FILE* fp) {
   char* buffer = NULL;
   size_t buffer_size;
   ssize_t read;

   //Get the team compositions
   read = getline(&buffer, &buffer_size, fp);//My team

   //Get each name
   if(read > 0) {
      //Names are delimited by "/"
      buffer[read - 1] = '\0';//Remove the newline getline keeps
      char *name, *temp = strdup(buffer);
      char* delimiter = "/";
      name = strtok(temp, delimiter);
      int result; // Remove
      if(name != NULL) {
         addPokemon(squad, name, NULL, NULL, NULL);
         while(name = strtok(NULL, delimiter)) {
            addPokemon(squad, name, NULL, NULL, NULL);
         }
      } else {
         free(temp);
         free(buffer);
         return 1;
      }
      free(temp);
   } else {
      return 1;
   }

   free(buffer);

   return 0;
}


int processLeadLine(char* buffer, battle* fight, ssize_t read) {
   //Get the first lead
   char* keyword;
   int team;
   if(strstr(buffer, "Go! ")) {
      team = 1; // My team
      keyword = "Go! ";
   } else {
      team = 2; // Opponent team
      keyword = "sent out ";
   }

   buffer[read - 2] = '\0';//Remove "!\n" at the end
      
   char* name = strstr(buffer, keyword);
   if(name) {
      name += strlen(keyword);

      //Check to see if name used is different from formal name
      char* form_check = strstr(name, "(");
      if(form_check) {
         name = form_check + 1;
         while(*form_check != ')') { form_check++; }
         *form_check = '\0';
      }
      if(team == 1) {
         updateStatus(fight->my_team, name, 2);
      } else {
         updateStatus(fight->opponent_team, name, 2);
      }
   }
   
   return 0;
}

//Get the leads and update the team info
//Return 0 on success, -1 on failure

//Redo this since youre mons arnt always first, but the location is consistent
int fillLeads(battle* fight, FILE* fp) {
   char* buffer = NULL;
   size_t buffer_size;
   ssize_t read;
   
   for(int i = 0; i < 3; i++) { getline(&buffer, &buffer_size, fp); } //Get to beginning of relevant text

   //Get the first lead line
   if( (read = getline(&buffer, &buffer_size, fp)) > 0 ) {
      processLeadLine(buffer, fight, read);
   } else { printf("Problem reading in lead line\n"); return -1; }

   for(int i = 0; i < 3; i++) {
      getline(&buffer, &buffer_size, fp); // Skip empty line
   
      //Get the next lead
      if((read = getline(&buffer, &buffer_size, fp)) > 0) {
         processLeadLine(buffer, fight, read);
      } else { printf("Problem reading in lead line\n"); return -1;}
   } 
   
   free(buffer);
   return 0;
}



//Look at each line and determine what information you can get from it
//Aims to fill in information regarding ability, item, dynamax, and moveset
int processBattle(battle* fight, FILE* fp) {
   char* buffer = NULL; 
   size_t buffer_size;
   ssize_t read;

   char* loc;
   char* name;

   //Read each line and try to find a keyword
   while((read = getline(&buffer, &buffer_size, fp)) > 0) {
      //I could make this a little shorter by making a team variable and not repeating some code but whatever
      //This could also run faster by reordering the searches so less common are at the end      
      //Also add continue statements to the end you psycho
  

      //Get frisked items
      //IMPORTANT THE FRISK CHECK MUST BE BEFORE THE ABILITY CHECK//
      //IMPORTANT THE FRISK CHECK MUST BE BEFORE THE ABILITY CHECK//
      if( (loc = strstr(buffer, "frisked ")) ) {
         buffer[read - 2] = '\0'; //Remove "!\n" from end

         if( (name = strstr(buffer, "opposing ")) ) {
            name += strlen("opposing ");
            char* end = name;
            while (*end != ' ') { end++; }
            *end = '\0';

            loc = end + strlen(" and found its ");
 
            updateItem(fight->opponent_team, name, loc);
         } else {
            name = loc + strlen("frisked ");
            char* end = name;
            while(*end != ' ') { end++; }
            *end = '\0';

            loc = end + strlen(" and found its ");

            updateItem(fight->my_team, name, loc);
         }
      }

      //Get focus sash
      if( (loc = strstr(buffer, "hung on using its ")) ) {
         buffer[read - 2] = '\0'; //Remove "!\n" from end

         loc += strlen("hung on using its ");

         if( (name = strstr(buffer, "opposing ")) ) {
            name += strlen("opposing ");
            char* end = name;
            while(*end != ' ') { end++; }
            *end = '\0';
            
            updateItem(fight->opponent_team, name, loc);
         } else {
            name = buffer;
            char* end = name; 
            while(*end != ' ') { end++; }
            *end = '\0';

            updateItem(fight->my_team, name, loc);
         }
      }

      //Get leftovers/black sludge
      if( (loc = strstr(buffer, "restored a little HP")) ) {
         buffer[read - 2] = '\0'; //Remove "!\n" from end

         loc += strlen("restored a little HP using its ");

         if( (name = strstr(buffer, "opposing ")) ) {
            name += strlen("opposing ");
            char* end = name; 
            while(*end != ' ') { end++; }
            *end = '\0';
            
            updateItem(fight->opponent_team, name, loc);
         } else {
            name = buffer;
            char* end = name;
            while(*end != ' ') { end++; }
            *end = '\0';
            
            updateItem(fight->my_team, name, loc);
         } 
      }

      //Get life orb information
      if( (loc = strstr(buffer, "lost some of its HP")) ) {
         if( (name = strstr(buffer, "opposing ")) ) {
            name += strlen("opposing ");
            char* end = name;
            while(*end != ' ') { end++; }
            *end = '\0';
 
            updateItem(fight->opponent_team, name, "Life Orb");
         } else {
            name = buffer;
            char* end = name;
            while(*end != ' ') { end++; }
            *end = '\0';

            updateItem(fight->my_team, name, "Life Orb");
         }
      }

      //Get item from poltergeist use
      if( (loc = strstr(buffer, "about to be attacked by its ")) ) {
         buffer[read - 2] = '\0'; //Remove "!\n" from end

         loc += strlen("about to be attacked by its ");
         
         if( (name = strstr(buffer, "opposing")) ) {
            name += strlen("opposing ");
            char* end = name;
            while(*end != ' ') { end++; }
            *end = '\0';

            updateItem(fight->opponent_team, name, loc);
         } else {
            name = buffer;
            char* end = name;
            while (*end != ' ') { end++; } 
            *end = '\0';
   
            updateItem(fight->my_team, name, loc);
         } 
      } 
      
      //Catch items that knocked off
      if( (loc = strstr(buffer, "knocked off")) ) {
         buffer[read - 2] = '\0'; // Remove "!\n"

         if( (name = strstr(loc, "opposing ")) ) {
            name += strlen("opposing ");
            char* end = name;
            while(*end != '\'') { end++; }
            *end = '\0'; //Null terminate the name

            loc = end + 3; //Move pointer to start of item name
            
            updateItem(fight->opponent_team, name, loc);
         } else {
            name = loc + strlen("knocked off ");
            char* end = name; 
            while(*end != '\'') { end++; }
            *end = '\0';

            loc = end + 3;
            
            updateItem(fight->my_team, name, loc);
         }
      }

      //Add anything pokemon eats to items
      if( (loc = strstr(buffer, " ate its ")) ) {
         buffer[read - 3] = '\0'; // Remove '!)\n' from end
         
         loc += strlen(" ate its ");

         if( (name = strstr(buffer, "opposing ")) ) {
            name += strlen("opposing ");
            char* end = name;
            while(*end != ' ') { end++; } 
            end = '\0';
            
            updateItem(fight->opponent_team, name, loc);
         } else {
            name = buffer + 1; // Name starts after '('
            char* end = name;
            while( *end != ' ') { end++; }
            *end = '\0';

            updateItem(fight->my_team, name, loc);
         }
      } 
    
      //Add any moves to moveset
      if( (loc = strstr(buffer, "used ")) ) {
         buffer[read - 2] = '\0'; //Remove the !\n at the end of the line

         loc += strlen("used "); //Start of move name
         
         if(!strncmp(loc, "its ", 4)) { continue; }// This should be changed, its here until i implement the items part

         if( (name = strstr(buffer, "opposing ")) ) {
            name += strlen("opposing ");
            char* end = name;
            while(*end != ' ') { end++; }
            *end = '\0';//Terminate the name
            updateMoveset(fight->opponent_team, name, loc);
         } else {
            char* end = buffer;
            while(*end != ' ') { end++; }
            *end = '\0';
            updateMoveset(fight->my_team, buffer, loc);
         }
      }

      //Get other pokemon my team used
      if( (loc = strstr(buffer, "Go! ")) ) {
         buffer[read - 2] = '\0'; //Remove !\n

         loc += strlen("Go! ");
         updateStatus(fight->my_team, loc, 1);
      }

      //Get other pokemon opponent team used
      if( (loc = strstr(buffer, "sent out ")) ) {
         buffer[read - 2] = '\0'; //Remove !\n

         loc += strlen("sent out ");
         updateStatus(fight->opponent_team, loc, 1);
      }

      //Get abilities used
      //IMPORTANT ABILITY CHECK MUST BE AFTER FRISK CHECK//
      //IMPORTANT ABILITY CHECK MUST BE AFTER FRISK CHECK//
      if( (loc = strstr(buffer, "[")) ) {
         char* end = loc;
         while(*end != ']') { end++; }
         *end = '\0';         

         char* name;
         if( (name = strstr(buffer, "opposing ")) ) {
            //This is an opponent's pokemon's ability
            name += strlen("opposing ");
            end = name;
            while(*end != '\'') { end++; }
            *end = '\0';
            end += 3; // Set end to start of ability
            updateAbility(fight->opponent_team, name, end);
         } else {
            //This is my pokemon's ability
            name = loc + 1;
            end = name;
            while(*end != '\'') { end++; }
            *end = '\0';
            end += 3;
            updateAbility(fight->my_team, name, end);
         }
      }

      //Get dynamax
      if( (loc = strstr(buffer, "Dynamax!")) ) {
         buffer[read - 2] = '\0'; //Remove )\n at end

         char* name;
         if( (name = strstr(buffer, "opposing ")) ) {
            name += strlen("opposing ");
            char* end = name;
            while(*end != '\'') { end++; }
            *end = '\0';
            updateDynamax(fight->opponent_team, name);
         } else {
            name = buffer + 1;
            char* end = name;
            while(*end != '\'') { end++; }
            *end = '\0';
            updateDynamax(fight->my_team, name);
         }
      }

   }

   free(buffer);
   return 0;
}


//Get the number of battles in the folder - essentially just count number of files in folder
//Attempts to create the directory if it fails to open the first time
//Return -1 on failure, returns number of files on success
size_t numBattles(char* dir_name) {
   struct dirent* dirn;
   DIR* dirc = opendir(dir_name);

   if (!dirc) {
      if(!mkdir(dir_name, 0777)) { // Create directory if it didnt open
         return 0;
      } else {
         return -1;
      }
   }

   size_t num = 0;
   while( (dirn = readdir(dirc)) ) { num++; }

   closedir(dirc);
   return num - 2; // Remove the . and .. directories from the count 
}


#endif /*READER_H*/
