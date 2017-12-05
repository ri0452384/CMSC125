#include <windows.h>
#include <tchar.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <unistd.h>

#ifdef _WIN32_WINNT
#undef _WIN32_WINNT
#endif
#define _WIN32_WINNT 0x0501

//variable that controls to relaunch the shell. only switches by inputting cmd command.
int restart=0;

//built-in function declarations go here
int shell_dir(char **args);
int shell_exit(char **args);
int shell_cls();
int shell_cd(char **args);
int shell_chdir(char **args);
int shell_cmd();
int shell_copy(char **args);
int shell_del(char **args);
int shell_move(char **args);
int shell_time(char **args);
int shell_date(char **args);
int shell_mkdir(char **args);
int shell_rmdir(char **args);
int shell_type(char **args);


//number of built-in commands
int num_built_in_commands = 14;

//array of built-in commands in string form
char *built_in_commands[] = {
  "dir",
  "exit",
  "cls",
  "cd",
  "chdir",
  "cmd",
  "copy",
  "del",
  "move",
  "time",
  "date",
  "mkdir",
  "rmdir",
  "type"
};

//array of pointers to the addresses for the different functions
int (*built_in_pointers[]) (char **) = {
  &shell_dir,
  &shell_exit,
  &shell_cls,
  &shell_cd,
  &shell_chdir,
  &shell_cmd,
  &shell_copy,
  &shell_del,
  &shell_move,
  &shell_time,
  &shell_date,
  &shell_mkdir,
  &shell_rmdir,
  &shell_type
  };

//CurDirBuffer is the container for the current directory
#define BUFFER_SIZE MAX_PATH    //The maximum path of 32,767 characters is approximate as per MSDN documentation
TCHAR CurDir_Buffer[BUFFER_SIZE+1]; // the +1 is for the NULL terminating character

//FUNCTION IMPLEMENTATIONS GO HERE:

//exit, returns 0 to exit from the shell_loop
int shell_exit(char *argv[])
{
  return 0;
}
/*
    dir: displays all files and folders in the current directory. this is done via traversing each content and displaying the file name.
    FindFirstFile = folder info, FindNextFile = file/subdirectory info
*/
int shell_dir(char *argv[])
{
    WIN32_FIND_DATA find_data;
    LARGE_INTEGER file_size;
    LARGE_INTEGER total_bytes;
    TCHAR target_folder[BUFFER_SIZE];
    HANDLE find_handle = INVALID_HANDLE_VALUE;

       if(argv[1] == NULL){
            //displays the current directory if no parameters
        argv[1] = ".";
       }


       total_bytes.LowPart = 0;
        total_bytes.HighPart = 0;
       // locates first file in the folder
       find_handle = FindFirstFileA(argv[1], &find_data);
            if(find_handle == INVALID_HANDLE_VALUE){
                    printf("\tNo file/folder named '%s' found!\n",target_folder);
                return 1;
            }
            else{
                _tprintf(TEXT("\nDisplaying results for: %s\n\n"), argv[1]);
            }
            //check if the first handle is for a folder or a file.
         if (find_data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
          {
              //if handle is a folder... need to add the \* wildcard to open its contents
               strcpy(target_folder, argv[1]);
               strcat(target_folder, TEXT("\\*"));
                find_handle = FindFirstFileA(target_folder, &find_data);
          }else{
                //if handle is a file...
                strcpy(target_folder, argv[1]);
                find_handle = FindFirstFileA(target_folder, &find_data);
          }

    int folder_count, file_count = 0;
       do
       {
           //get the file time struct
                FILETIME ft = find_data.ftLastWriteTime;
                SYSTEMTIME st;
                FileTimeToLocalFileTime( &ft, &ft );
                FileTimeToSystemTime( &ft, &st );
                char local_date[255], local_time[255];
                GetDateFormat( LOCALE_USER_DEFAULT,
                              DATE_SHORTDATE,
                              &st,
                              NULL,
                              local_date,
                              255 );
                GetTimeFormat( LOCALE_USER_DEFAULT,
                              0,
                              &st,
                              NULL,
                              local_time,
                              255 );

          // if the next handle is a folder
          if (find_data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
          {
              _tprintf("%s %s [FOLDER]\t\t%s\n", local_date, local_time, find_data.cFileName);
             folder_count++;
          }
          else
          {
              //if the handle is for a file
             file_size.LowPart = find_data.nFileSizeLow;
                 total_bytes.LowPart += find_data.nFileSizeLow;
                 file_size.HighPart = find_data.nFileSizeHigh;
                 total_bytes.HighPart += find_data.nFileSizeHigh;
                 printf("%s %s\t\t %llu bytes", local_date, local_time,  file_size.QuadPart);
                 printf(" %s\n",find_data.cFileName);
                 file_count++;
          }
       }
       while (FindNextFile(find_handle, &find_data) != 0);

        printf("\t\t%d File%s, %d Folder%s\n\t\tTotal size: %llu bytes",
               file_count,
               ((file_count > 1) ? "s":""),
               folder_count,
               ((folder_count > 1) ? "s":""),
               total_bytes.QuadPart);
       FindClose(find_handle);
   return 1;
}

// clear screen: replace all characters displayed on console with spaces and move cursor back to 0,0
int shell_cls()
  {
      CONSOLE_SCREEN_BUFFER_INFO screen_info;
      HANDLE   output_handle;
      DWORD    count;
      DWORD    screen_spaces;
      COORD    first_cell = { 0, 0 };

      output_handle = GetStdHandle( STD_OUTPUT_HANDLE );
      // get dimensions(x&y) of the console
      GetConsoleScreenBufferInfo(output_handle, &screen_info);
      // x * y = total number of character cells on screen
      screen_spaces = screen_info.dwSize.X *screen_info.dwSize.Y;
      // replace all cells with a blank space
      FillConsoleOutputCharacter(output_handle, ' ', screen_spaces, first_cell, &count);
      // set cursor back to first cell before printing the prompt for next command
      SetConsoleCursorPosition( output_handle, first_cell );
      return 1;
  }

  /*
    cd, display if no arguments or change directory if argv[1] is valid,
    '.' for same directory, '..' for up one level
   */
int shell_cd(char *argv[])
{
        GetCurrentDirectory(BUFFER_SIZE, CurDir_Buffer);
        if(argv[1] == NULL){
            printf("\n%s\n",CurDir_Buffer);
        }
        else
        {
            if( !SetCurrentDirectory(argv[1]))
                printf("%s not found! \n", argv[1]);
        }
      return 1;
    }

// chdir, upon testing with windows cmd, performs exactly the same function as cd
int shell_chdir(char *argv[])
{
        //pardon the shameless copy + paste. 'cd' and 'chdir' really do the same thing in Windows cmd.
        GetCurrentDirectory(BUFFER_SIZE, CurDir_Buffer);
        if(argv[1] == NULL){
            printf("\n%s\n",CurDir_Buffer);
        }
        else
        {
            if( !SetCurrentDirectory(argv[1]))
                printf("%s not found! \n", argv[1]);
        }
      return 1;
    }

//cmd, restarts the program and resets the entire program back to start
int shell_cmd(char *argv[])
{
        //restart variable is flagged to 1 so it will restart the shell_loop
      restart = 1;
      //returns 0 to get out of the current shell_loop, freeing any objects from the heap
      return 0;
    }

/*
    copies a specific file and places it in the specified directory, confirmed working on text files
*/
int shell_copy(char *argv[])
{
        WIN32_FIND_DATA find_data,dest_data;
        TCHAR dest_folder[MAX_PATH];
        HANDLE find_handle,dest_handle = INVALID_HANDLE_VALUE;
        int file_count;

        if(argv[1] ==NULL)
           {
                printf("\nError! Syntax must be [copy]{space}<source_file>{space}<destination_file>\n");
           }

           // Find the first file
            find_handle = FindFirstFile(argv[1], &find_data);
            dest_handle = FindFirstFile(argv[2], &dest_data);
           if(dest_data.dwFileAttributes == FILE_ATTRIBUTE_DIRECTORY){
                    strcpy(dest_folder,argv[2]);
                    strcat(dest_folder,"\\");
           }else{
                strcpy(dest_folder,argv[2]);
           }


        //keep looping until all files have been copied
        do{

                TCHAR temp_dest[MAX_PATH];
                //manipulate temp_dest within the loop, so dest_folder remains unchanged.
                strcpy(temp_dest,dest_folder);
                if(dest_data.dwFileAttributes == FILE_ATTRIBUTE_DIRECTORY){
                        strcat(temp_dest,find_data.cFileName);
                    if(CopyFile(find_data.cFileName,temp_dest,0) == 0){
                       printf("error while copying to folder:%s", temp_dest);
                        return 1;
                   }
                }else{
                    _tprintf(TEXT("\ncopying %s to: %s\n\n"), find_data.cFileName,dest_folder);
                    GetFullPathName(dest_folder,BUFFER_SIZE,dest_folder,NULL);
                    //concatenate the folder and the new filenames together for the destination filename
                    if(CopyFile(find_data.cFileName,argv[2],0) == 0){
                       printf("error while copying to file!");
                        return 1;
                   }
                }
            file_count++;
        }while (FindNextFile(find_handle, &find_data) != 0);

        printf("%d file%s copied successfully.\n",file_count,(file_count > 1 ? "s":""));
        FindClose(find_handle);
        FindClose(dest_handle);
        return 1;
    }
/*
    deletes a file or group of files
*/
int shell_del(char *argv[]){
    //implement multiple file deletion here
    WIN32_FIND_DATA find_data;
    TCHAR target_folder[BUFFER_SIZE];
    HANDLE find_handle = INVALID_HANDLE_VALUE;
    int file_count = 0;

       if(argv[1] == NULL){
            //displays error because it needs a target as a parameter
            printf("Error: missing target file/s!");
       }


       // locates first file in the folder
       find_handle = FindFirstFileA(argv[1], &find_data);
            if(find_handle == INVALID_HANDLE_VALUE){
                    printf("\tNo file/folder named '%s' found!\n",target_folder);
                return 1;
            }
            //check if the first handle is for a folder or a file.
         if (find_data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
          {
              //if handle is a folder... need to add the \ strcpy(target_folder, argv[1]);
               strcat(target_folder, TEXT("\\"));
          }
       do
       {
          // if the next handle is a folder
          if (find_data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
          {
              //if the handle is for a folder
              printf("folder found, using \"rmdir<space>[target_folder]\"instead.");
              shell_rmdir(argv);
              return 1;
          }
          else
          {
              //if the handle is for a file, single delete here
               int res = delete_single_file(find_data);
               if(res != 0){
                    printf("%s deleted successfully",find_data.cFileName);
                    file_count++;
               }
          }
       }
       while (FindNextFile(find_handle, &find_data) != 0);
    printf("\n%d file%s deleted successfully.\n",file_count,(file_count > 1 ? "s":""));
    FindClose(find_handle);

    return 1;
}

/*
    deletes a single file given the find data to the target file. used by MOVE and DEL commands
*/
int delete_single_file(WIN32_FIND_DATA find_data){
    HANDLE file_handle;
    LPCWSTR target_file = find_data.cFileName;

// Create a file handle
file_handle = CreateFile(target_file, //file to be opened
                        GENERIC_READ, //open for writing
                        FILE_SHARE_READ, //share for writing
                        NULL, //default security
                        CREATE_ALWAYS, //create new file only
                        FILE_ATTRIBUTE_ARCHIVE | SECURITY_IMPERSONATION,//archive and impersonate client
                        NULL); //no attribute template

// Check the handle, then open...
if(file_handle == INVALID_HANDLE_VALUE)
printf("\nCould not open %s!\n", target_file);

// delete requires that all file handles to the target are closed
if(CloseHandle(file_handle) == 0)
    printf("\nCloseHandle() for %S file failed!\n", target_file);

return  DeleteFile(target_file);
}
/*
    copies the target file to another location, and deletes the copy on the original location
*/
int shell_move(char *argv[]){
    WIN32_FIND_DATA find_data,dest_data;
    TCHAR source_folder[MAX_PATH];
    TCHAR dest_folder[MAX_PATH];
    HANDLE find_handle,dest_handle = INVALID_HANDLE_VALUE;
    int file_count;

    if(argv[1] ==NULL)
       {
            printf("\nError! Syntax must be [copy]{space}<source_file>{space}<destination_file>\n");
       }

       // Find the first file
        find_handle = FindFirstFile(argv[1], &find_data);
        dest_handle = FindFirstFile(argv[2], &dest_data);
       if(dest_data.dwFileAttributes == FILE_ATTRIBUTE_DIRECTORY){
                strcpy(dest_folder,argv[2]);
                strcat(dest_folder,"\\");
       }else{
            strcpy(dest_folder,argv[2]);
       }


    //keep looping until all files have been copied
    do{

            TCHAR temp_dest[MAX_PATH];
            //manipulate temp_dest within the loop, so dest_folder remains unchanged.
            strcpy(temp_dest,dest_folder);
            if(dest_data.dwFileAttributes == FILE_ATTRIBUTE_DIRECTORY){
                    strcat(temp_dest,find_data.cFileName);
                if(MoveFileA(find_data.cFileName,temp_dest) == 0){
                   printf("error while copying to folder:%s", temp_dest);
                    return 1;
               }
               delete_single_file(find_data);
            }else{
                _tprintf(TEXT("\ncopying %s to: %s\n\n"), find_data.cFileName,dest_folder);
                GetFullPathName(dest_folder,BUFFER_SIZE,dest_folder,NULL);
                //concatenate the folder and the new filenames together for the destination filename
                if(MoveFileA(find_data.cFileName,dest_folder) == 0){
                   printf("error while moving file!");
                    return 1;
               }
               //delete the original file
               delete_single_file(find_data);
            }
        file_count++;
    }while (FindNextFile(find_handle, &find_data) != 0);

    printf("%d file%s moved successfully.\n",file_count,(file_count > 1 ? "s":""));
    FindClose(find_handle);
    FindClose(dest_handle);
    return 1;
}


    int shell_type(char *argv[]){
        FILE *target_file;
        char c;

        // Open file
        target_file = fopen(argv[1], "r");
        if (target_file == NULL)
        {
            printf("Error: Unable to open %s \n",argv[1]);
            return 1;
        }

        // Read contents from file
        c = fgetc(target_file);
        while (c != EOF)
        {
            printf ("%c", c);
            c = fgetc(target_file);
        }

        fclose(target_file);
        return 1;
    }


int shell_time(char *argv[]){
    char *day_text[] = {"","Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"};
    SYSTEMTIME time_struct;

    if(argv[1] == NULL){
        //show time
        GetLocalTime(&time_struct);
        printf("Current time is: %d : %d : %d\n",time_struct.wHour,time_struct.wMinute,time_struct.wSecond);

    }
        //set time
        char *new_time[10];
        printf("Enter the new time: (hh:mm:ss): ");
        scanf("%s", new_time);
        SetLocalTime(new_time);
    return 1;
}

int shell_date(char *argv[]){
    char *month_text[] = {"","January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};
    char *day_text[] = {"","Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"};
    SYSTEMTIME time_struct;

    if(argv[1] == NULL){
        //show time if no parameters
        GetSystemTime(&time_struct);
        int year = time_struct.wYear;
        int month = time_struct.wMonth;
        int day = time_struct.wDay;
        int week;

        //calculate what day it is using Key Value method
        week =  ( (day+=(month <3? year -- :(year -2))), (23* month/9+ day +4 + year /4- year /100+ year/400) ) % 7;

        printf("The current date is: %s, %s-%d-%d \n",day_text[week],month_text[time_struct.wMonth],time_struct.wDay,time_struct.wYear);

    }
        //set date
        char *new_date[10];
        printf("Enter the new date: (mm-dd-yyyy): ");
        scanf("%s", new_date);
        SetLocalTime(new_date);
    return 1;
}

int shell_mkdir(char *argv[]){
LPCWSTR directory_path;
directory_path = argv[1];

// Create a new directory.
if(!CreateDirectory(directory_path, NULL))
printf("\nError: Unable to create directory named %S.\n", directory_path);
else
printf("\n%S folder created successfully.\n", directory_path);
}


int shell_rmdir(char *argv[]){
LPCWSTR directory_path;
directory_path = argv[1];

// deletes the directory given its relative path
if(RemoveDirectory(directory_path) != 0)
printf("\nFolder deleted successfully.\n", directory_path);
else
printf("\nCould not delete folder.\n", directory_path);

return 1;
}
// end of all built-in function implementations

//executes all built-in commands, if not found on the list, it returns command not found
int shell_execute(TCHAR *argv[])
{
    int i;
    if (argv[0] == NULL) {
      // An empty command was entered, just displays the prompt again.
      return 1;
    }
    for (i = 0; i < num_built_in_commands; i++) {
            if(strcmp(argv[0],"quit") == 0)
                {
                argv[0] = "exit";
                }
            if(strcmp(argv[0],"cd..") == 0)
                {
                argv[0] = "cd";
                argv[1] = "..";
                }
            if(strcmp(argv[0],"cd\\") == 0)
                {
                argv[0] = "cd";
                argv[1] = "\\";
                }
          if ( strcmp(argv[0], built_in_commands[i]) == 0) {
          return (*built_in_pointers[i])(argv);
          }
    }
    printf("Error: \"%s\"is not a built-in command.",argv[0]);
    return 1;
}

#define TOKEN_BUFFER_SIZE 64
#define TOKEN_DELIMITERS " /\t\r\n\a"
//should return a NULL-terminated array of pointers
char **shell_tokenize(char *user_input)
{
  int buffer_size = TOKEN_BUFFER_SIZE, position = 0;
  char **tokens = malloc(buffer_size * sizeof(char*));
  char *token;

  if (!tokens) {
    fprintf(stderr, "Shell: Unable to allocate!\n");
    exit(EXIT_FAILURE);
  }

  token = strtok(user_input, TOKEN_DELIMITERS);
  while (token != NULL) {
    tokens[position] = token;
    position++;

    if (position >= buffer_size) {
      buffer_size += TOKEN_BUFFER_SIZE;
      tokens = realloc(tokens, buffer_size * sizeof(char*));
      if (!tokens) {
        fprintf(stderr, "Shell: Unable to re-allocate!\n");
        exit(EXIT_FAILURE);
      }
    }
    token = strtok(NULL, TOKEN_DELIMITERS);
  }
  tokens[position] = NULL;
  return tokens;
}

//used to get a line from the user
#define LINE_BUFFER_SIZE 1024
char *shell_read_line(void)
{
  int buffer_size = LINE_BUFFER_SIZE;
  int position = 0;
  char *buffer = malloc(sizeof(char) * buffer_size);
  int c;

  if (!buffer) {
    fprintf(stderr, "Unable to allocate!\n");
    exit(EXIT_FAILURE);
  }

  while (1) {
    // Read a character
    c = getchar();
    c = tolower(c);

    // should terminate with a NULL character
    if (c == EOF || c == '\n') {
      buffer[position] = '\0';
      return buffer;
    } else {
      buffer[position] = c;
    }
    position++;

    // allocate more space if it exceeds the buffer
    if (position >= buffer_size) {
      buffer_size += LINE_BUFFER_SIZE;
      buffer = realloc(buffer, buffer_size);
      if (!buffer) {
        fprintf(stderr, "Unable to allocate!\n");
        exit(EXIT_FAILURE);
      }
    }
  }
}

//main loop, used to receive user input over and over until exit is called.
void shell_loop()
{
  char *user_input;
  char **arguments;
  int keep_running;

    printf("My First Shell 1.03 build 34 \n by Rayven Ingles, BSCS 4\n");
  do {
    //get the current directory where the program is running
    GetCurrentDirectory(BUFFER_SIZE, CurDir_Buffer);
    printf(("\n%s>"), CurDir_Buffer);
    //printf("%p> ", &current_directory);
    user_input = shell_read_line();
    arguments = shell_tokenize(user_input);
    keep_running = shell_execute(arguments);

    //free up heap objects here
    free(user_input);
    free(arguments);

  } while (keep_running !=0);
}

//header function, nothing but loop and exiting the program.
int main(void)
{
    do{
        //set to 0 at every start of the program so it can exit when invoking exit command
        restart = 0;
         shell_loop();
         if(restart == 0){
            return EXIT_SUCCESS;
         }
    }while(restart==1);

    return 0;
}
