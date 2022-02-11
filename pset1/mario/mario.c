#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get height
    int n;
    do
    {
        n = get_int("Enter height:\n");
    }
    while (n < 1 || n > 8);
    
    // Create blocks
    for (int row = 0; row < n; row++)
    {
        for (int l_space = n - row - 1; l_space > 0; l_space--)
        {
            printf(" ");
        }
        for (int l_hash = 0; l_hash < row + 1; l_hash++)
        {
            printf("#");
        }
        printf("  ");
        for (int r_hash = 0; r_hash < row + 1;r_hash++)
        {
            printf("#");
        }
        printf("\n");
    }
    
}