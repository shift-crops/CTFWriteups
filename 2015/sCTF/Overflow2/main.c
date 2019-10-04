/*
Copyright (c) 2015, Cory L.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

//intended for use on 32 bit little endian systems

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <signal.h>

void printfile(const char* fname)
{
    FILE *file=fopen(fname,"rt");
    char c;
    while( !feof(file) && (c=fgetc(file))!=EOF ) putchar(c);
    fclose(file);
}

void show_soln(void)
    {
    printfile("flag.txt");
    fflush(stdout);
    }

void test(void)
{
    char name[32];
    

    printf("What is your name? ");
    fgets(name,256,stdin);
    
    srand(time(NULL));

    if( (rand()%100)==(rand()%100) )
    {
        printf("You have good luck, but it still won't be that easy.\n");
        //show_soln();
    }
    else
    {
        printf("You have bad luck.\n");
    }
}

//This function will run when the program segfaults.
//This is a workaround for a "feature" of the wrapper program
//making this a network service.
void handle_segfault(int snum)
{
    printf("segmentation fault\n");
    exit(0);
}

int main(void)
{
    //use a custom handler for any segfaults that occur
    signal(SIGSEGV,handle_segfault);
    
    printf("Let's play a little game of luck!\n");
    test();
    printf("Goodbye.\n");
    return 0;
}

