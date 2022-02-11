#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

// prototypes here
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");
    // printf("%i letters\n%i words\n%i sentences\n", count_letters(text), count_words(text), count_sentences(text));
    // Calculate Coleman-Liau index
    float L = ((float) count_letters(text) / count_words(text)) * 100;
    float S = ((float) count_sentences(text) / count_words(text)) * 100;
    float index = (0.0588 * L) - (0.296 * S) - 15.8;
    int roundedIndex = round(index);
    // If statement to pick correct grade
    if (roundedIndex > 1 && roundedIndex < 16)
    {
        printf("Grade %i\n", roundedIndex);
    }
    else if (roundedIndex < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade 16+\n");
    }
}

int count_letters(string text)
{
    int numLetters = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isupper(text[i]))
        {
            numLetters++;
        }
        else if (islower(text[i]))
        {
            numLetters++;
        }
    }
    return numLetters;
}

int count_words(string text)
{
    int numWords = 1;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == ' ')
        {
            numWords++;
        }
    }
    return numWords;
}

int count_sentences(string text)
{
    int numSentences = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            numSentences++;
        }
    }
    return numSentences;
}