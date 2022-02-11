#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    // Get user cash amount
    float dollars;
    do
    {
        dollars = get_float("Enter dollar amount:\n");
    }
    while (dollars <= 0);
    
    // Convert to cents
    int cents = round(dollars * 100);
    
    // Use while loop to iterate through change
    int numCoins = 0;
    
    // Now calculate change
    while (cents >= 25)
    {
        cents -= 25;
        numCoins++;
    }
    while (cents >= 10)
    {
        cents -= 10;
        numCoins++;
    }
    while (cents >= 5)
    {
        cents -= 5;
        numCoins++;
    }
    while (cents >= 1)
    {
        cents -= 1;
        numCoins++;
    }
    
    // output entered cash amount
    printf("%i\n",numCoins);
}