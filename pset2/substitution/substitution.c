#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

bool uniqueLetters(string letters);
void cipher(string key);

int main(int argc, string argv[])
{
    // Validate key
    // Check if there are two argc
    if (argc == 2)
    {
        // Check if the second argv is 26 characters long and if characters are alpha
        if (strlen(argv[1]) == 26)
        {
            for (int i = 0; i < strlen(argv[1]) ; i++)
            {
                if (! isalpha(argv[1][i]))
                {
                    printf("Key must contain 26 alphabetic characters.\n");
                    return 1;
                }
            if (! uniqueLetters(argv[1]))
            {
                printf("Key must not contain repeated alphabetic characters.\n");
                return 1;
            }
            }
        cipher(argv[1]);
        }
        else
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }
    }
    else
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    return 0;
}

void cipher(string key)
{
    string abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    // Get and print out inputted text
    string plainText = get_string("plaintext: ");
    printf("ciphertext: ");

    //Check to see if plain text is alpha or not
    for (int i = 0; i < strlen(plainText); i ++)
    {
        if (isalpha(plainText[i]))
        {
            if (islower(plainText[i]))
            {
                char letterLower = plainText[i];
                for (int j = 0; j < strlen(abc); j++)
                {
                    if (tolower(abc[j]) == letterLower)
                    {
                    printf("%c", tolower(key[j]));
                    break;
                    }
                }
            }
            else
            {
                char letterUpper = plainText[i];
                for (int j = 0; j < strlen(abc); j++)
                {
                    if (toupper(abc[j]) == letterUpper)
                    {
                    printf("%c", toupper(key[j]));
                    break;
                    }
                }
            }
        }
        else
        {
            // Keep non-alpha in order
            printf("%c",plainText[i]);
        }
    }
    printf("\n");
}

bool uniqueLetters(string letters)
{
    for (int i = 0; i < strlen(letters); i++)
    {
        for (int j = i + 1; j < strlen(letters); j++)
        {
            if (toupper(letters[i]) == toupper(letters[j]))
            {
                return false;
            }
        }
    }
    return true;
}