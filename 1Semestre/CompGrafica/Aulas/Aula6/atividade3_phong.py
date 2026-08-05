import numpy as np
import matplotlib.pyplot as plt

angulos = np.linspace(0, 90, 500)
radianos = np.radians(angulos)

shininess_values = [2, 16, 64, 256]
cores = ['#185FA5', '#1D9E75', '#BA7517', '#D85A30']
estilos = ['-', '--', '-.', ':']
rotulos = ['α = 2 (fosco)', 'α = 16', 'α = 64', 'α = 256 (polido)']

fig, ax = plt.subplots(figsize=(9, 5))

for alpha, cor, estilo, rotulo in zip(shininess_values, cores, estilos, rotulos):
    intensidade = np.cos(radianos) ** alpha
    ax.plot(angulos, intensidade, color=cor, linestyle=estilo, linewidth=2, label=rotulo)

angulos_dest = [10, 30, 60]
for a in angulos_dest:
    ax.axvline(x=a, color='gray', linewidth=0.7, linestyle='--', alpha=0.4)
    ax.text(a + 0.8, 0.97, f'{a}°', fontsize=9, color='gray', va='top')

ax.set_xlabel('Ângulo entre R e V (graus)', fontsize=12)
ax.set_ylabel('Intensidade especular  I_s = cos(θ)^α', fontsize=12)
ax.set_title('Modelo de Phong — Intensidade especular por shininess', fontsize=13, fontweight='bold')
ax.set_xlim(0, 90)
ax.set_ylim(0, 1.02)
ax.set_xticks(range(0, 91, 10))
ax.legend(fontsize=11, loc='upper right')
ax.grid(True, linestyle='--', alpha=0.3)

fig.tight_layout()
plt.savefig('QuartoAno\\1Semestre\\CompGrafica\\Aulas\\Aula6\\atividade3_phong.png', dpi=150, bbox_inches='tight')
plt.show()

print("Observações:")
for alpha, rotulo in zip(shininess_values, rotulos):
    for grau in [10, 30, 60]:
        val = np.cos(np.radians(grau)) ** alpha
        print(f"  {rotulo:20s} | θ={grau:2d}°  →  I_s = {val:.4f}")
    print()
