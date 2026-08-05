#include <iostream>
#include <vector>
#include <random>
#include <cmath>

using namespace std;

// Tamanho fixo para o teste (pode mudar para até 100)
const int N = 65536;
const unsigned int SEMENTE = 1000;
const int bandas = 3;

// --- FUNÇÕES DE ÁLGEBRA LINEAR TRADICIONAL ---

// Produto escalar entre dois vetores (u . v)
double produto_escalar(const vector<double>& u, const vector<double>& v) {
    double resultado = 0.0;
    for (int i = 0; i < N; ++i) {
        resultado += u[i] * v[i];
    }
    return resultado;
}

// Calcula a norma L2 (magnitude do erro)
double calcular_norma(const vector<double>& v) {
    return sqrt(produto_escalar(v, v));
}

// Produto Matriz-Vetor Padrão (Sem otimização, varre a matriz inteira)
vector<double> produto_matriz_vetor(const vector<vector<double>>& A, const vector<double>& x) {
    vector<double> resultado(N, 0.0);
    
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            resultado[i] += A[i][j] * x[j];
        }
    }
    return resultado;
}

int main() {
    // --- 1. CONSTRUÇÃO DA MATRIZ CHEIA (N x N) ---
    cout << "Criando matriz quadrada " << N << "x" << N << "..." << endl;
    
    mt19937 gerador(SEMENTE);
    uniform_real_distribution<double> distribuicao(0.1, 1.0);

    // Inicializa uma matriz cheia de zeros
    vector<vector<double>> Matriz_A(N, vector<double>(N, 0.0));

    // Preenche as diagonais (simulando o espalhamento do problema anterior)
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            int deslocamento = j - i;
            
            // Se o deslocamento estiver dentro do raio de 13 posições, coloca o valor
            if (deslocamento >= (bandas * -1) && deslocamento <= bandas) {
                Matriz_A[i][j] = distribuicao(gerador);
            }
            
            // Força a diagonal principal (onde i == j) a ser dominante para convergir
            if (i == j) {
                Matriz_A[i][j] += 30.0;
            }
        }
    }

    // Vetores do sistema Ax = b
    vector<double> vetor_b(N, 1.0);  // Termo independente
    vector<double> vetor_x(N, 0.0);  // Resposta inicial (chute)

    // --- 2. EXECUÇÃO DO GRADIENTE CONJUGADO ---
    cout << "Calculando o Gradiente Conjugado..." << endl;

    int contador_passos = 0;
    int max_iteracoes = 10000;
    double tolerancia = 1e-6;

    // r = b - A*x
    vector<double> Ax = produto_matriz_vetor(Matriz_A, vetor_x);
    vector<double> r(N);
    for (int i = 0; i < N; ++i) r[i] = vetor_b[i] - Ax[i];
    
    vector<double> p = r;

    while (calcular_norma(r) > tolerancia && contador_passos < max_iteracoes) {
        contador_passos++;

        // Ap = A * p
        vector<double> Ap = produto_matriz_vetor(Matriz_A, p);
        
        double r_quadrado_antigo = produto_escalar(r, r);
        double alpha = r_quadrado_antigo / produto_escalar(p, Ap);

        for (int i = 0; i < N; ++i) {
            vetor_x[i] += alpha * p[i];
            r[i] -= alpha * Ap[i];
        }

        double r_quadrado_novo = produto_escalar(r, r);
        double beta = r_quadrado_novo / r_quadrado_antigo;

        for (int i = 0; i < N; ++i) {
            p[i] = r[i] + beta * p[i];
        }
    }

    // --- 3. EXIBIÇÃO COMPLETA DOS DADOS ---
    cout << "\n==========================================" << endl;
    cout << "Execucao concluida!" << endl;
    cout << "Passos necessarios: " << contador_passos << endl;
    cout << "Norma final do erro: " << calcular_norma(r) << endl;
    //cout << "==========================================" << endl;

   // Imprime a Matriz Inteira
   //cout << "\n--- MATRIZ COMPLETA (A) ---" << endl;
   // for (int i = 0; i < N; ++i) {
   //     cout << "[ ";
   //     for (int j = 0; j < N; ++j) {
   //         cout << Matriz_A[i][j] << " ";
   //     }
   //     cout << "]" << endl;
   //}

    // Imprime o Vetor b
    cout << "\n--- VETOR DE ENTRADA (b) ---" << endl;
    for (int i = 0; i < N; ++i) {
        cout << "b[" << i << "] = " << vetor_b[i] << endl;
    }

    // Imprime o Vetor x
    cout << "\n--- VETOR DE RESULTADO (x) ---" << endl;
    for (int i = 0; i < N; ++i) {
        cout << "x[" << i << "] = " << vetor_x[i] << endl;
    }
    cout << "==========================================" << endl;

    return 0;
}
