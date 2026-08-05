# include <iostream>
using namespace std;

string nomeGuerreiro(string guerreiros[], int i){
    return guerreiros[i];
}
void nomeMaiorValor(string guerreiros[], int percentualKi[]) {
    int maiorValor = 0;
    string nome;
    for (int i = 0; i < 8 - 1; i++) {
        if (maiorValor < percentualKi[i]) {
            maiorValor = percentualKi[i];
            nome = nomeGuerreiro(guerreiros, i);
        }
    }
    cout << "O maior percentual de aumento de ki é do " << nome << ": " << maiorValor << "%" << endl;
}

void mediaKi(string guerreiros[], int kiVelho[], int kiNovo[]) {
    string nomesAcimaMedia[8];
    int somaValores = 0;
    for (int i = 0; i < 8; i++) {
        somaValores += kiNovo[i];
    }
    double media = somaValores / 8.0;
    cout << "A média de ki dos guerreiros é: " << media << endl;
    for (int i = 0; i < 8; i++) {
        if (kiNovo[i] > media) {
            cout << "O ki de " << nomeGuerreiro(guerreiros, i) << " é: " << kiNovo[i] << endl;
            nomesAcimaMedia[i] = nomeGuerreiro(guerreiros, i);
        }
    }
}
void lutadorFraco(string guerreiros[], int kiNovo[]) {
    string nomeLutadorFraco;
    int menorValor = kiNovo[0];
    for (int i = 1; i < 8; i++) {
        if (menorValor > kiNovo[i]) {
            menorValor = kiNovo[i];
            nomeLutadorFraco = nomeGuerreiro(guerreiros, i);
        }
    }
    cout << "O lutador mais fraco é o " << nomeLutadorFraco << " com um ki de: " << menorValor << endl;
}

int main() {
    string guerreiros[8];
    int kiAntigo[8], kiNovo[8], percentualKi[8];
    
    guerreiros[0] = "Goku";
    guerreiros[1] = "Kuririn";
    guerreiros[2] = "Piccolo";
    guerreiros[3] = "Gohan";
    guerreiros[4] = "Tenshunhan";
    guerreiros[5] = "Chaos";
    guerreiros[6] = "Yamvha";
    guerreiros[7] = "Yajirobe";
    
    kiAntigo[0] = 924;
    kiAntigo[1] = 206;
    kiAntigo[2] = 408;
    kiAntigo[3] = 101;
    kiAntigo[4] = 250;
    kiAntigo[5] = 145;
    kiAntigo[6] = 177;
    kiAntigo[7] = 4;
    
    kiNovo[0] = 10000;
    kiNovo[1] = 1750;
    kiNovo[2] = 3500;
    kiNovo[3] = 981;
    kiNovo[4] = 1830;
    kiNovo[5] = 610;
    kiNovo[6] = 1480;
    kiNovo[7] = 4;
    
    percentualKi[0] = ((kiNovo[0] - kiAntigo[0]) * 100) / kiAntigo[0];
    percentualKi[1] = ((kiNovo[1] - kiAntigo[1]) * 100) / kiAntigo[1];
    percentualKi[2] = ((kiNovo[2] - kiAntigo[2]) * 100) / kiAntigo[2];
    percentualKi[3] = ((kiNovo[3] - kiAntigo[3]) * 100) / kiAntigo[3];
    percentualKi[4] = ((kiNovo[4] - kiAntigo[4]) * 100) / kiAntigo[4];
    percentualKi[5] = ((kiNovo[5] - kiAntigo[5]) * 100) / kiAntigo[5];
    percentualKi[6] = ((kiNovo[6] - kiAntigo[6]) * 100) / kiAntigo[6];
    percentualKi[7] = ((kiNovo[7] - kiAntigo[7]) * 100) / kiAntigo[7];
    
    nomeMaiorValor(guerreiros, percentualKi);
    mediaKi(guerreiros, kiAntigo, kiNovo);
    lutadorFraco(guerreiros, kiNovo);

    return 0;
    
}
