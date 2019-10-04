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

//Yes, this *is* the source code for the program
//you're interacting with.

#include <stdio.h>

typedef struct
{
const char *fname;
const unsigned int authlevel;
}FENTRY;

#define NUM_FENTRY 2

const FENTRY flist[]={
    {"main.c",3},
    {"flag.txt",126}
    };


void printfile(const char* fname)
{
    FILE *file=fopen(fname,"rt");
    char c;
    while( !feof(file) && (c=fgetc(file))!=EOF ) putchar(c);
    fclose(file);
}

int main(void)
{
    unsigned int authlevel=5;
    char name[32];
    int i;
    int choice;

    printf("Welcome to remote file viewing, guest access mode.\n");
    printf("What is your name? ");
    fgets(name,34,stdin);
    printf("Your authorization level is %03d.\n",authlevel);

    for(;;)
    {
        printf("0: exit\n");
        for(i=0;i<NUM_FENTRY;++i)
            printf("%d: Level %03d: view \"%s\"\n",i+1,
                flist[i].authlevel,flist[i].fname);
        
        if(scanf("%d",&choice)!=1)
        {
            scanf("%*[^\n]%1*[\n]");
            continue;
        }
        
        if(choice==0) return 0;

        if(choice>NUM_FENTRY)
        {
            printf("Invalid choice\n");
            continue;
        }

        if(authlevel>=flist[choice-1].authlevel)
            printfile(flist[choice-1].fname);
        else printf("Error: Authorization level of %03d+ required.  "
            "Your level is %03d.\n",flist[choice-1].authlevel,
            authlevel);

    }

    return 0;
}
