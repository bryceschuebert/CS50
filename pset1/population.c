#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int start_n;
    do
    {
        start_n = get_int("Enter starting population size greater than 9:\n");
    }
    while (start_n < 9);
    // TODO: Prompt for end size
    int end_n;
    do
    {
        end_n = get_int("Enter ending population size:\n");
    }
    while (end_n < start_n);
    // TODO: Calculate number of years until we reach threshold
    int n = 0;

    while (start_n < end_n)
    {
        start_n = start_n + (start_n/3) - (start_n/4);
        n++;
    }
    // TODO: Print number of years
    printf("Years: %i", n);
}