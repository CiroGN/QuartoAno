#include <iostream>
using namespace std;

int main(){
    int n, s;  
    cout << "Digite o numero de pedras: ";
    cin >> n;
    cout << "Digite o numero de sapos: ";
    cin >> s;
    int pedras[n];
    int sapo[s];
    bool pulou = false;
    
    for(int i = 0; i < s; i++){
        int posicao;
        cout << "Esolha a posicao do sapo " << i + 1 << " qual pedra esta: ";
        cin >> posicao;
        cout << "Quantos metros o sapo " << i + 1 << " pode pular: ";
        cin >> sapo[i];
        pedras[posicao - 1] = i + 1;
    }
    for(int i = 0; i < n; i++){
        if (pedras[i] <= 0 and pedras[i] > s){
            pedras[i] = 0;
        }
        cout << "Pedra " << i + 1 << ": " << pedras[i] << " ";
    }
    for(int i = 0; i < s; i++){
        cout << "Sapo " << i + 1 << ": " << sapo[i] << " ";
    }
    cout << endl;

    for(int i = 0; i < n; i++){
        if (pedras[i] > 0 and pedras[i] <= s){
            cout << "Sapo " << pedras[i] << " esta na pedra " << i + 1 << endl;
            cout << "O sapo " << pedras[i] << " pode pular " << sapo[pedras[i] - 1] << " metros" << endl;
            cout << "Para qual direção o sapo irá pular? (1 para direita, 2 para esquerda): ";
            int direcao;
            cin >> direcao;
            if (direcao == 1){
                if(pedras[i] != 0){
                    int j = sapo[pedras[i] - 1];
                    if(i + j < n){
                        pedras[i+j] = pedras[i];
                        pedras[i] = 0;
                    } else {
                        cout << "O sapo " << pedras[i] << " nao pulou pois ultrapassaria o limite!" << endl;}
                }
            } else if (direcao == 2){    
                if(pedras[i] != 0){
                    int j = sapo[pedras[i] - 1];
                    if(i - j >= 0){
                        pedras[i-j] = pedras[i];
                        pedras[i] = 0;
                    } else {
                        cout << "O sapo " << pedras[i] << " nao pulou pois ultrapassaria o limite!" << endl;}
                }
            } else {
                cout << "Direção inválida!" << endl;
            }
        } else {
            cout << "Não há sapo na pedra " << i + 1 << endl;
        }
    }
    for (int i = 0; i < n; i++){
        cout << "Pedra " << i + 1 << ": " << pedras[i] << endl;
    }
}