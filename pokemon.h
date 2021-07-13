#ifndef POKEMON_H
#define POKEMON_H

#include <stdlib.h>
#include <string.h>
#include <stdio.h>

const size_t MAX_NAME_LENGTH = 32;
const size_t MAX_MOVE_LENGTH = 32;
const size_t NUMBER_OF_MOVES = 8;  // Change value in struct Pokemon{ moveset[*] } if you change this  V
                          //                                                                           |
typedef struct Pokemon {  //                                                                           |
   char* name;            //                                                                           |
   char* ability;         //                                                                           |
   char* moveset[8];      // Change const size_t NUMBER_OF_MOVES if you change this as well            ^
   char* item;
} pokemon;


void releasePokemon(pokemon* mon);

//Make a new pokemon with fields
//Must include a name, rest of the fields may be left NULL
pokemon* Pokemon(char* name, char* ability, char** moveset, char* item) {
  
   //return NULL if no name or name is too long
   if(!name || (strlen(name) > MAX_NAME_LENGTH - 1)) {
      return NULL;
   }
 
   pokemon* newmon = malloc(sizeof(pokemon));
   memset(newmon, 0, sizeof(pokemon));

   if(!newmon) {
      return NULL;
   }
    
   newmon->name = malloc(MAX_NAME_LENGTH);

   if(!(newmon->name)) {
      free(newmon);
      return NULL;
   }

   strncpy(newmon->name, name, MAX_NAME_LENGTH);
   newmon->name[MAX_NAME_LENGTH - 1] = '\0';//null terminate just in case

   //Set ability flag
   if(ability) {
      newmon->ability = malloc(MAX_NAME_LENGTH); 
      
      if(!(newmon->ability)) {
         releasePokemon(newmon);
         return NULL;
      }

      strncpy(newmon->ability, ability, MAX_NAME_LENGTH);
      newmon->ability[MAX_NAME_LENGTH - 1] = '\0';
   } else {
      newmon->ability = NULL;
   }

   //Set moveset
   if(moveset) {
      //Copy over at most the 8 moves
      for(size_t i = 0; i < NUMBER_OF_MOVES; i++) {
         char* current_move = *(moveset + i);
         
         if(!current_move) {
            newmon->moveset[i] = NULL;
            break;
         }
         
         newmon->moveset[i] = malloc(MAX_MOVE_LENGTH);

         if(!(newmon->moveset + i)) {
            releasePokemon(newmon); 
            return NULL;
         }

         strncpy(newmon->moveset[i], current_move, MAX_MOVE_LENGTH);
         newmon->moveset[i][MAX_MOVE_LENGTH - 1] = '\0';
      } 
   } else {
      newmon->moveset[0] = NULL;
   }

   if(item) {
      newmon->item = malloc(MAX_NAME_LENGTH);
      
      if(!newmon->item) {
         releasePokemon(newmon);
         return NULL;
      }

      strncpy(newmon->item, item, MAX_NAME_LENGTH);
      newmon->item[MAX_NAME_LENGTH - 1] = '\0';
   } else {
      newmon->item = NULL;
   }

   return newmon;
}


//Print out info for a pokemon
void printMonInfo(pokemon* mon, FILE* fp) {
   fprintf(fp, "%s\n", mon->name);
   fprintf(fp, "Ability: %s\n", mon->ability);
   fprintf(fp, "Item: %s\n", mon->item);
   fprintf(fp, "Moveset:\n");
   for(size_t i = 0; i < NUMBER_OF_MOVES; i++) {
      fprintf(fp, "\t%s\n", mon->moveset[i]);
   }
   fprintf(fp, "\n");
   return;
}


//Add move to moveset
//Returns -1 if could not add, 0 if successful
int addMove(pokemon* mon, char* move) {
   if(!mon) { return -1; }

   for(size_t i = 0; i < NUMBER_OF_MOVES; i++) {
      if(mon->moveset[i] && (strcmp(move, mon->moveset[i]) == 0)) { //Don't add repeat moves
         return 0;
      }
      
      if(!mon->moveset[i]) {
         mon->moveset[i] = malloc(MAX_MOVE_LENGTH);

         if(!(mon->moveset + i)) {
            return -1;
         }

         strncpy(mon->moveset[i], move, MAX_MOVE_LENGTH);
         mon->moveset[i][MAX_MOVE_LENGTH - 1] = '\0';
         return 0;
      }
   }
   return -1;
}


//Add ability
//Returns -1 if failed, 0 if successful
int addAbility(pokemon* mon, char* ability) {
   if(!mon) { return -1; }

   if(!mon->ability) {
      mon->ability = malloc(MAX_NAME_LENGTH);

      if(!mon->ability) {
         return -1;
      }

      strncpy(mon->ability, ability, MAX_NAME_LENGTH);
      mon->ability[MAX_NAME_LENGTH - 1] = '\0';
      return 0;
   }
   return -1;
}


//Add item to pokemon
//Returns -1 on failure, 0 on success
int addItem(pokemon* mon, char* item) {
   if(!mon) { return -1; }

   if(!mon->item) {
      mon->item = malloc(MAX_NAME_LENGTH);
      
      if(!mon->item) {
         return -1;
      }

      strncpy(mon->item, item, MAX_NAME_LENGTH);
      mon->item[MAX_NAME_LENGTH - 1] = '\0';
      return 0;
   }
   return -1;
}


//Free a pokemon and free up any space it is using
void releasePokemon(pokemon* mon) {
   
   free(mon->name);
   
   if (mon->ability) { free(mon->ability); }
   
   for(size_t i = 0; i < NUMBER_OF_MOVES ; i++) {
      if(mon->moveset[i]) { free(mon->moveset[i]); }
      else { break; }
   }
   
   if (mon->item) { free(mon->item); }

   free(mon);   

   return;
}

#endif /* POKEMON_H */
