#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    const int BLOCK_SIZE = 512;
    // Check correct CLAs
    if (argc != 2)
    {
        printf("Usage: ./filter IMAGE\n");
        return 1;
    }

    // If won't open return the following
    FILE *rawFile = fopen(argv[1], "r");
    if (rawFile == NULL)
    {
        printf("Could not open.\n");
        return 1;
    }

    // Create buffer and go through file
    unsigned char buffer[BLOCK_SIZE];
    int numJPG = 0;
    FILE *img = NULL;
    char *filename = malloc(8 *sizeof(char));

    while (fread(buffer, sizeof(char), BLOCK_SIZE, rawFile))
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
                sprintf(filename, "%03i.jpg", numJPG);
                img = fopen(filename, "w");
                numJPG++;
        }
        if (img != NULL)
        {
           fwrite(buffer, sizeof(char), BLOCK_SIZE, img);
        }
    }
    free(filename);
    fclose(img);
    fclose(rawFile);
    return 0;

}

