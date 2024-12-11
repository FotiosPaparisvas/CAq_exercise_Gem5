#include <stdio.h>

int main(int argc, char* argv[]) {

    int n = 45; // Predefined number of terms
    int t1 = 0, t2 = 1, nextTerm = 0;

    for (int i = 2; i < n; ++i) {
        nextTerm = t1 + t2;
        t1 = t2;
        t2 = nextTerm;
    }

    // The last Fibonacci number is now in `nextTerm'
    printf("\n%d\n", nextTerm);


    return 0;
}
