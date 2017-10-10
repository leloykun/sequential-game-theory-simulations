#include <iostream>
#include <cmath>
#include <algorithm>

#define MAX_N 4 // adjust this value as needed
struct AugmentedMatrix { double mat[MAX_N][MAX_N + 1]; };
struct ColumnVector { double vec[MAX_N]; };

const double e = exp(1);

ColumnVector GaussianElimination(int N, AugmentedMatrix Aug) { // O(N^3)
    // input: N, Augmented Matrix Aug, output: Column vector X, the answer
    int i, j, k, l; double t; ColumnVector X;

    for (j = 0; j < N - 1; j++) { // the forward elimination phase
        l = j;
        for (i = j + 1; i < N; i++) // which row has largest column value
            if (fabs(Aug.mat[i][j]) > fabs(Aug.mat[l][j]))
                l = i; // remember this row l
    // swap this pivot row, reason: to minimize floating point error
    for (k = j; k <= N; k++) // t is a temporary double variable
        t = Aug.mat[j][k], Aug.mat[j][k] = Aug.mat[l][k], Aug.mat[l][k] = t;
    for (i = j + 1; i < N; i++) // the actual forward elimination phase
        for (k = N; k >= j; k--)
            Aug.mat[i][k] -= Aug.mat[j][k] * Aug.mat[i][j] / Aug.mat[j][j];
    }
    for (j = N - 1; j >= 0; j--) { // the back substitution phase
        for (t = 0.0, k = j + 1; k < N; k++) t += Aug.mat[j][k] * X.vec[k];
        X.vec[j] = (Aug.mat[j][N] - t) / Aug.mat[j][j]; // the answer is here
    }
    return X;
}

int main() {
    AugmentedMatrix ag;
    double mat[][5] = {{e, 1, 1, 1, 1230},
              {1, e, 1, 1, 1012},
              {1, 1, e, 1, 952},
              {1, 1, 1, e, 1478}};
    for (int i = 0; i < 4; ++i)
        for (int j = 0; j < 4 + 1; ++j)
            ag.mat[i][j] = mat[i][j];
    
    ColumnVector res = GaussianElimination(4, ag);
    for (int i = 0; i < 4; ++i)
        std::cout<<res.vec[i]<<" ";
    
    std::cout<<res.vec[0]*exp(100) + res.vec[1]*exp(1) + res.vec[2]*exp(0.5) + res.vec[3]*exp(0.5)<<"\n";
    
    return 0;
}
