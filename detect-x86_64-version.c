#include <stdio.h>
#include <unistd.h>

int main() {
    #if defined(__AVX512VL__)
    printf("4");
    return 0;
    #endif

    #if defined(__AVX2__)
    printf("3");
    return 0;
    #endif

    #if defined(__SSE4_2__) && defined(__POPCNT__)
    printf("2");
    return 0;
    #endif

    printf("1");
    return 0;
}
