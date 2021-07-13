#ifndef STRIPPER_H
#define STRIPPER_H

#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <dirent.h>



int processFile(char* dirn, char* filename, size_t battle_num);
void remove_equal_return(char* file_contents);
void remove_UTF(int fd);
size_t numBattles(char* dir_name);


const char* DESTINATION_DIR = "ProcessedGames/";
const char* SOURCE_DIR = "TBAnalyzed/";



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
      printf("Processing game #%06zu  ( %s )\n", start_num, dirn->d_name);
      if (strcmp(dirn->d_name, ".") && strcmp(dirn->d_name, "..")) {
         processFile(argv[1], dirn->d_name, start_num);
         start_num++;
      }
   }

   free(dest_dir);
   free(src_dir);
   return 0;
}


//Rename the below to process file or something
int processFile(char* dirn, char* filename, size_t battle_num) {
   if(battle_num > 999999) { printf("battle_num is too big"); return -1; }
   
   //Setup file path
   char* src_path = malloc(strlen(SOURCE_DIR) + strlen(dirn) + 1 + strlen(filename) + 1);
   strcpy(src_path, SOURCE_DIR);
   strcpy(src_path + strlen(SOURCE_DIR), dirn);
   src_path[strlen(SOURCE_DIR) + strlen(dirn)] = '/';
   strcpy(src_path + strlen(SOURCE_DIR) + strlen(dirn) + 1, filename); 
   
   //OPEN A FILE HERE
   int fd = open(src_path, O_RDONLY);
   if (fd == -1) {
      printf("Error opening file\n");
      exit(1);
   }

   //Setup destination filepath
   char* dest_path = malloc(strlen(DESTINATION_DIR) + strlen(dirn) + 1 + strlen("Battle") + 7);
   strcpy(dest_path, DESTINATION_DIR);
   strcpy(dest_path + strlen(DESTINATION_DIR), dirn);
   dest_path[strlen(DESTINATION_DIR) + strlen(dirn)] = '/';
   strcpy(dest_path + strlen(DESTINATION_DIR) + strlen(dirn) + 1, "Battle");

   char* number = malloc(7);
   snprintf(number, 7, "%06zu", battle_num);
   number[6] = '\0';
 
   strcpy(dest_path + strlen(DESTINATION_DIR) + strlen(dirn) + 1 + strlen("Battle"), number); 
   
   //MAKE FILE TO SAVE ESSENTIALS
   int save_fd = open(dest_path, O_RDWR | O_CREAT, S_IRWXU | S_IRGRP | S_IROTH);
   if (save_fd == -1) {
      close(fd);
      printf("Error creating file");
      free(src_path); free(dest_path); free(number);
      exit(1);
   }


   //GET STAT STRUCT
   struct stat sb;
   if (fstat(fd, &sb)) {
      printf("Error getting fstat\n");
   }


   //MMAP THE FILE - SHOULD BE RELATIVELY SMALL  ~4KB
   char* file_contents = mmap(NULL, sb.st_size, PROT_READ | PROT_WRITE, MAP_PRIVATE, fd , 0);
   if (!file_contents) {
      printf("Error in mmap\n");
   }

   //REMOVE THE EQUAL SIGN AND CARRIAGE RETURN CHROME ADDS TO EACH LINE
   remove_equal_return(file_contents);
   

   //GO TO BEGINNING OF LOGS
   char* current = strstr(file_contents, "<div class=3D\"chat battle-history\">");
   if (!current) {
      printf("Problem with strstr finding beginning of logs"); 
   }

   //Get a copy of the teams used, first one is mine second is theirs. Delimited names with '/'
   for(int j = 0; j < 2; j++) {
      current = strstr(current, "display:block;\">");

      if(current == NULL) { printf("Could not find beginning of battle"); return 1; }

      current += 16;

      int offset = 0;
      while(current[offset] != '<') {
         offset++;
      }

      char team[offset + 1]; // Remove white space with this
      
      int written = 0;
      for(int i = 0; i < offset; i++) {
         if (current[i] != ' ') {
            team[written] = current[i];
            written++;
         }
      }
      team[written] = '\0';

      //printf("%s\n", team);//This should save somewhere eventually

      write(save_fd, team, written);
      write(save_fd, "\n", 1);
   }


   //Get each line in the history section and write to a file
   char* br;
   while((current = strstr(current, "battle-history\">"))) {
      current += 16; /*get to start of string*/
      br = strstr(current, "<br>"); /*Find end of string*/

      //Frisk lines have a different html format (idk why) so this avoids skipping over info
      if( strncmp(br - 6, "Frisk]", 6) == 0) { 
         br = strstr(br+1, "<br>");
      }

      size_t line_length = br - current;

      //rewrite so ensure all writes
      write(save_fd, current, line_length);
      write(save_fd, "\n", 1);


      char* end_check = strndup(current, line_length);
      if(strstr(end_check, "won the battle!")) { break; }
      free(end_check);
   }
 
   munmap(file_contents, sb.st_size);

   remove_UTF(save_fd); 

   close(fd);
   close(save_fd);
   free(dest_path);
   free(src_path);
   free(number);

   return 0;
}


//Inspired by:
//stackoverflow.com/questions/9895216/how-to-remove-all-occurrences-of-a-given-character-from-string-in-c
void remove_equal_return(char* file_contents) {
   char *pr = file_contents, *pw = file_contents;
   
   while(*pr) {
      if(pr[0] == 61 && pr[1] == 13 && pr[2] == 10) {//this is '=\r\n' - limits char per line when i save the html
         pr+=3;
      }
      *pw = *pr;
      pw++;
      pr++;
   }
   *pw = '\0';
}


//Remove utf sequences and other things from battle history
void remove_UTF(int fd){
   //GET STAT STRUCT
   struct stat sb;
   if (fstat(fd, &sb)) {
      printf("Error getting fstat\n");
   }


   //MMAP THE FILE - SHOULD BE RELATIVELY SMALL  ~4KB
   char* file_contents = mmap(NULL, sb.st_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd , 0);
   if (!file_contents) {
      printf("Error in mmap\n");
   }

   //Remove UTF characters in the file and replace if desired
   size_t written = 0;
   for(size_t i = 0; i < sb.st_size; i++) { 
      //Remove <strong>
      if(!strncmp(file_contents+i, "<strong>", 8)) {
         i += 7;
         continue;
      }

      //Remove <br>
      if(!strncmp(file_contents+i, "<br>", 4)) {
         i += 3;
         continue;
      }

      //Remove </strong>
      if(!strncmp(file_contents+i, "</strong>", 9)) {
         i += 8;
         continue;
      }

      //Remove </h2>
      if(!strncmp(file_contents+i, "</h2>", 5)) {
         i += 4;
         continue;
      }

      //Remove <small>
      if(!strncmp(file_contents+i, "<small>", 7)) {
         i += 6;
         continue;
      }

      //Remove </small>
      if(!strncmp(file_contents+i, "</small>", 8)) {
         i += 7;
         continue;
      }

      //Remove <div class=3D"spacer battle-history">
      if(!strncmp(file_contents+i, "<div class=3D\"spacer battle-history\">", 37)) {
         i += 36;
         continue;
      }

      //Remove <abbr title.....>
      if(!strncmp(file_contents+i, "<abbr title", 11)) {
         i += 10;
         while(file_contents[i] != '>') {
            i++;
         }
         continue;
      }

      //Remove </abbr>
      if(!strncmp(file_contents+i, "</abbr>", 7)) {
         i += 6;
         continue;
      }

      //Replace a character with a dash
      if(!strncmp(file_contents+i, "=E2=80=93", 9)) {
         //Replace with a dash
         file_contents[written] = '-';
         written++;
         i += 8;
         continue;
      }

      //Replace accented e for e
      if(!strncmp(file_contents+i, "=C3=A9", 6)) {
         file_contents[written] = 'e';
         written++;
         i += 5;
         continue;
      }

      //Replace apostrophe
      if(!strncmp(file_contents+i, "=E2=80=99", 9)) {
         file_contents[written] = '\'';
         written++;
         i += 8;
         continue;
      }

      //Remove <div class=3D"chat message-error">
      if(!strncmp(file_contents+i, "<div class=3D\"chat message-error\">", 34)) {
         i += 33;
         continue;
      }

      //Remove </div>
      if(!strncmp(file_contents+i, "</div>", 6)) {
         i += 5;
         continue;
      }

      file_contents[written] = file_contents[i];
      written++;
   }

   file_contents[written] = '\0';
   written++;

   munmap(file_contents, sb.st_size);
   ftruncate(fd, written);
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

#endif /*STRIPPER_H*/
