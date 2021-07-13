#ifndef BATTLE_H
#define BATTLE_H

#include "team.h"
#include <string.h>
#include <stdlib.h>


const size_t MAX_LINE_LENGTH = 256;


typedef struct BattleLine {
   char* line;
   void* next;
} battle_line;


typedef struct Battle {
   team* my_team;
   team* opponent_team;
   battle_line* history;
   battle_line* end;
} battle;

//history is pointers to char strings where each line is one part of the history
//once you get to a NULL pointer its over


battle* Battle(void) {
   battle* fight = malloc(sizeof(battle));

   if (!fight) { return NULL; }

   fight->my_team = Team();
   if (!fight->my_team) { free(fight); return NULL;}

   fight->opponent_team = Team();
   if(!fight->opponent_team) { disbandTeam(fight->my_team); free(fight); return NULL;}

   fight->history = NULL;
   fight->end = NULL;
   
   return fight; 
}


//Take a sentence (char string) and append to end of history
//Returns -1 on failure, 0 on success
//This function is broken right now, but i dont need it now so ill fix it later if i even want it
int addLine(battle* fight, char* line) {
   fight->end->next = malloc(sizeof(battle_line));

   if(!fight->end->next) { return -1;}

   size_t length;
   if ((length = strlen(line)) > MAX_LINE_LENGTH) {
      length = MAX_LINE_LENGTH;
   }

   fight->end->line = malloc(length);

   if(!fight->end->line) {
      free(fight->end->next);
      return -1;
   }

   strncpy(fight->end->line, line, length);
   fight->end->line[length - 1] = '\0';   

   fight->end = fight->end->next;
   fight->end->next = NULL;

   return 0;
}


//Remove a battle
void deleteBattle(battle* fight) {
   disbandTeam(fight->my_team);
   disbandTeam(fight->opponent_team);
   battle_line* process_me = fight->history;
   while(process_me) {
      fight->history = process_me->next;
      free(process_me->line);
      free(process_me);
      process_me = fight->history;
   }
   return;
}


#endif /*BATTLE_H*/


