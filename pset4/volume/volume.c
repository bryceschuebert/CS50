// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // TODO: Copy header from input file to output file
    uint8_t header[HEADER_SIZE];
    fread(header, HEADER_SIZE, 1, input);
    fwrite(header, HEADER_SIZE, 1, output);


    // TODO: Read samples from input file and write updated data to output file
    int16_t buffer;
    while (fread(&buffer, sizeof(int16_t), 1, input))
    {
        buffer *= factor;
        fwrite(&buffer, sizeof(int16_t), 1, output);
    }

    // Close files
    fclose(input);
    fclose(output);
}





int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover card.raw");
        return 1;
    }
    //Open file for reading
    FILE *input_file = fopen(argv[1], "r");
    //if check Input_file pointer fail to open then REturn error code "Could not open file"
    if (input_file == NULL)
    {
        printf("Could not open file");
        return 2;
    }

    //declare a variable to unsigned char to store 512 chunks array
    unsigned char buffer[512];

    //for the purpose of counting of image later in the loop
    int count_image = 0;

    //An uninitialize file pointer to use to output data gotten from input file
    FILE *output_file = NULL;

    char *filename = malloc(8 * sizeof(char));
    //char filename[8];

    /*Read 512 bytes from input_file and store on the buffer*/
    while (fread(buffer, sizeof(char), 512, input_file))
    {
        //check if bytes is start of a JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //write jpeg into file name in form 001.jpg, 002.jpg and so on
            sprintf(filename, "%03i.jpg", count_image);

            //open Out_file for writing
            output_file = fopen(filename, "w");

            //fwrite(buffer, sizeof(buffer), 1, output_file);
            //count number of image found
            count_image++;
        }
        //Check if output have been used for valid input
        if (output_file != NULL)
        {
            fwrite(buffer, sizeof(char), 512, output_file);
        }

    }
    free(filename);
    fclose(output_file);
    fclose(input_file);

    return 0;
}