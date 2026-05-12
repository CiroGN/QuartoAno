#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "Digite o tamanho do vetor: ";
    cin >> n;
    bool swapped;

    int vetor[n]; // vetor []

    for (int i = 0; i < n; i++) {
        cout << "Digite o elemento " << i << ": ";
        cin >> vetor[i];
    }
    cout << "Vetor original: ";
    for (int i = 0; i < n; i++) {
        cout << vetor[i] << " ";
    }
    cout << endl;

    // Ordenar o vetor (método da bolha)
    for (int i = 0; i < n - 1; i++) {
        swapped = false;
        for (int j = 0; j < n - i - 1; j++) {
            if (vetor[j] > vetor[j + 1]) {
                int temp = vetor[j];
                vetor[j] = vetor[j + 1];
                vetor[j + 1] = temp;
                swapped = true;
            }
            cout << "Passo " << i + 1 << ", comparação " << j + 1 << ": ";
            for (int k = 0; k < n; k++) {
                cout << vetor[k] << " ";
            }
            cout << endl;
        }
        if (!swapped) {
            break;
        }
    }
    cout << "Vetor ordenado: ";
    for (int i = 0; i < n; i++) {
        cout << vetor[i] << " ";
    }
    cout << endl;
    return 0;
}