## Plot do Histograma de erros Original
import numpy as np
import matplotlib.pyplot as plt

# Função para ler os valores do arquivo txt
def read_values_from_file(file_path):
    with open(file_path, 'r') as file:
        values = [float(line.strip()) for line in file.readlines()]
    return values

# Intervalos desejados para o histograma
bin_edges = [-4.5,-3.9,-3.3,-2.7,-2.1 ,-1.5 ,-0.9, -0.3, 0.3, 0.9, 1.5, 2.1, 2.7, 3.3, 3.9, 4.5]

# Função para criar o histograma
def create_histogram(values, bin_edges):
    n, bins, patches = plt.hist(values, bins=bin_edges, color='skyblue', edgecolor='black', linewidth=1.2)
    
    # Adiciona rótulos personalizados ao eixo x
    bin_labels = []
    for i in range(len(bin_edges) - 1):
        bin_labels.append(f"{bin_edges[i]} - {bin_edges[i+1]}")
    
    plt.xticks([(bin_edges[i] + bin_edges[i+1]) / 2 for i in range(len(bin_edges) - 1)], bin_labels, rotation=45)

    # Adiciona anotações com os valores acima de cada bin
    for i in range(len(bins) - 1):
        plt.text((bins[i] + bins[i + 1]) / 2, n[i] + 0.1, int(n[i]), ha='center', fontsize=10)

    plt.xlabel('Intervalos')
    plt.ylabel('Frequência')
    plt.title('Histograma das diferenças entre as notas originais e as notas após a retirada do ruído')
    plt.tight_layout()
    plt.show()

file_path = 'diferenças.txt'

values = read_values_from_file(file_path)
# Cria e exibe o histograma
create_histogram(values, bin_edges)





## CRIAÇÃO DOS HISTOGRAMAS PARA OS DADOS COM RUÍDO


# Ler os dados dos arquivos txt
def read_data(filename):
    with open(filename, 'r') as f:
        data = [float(line.strip()) for line in f.readlines()]
    return data

files = ['test_stress/diferenças_100.txt', 'test_stress/diferenças_200.txt', 'test_stress/diferenças_500.txt', 'test_stress/diferenças_1000.txt', 'test_stress/original.txt']
labels = ['100 valores afetados', '200 valores afetados', '500 valores afetados', '1000 valores afetados', 'Original']
data = [read_data(file) for file in files]

# Definir bins
bin_edges = [-4.5, -3.9, -3.3, -2.7, -2.1, -1.5, -0.9, -0.3, 0.3, 0.9, 1.5, 2.1, 2.7, 3.3, 3.9, 4.5]

# Cores para os histogramas
colors = ['red', 'blue', 'green', 'orange', 'black']

# Calcular frequências para cada arquivo e bin
hist_data = [np.histogram(d, bins=bin_edges)[0] for d in data]

# Plotar os histogramas
plt.figure(figsize=(12, 6))
bar_width = 0.17
bar_positions = np.arange(len(bin_edges) - 1)

for i, hist in enumerate(hist_data):
    plt.bar(bar_positions + i * bar_width, hist, width=bar_width, color=colors[i], label=labels[i])

bin_labels = []
for i in range(len(bin_edges) - 1):
    bin_labels.append(f"{bin_edges[i]} - {bin_edges[i+1]}")
plt.xticks(bar_positions + bar_width * 1.5, bin_labels, rotation=45)

plt.xlabel('Diferenças')
plt.ylabel('Frequência')
plt.legend()
plt.title('Histogramas das Diferenças dos Algoritmos (Nota obtida - Nota original)')
plt.show()


