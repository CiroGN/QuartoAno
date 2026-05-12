#include <iostream>
using namespace std;

int main() {
    int pulgas = 2;
    int dias = 1;
    int antipulgas = 1;
    while (pulgas > 0){
        if (dias % 3 == 0){
            pulgas -= 2; // pulgas = pulgas - 2;
        }
        cout << "Dia " << dias << ": " << pulgas << " pulgas, " << antipulgas << " antipulgas" << endl;
        pulgas += 6; // pulgas = pulgas + 6;
        pulgas -= antipulgas; // pulgas = pulgas - antipulgas;
        antipulgas = 4 * antipulgas;
        if (pulgas > 0){
            dias++;
        }
    }
    cout << "Dias levados:  "<< dias << endl;

    return 0;

}

