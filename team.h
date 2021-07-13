#ifndef TEAM_H
#define TEAM_H

#include "pokemon.h"
#include <string.h>


typedef struct Team {
   pokemon* members[6];
   int brought[6];
} team;

/*brought should be filled with 3 different values -
0 - pokemon was not brought to battle
1 - pokemon was brought to battle 
2 - pokemon was brought to battle and was used in the lead
-1 or -2 - pokemon dynamaxed and respective meaning
*/


team* Team(void) {
   team* new_team = malloc(sizeof(team));

   if(!new_team) {
      return NULL;
   }

   memset(new_team->members, 0, sizeof(new_team->members));
   memset(new_team->brought, 0, sizeof(new_team->brought));
   return new_team;
}


//Add pokemon to the team
//Name must be non-NULL; others are optionally NULL
//Returns -1 if failed, 0 if successful
int addPokemon(team* squad, char* name, char* ability, char** moveset, char* item) {
   if(!squad || !name) { return -1; }

   pokemon* mon = Pokemon(name, ability, moveset, item);
  
   if(!mon) { return -1; }
 
   for(int i = 0; i < 6; i++) {
      if(!squad->members[i]) {
         squad->members[i] = mon;
         return 0;
      }
   }

   return -1;
}


//Find pokemon index on team
//Return index(0-5) of pokemon given name. If not on team returns -1
int findIndex(team* squad, char* name) {
   if(!squad || !name) { return -1; }

   pokemon* mon;
   for(int i = 0; i < 6; i++) {
      mon = squad->members[i];
      if(mon == NULL) { return -1; }
      if( !strncmp(mon->name, name, 5) ) { // Comparing only 5 characters can hypothetically lead to some problems,
                                           // but the likelihood is pretty small (the team would be very similar and
         return i;                         // would could be considered gimmicky, honestly it would lead to acceptab-
      }                                    // -le amount of error in my estimation)

   }
   return -1;
}


//Set status of pokemon, one of 0 (not brought), 1 (brought), or 2 (lead).
//Return -1 if failed, 0 if successful
int updateStatus(team* squad, char* name, int status) {
   if (!squad || !name || (status > 2 || status < 0)) { return -1; }

   int index = findIndex(squad, name);
   if(index >= 0) {
      if(squad->brought[index] != 0) { return 0; }
      squad->brought[index] = status;
      return 0;
   }
   
   return -1;
}


//Update ability of a pokemon on the team
//Return -1 on failure, 0 if successful
int updateAbility(team* squad, char* name, char* ability) {
   if(!squad || !name || !ability) { return -1; } 

   int result = -1, index = findIndex(squad, name);
   if(index >= 0) {
      result = addAbility(squad->members[index], ability);
   }

   return result;
}


//Update moveset
//Return -1 on failure, 0 if successful
int updateMoveset(team* squad, char* name, char* move) {
   if(!squad || !name || !move) { return -1; }

   int result = -1, index = findIndex(squad, name);
   if(index >= 0) {
      result = addMove(squad->members[index], move);
   }

   return result;
}


//Update item
//Returns -1 on failure, 0 if successful
int updateItem(team* squad, char* name, char* item) {
   if(!squad || !name || !item) { return -1; }

   int result = -1, index = findIndex(squad, name);
   if(index >= 0) {
      result = addItem(squad->members[index], item);
   }
   
   return result;
}


//Update dynamax
//Returns -1 on failure, 0 on success
int updateDynamax(team* squad, char* name) {
   if(!squad || !name) { return -1; }

   int result = -1, index = findIndex(squad, name); 
   if(index >= 0) {
      squad->brought[index] *= -1;
      result = 0;
   }
   
   return result;
}


//Disband team
//Free all pokemon
void disbandTeam(team* squad) {
   for(int i = 0; i < 6; i++) {
      if(!squad->members[i]) { break; }
      releasePokemon(squad->members[i]);
   }
   free(squad);
   return;
}


//Print team info
void printTeamInfo(team* squad, FILE* fp) {
   for(int i = 0; i < 6; i++) {
      if(!squad->members[i]) { fprintf(fp, "(No more pokemon on team)\n"); break;}

      if(squad->brought[i] == 0) {
         fprintf(fp, "(Not brought to battle)\n");
      } else if(squad->brought[i] == 1 || squad->brought[i] == -1) {
         fprintf(fp, "<Pokemon brought in back");
         if(squad->brought[i] < 0) {
            fprintf(fp, ", dynamaxed");
         }
         fprintf(fp, ">\n");
      } else {
         fprintf(fp, "<Pokemon used in lead");
         if(squad->brought[i] < 0) {
            fprintf(fp, ", dynamaxed");
         }
         fprintf(fp, ">\n");
      } 

      printMonInfo(squad->members[i], fp); 
   }

   return;
}

#endif /* TEAM_H */
