# Projeto de Criptossistema Simétrico: Lince-ARX

Este projeto apresenta o desenvolvimento e a análise do **Lince-ARX**, um criptossistema simétrico original projetado especificamente para aliar alta eficiência computacional a uma implementação simples e segura. O algoritmo adota a filosofia **ARX (Addition-Rotation-XOR)**, eliminando a necessidade de tabelas de substituição (S-Boxes) complexas e operações pesadas em Corpos de Galois.

---

## Estrutura do algoritmo

O Lince-ARX é uma cifra de bloco iterativa que opera sobre blocos de **128 bits** utilizando chaves de **128 bits** ao longo de **16 rounds** (rodadas). 

A segurança e a propriedade de confusão do algoritmo baseiam-se na **não-linearidade mista**, gerada pela combinação de operações de grupos algébricos distintos que não são distributivas entre si:
1. **Adição Modular ($\mathbf{A}$):** Adição de inteiros de 32 bits sem sinal com estouro natural ($\pmod{2^{32}}$). Introduz a não-linearidade através da propagação dos bits de transporte (*carry bits*).
2. **Rotação de Bits ($\mathbf{R}$):** Deslocamento circular de bits para a esquerda ($\lll$), garantindo a difusão rápida de modificações por toda a palavra.
3. **XOR ($\mathbf{X}$):** Disjunção exclusiva bit a bit, fornecendo uma operação linear complementar de mistura.

O bloco de 128 bits de entrada é dividido nativamente em 4 palavras de 32 bits, representadas como um vetor de estado:
$$S = (A, B, C, D) \quad \text{onde } A, B, C, D \in \mathbb{Z}_{2^{32}}$$

---

## Geração de subchaves

Para garantir máxima eficiência e reaproveitamento de código, o *Key Schedule* do Lince-ARX utiliza uma variação simplificada da própria função de round sobre a chave mestre de 128 bits, combinada com constantes de rodada pseudoaleatórias ($C_i$) derivadas da parte fracionária de $\pi$ para evitar chaves fracas.

Dada a chave mestre $K = (K_0, K_1, K_2, K_3)$, a subchave do round $i$ ($RK_i$), para $i = 0, 1, \dots, 15$, é gerada da seguinte forma:

$$K_0^{(i)} = (K_0 + C_i) \oplus K_3$$
$$K_1^{(i)} = (K_1 \lll 9) + K_0^{(i)}$$
$$K_2^{(i)} = K_2 \oplus (K_1^{(i)} \lll 13)$$
$$K_3^{(i)} = (K_3 + K_2^{(i)}) \lll 15$$

A subchave final para o round $i$ é extraída como:
$$RK_i = K_0^{(i)} \oplus K_2^{(i)}$$

Após cada extração, o vetor de chaves sofre uma rotação cíclica de palavras: $(K_0, K_1, K_2, K_3) \leftarrow (K_1, K_2, K_3, K_0)$ para o próximo cálculo.

---

## Operação de cifração

A cifração toma o bloco de texto claro $S^{(0)} = (A_0, B_0, C_0, D_0)$ e o submete a 16 iterações da função de transformação ARX. Para cada round $i$ (de 0 a 15), utilizando a subchave $RK_i$:

$$A_{i+1} = (A_i + B_i) \oplus RK_i$$
$$B_{i+1} = (B_i \lll 7) \oplus A_{i+1}$$
$$C_{i+1} = (C_i + D_i) \oplus B_{i+1}$$
$$D_{i+1} = (D_i \lll 13) \oplus C_{i+1}$$

No encerramento de cada round, as palavras sofrem uma permutação de posição (Word Shuffle) para garantir que todas as partes do bloco se influenciem mutuamente no round subsequente:
$$(A_{i+1}, B_{i+1}, C_{i+1}, D_{i+1}) \leftarrow (D_{i+1}, A_{i+1}, B_{i+1}, C_{i+1})$$

O texto cifrado é o estado final $S^{(16)} = (A_{16}, B_{16}, C_{16}, D_{16})$.

---

## Operação de decifração

Como a estrutura ARX proposta não se baseia estritamente em uma rede Feistel pura (onde a mesma função é usada invertendo as chaves), as operações matemáticas individuais devem ser invertidas na ordem exata oposta (de 15 até 0).

Antes de processar cada round inverso $i$, desfaz-se o Word Shuffle:
$$(D_{i+1}, A_{i+1}, B_{i+1}, C_{i+1}) \leftarrow (A_{i+1}, B_{i+1}, C_{i+1}, D_{i+1})$$

Em seguida, aplicam-se as operações inversas (subtração modular $\pmod{2^{32}}$ e rotação para a direita $\ggg$):

$$C_i = (D_{i+1} \oplus C_{i+1}) \ggg 13$$
$$C_i = C_i - D_i \pmod{2^{32}}$$
$$B_i = (B_{i+1} \oplus A_{i+1}) \ggg 7$$
$$A_i = (A_{i+1} \oplus RK_i) - B_i \pmod{2^{32}}$$

Este fluxo reverte perfeitamente o estado até recuperar o texto claro original $S^{(0)}$.

---

## Análise de desempenho

* **Velocidade de Execução:** Por operar nativamente com inteiros de 32 bits (`uint32_t`), o Lince-ARX consome pouquíssimos ciclos de clock por byte cifrado. Ele se beneficia diretamente das instruções de hardware de soma e rotação da CPU, superando implementações puramente em software do AES (sem aceleração AES-NI).
* **Consumo de Memória:** O consumo de RAM é praticamente **zero (0 bytes de overhead)**. Ao contrário do AES, que exige tabelas de busca pré-computadas (como as T-Tables ou S-Boxes de 256 bytes), o Lince-ARX mantém seu estado inteiramente dentro dos registradores internos do processador.
* **Paralelização:** Em modos de operação de bloco paralelos (como CTR), múltiplos blocos podem ser processados simultaneamente. Dentro de um único bloco, os pares $(A, B)$ e $(C, D)$ possuem dependências parciais que permitem pequena otimização de pipeline em compiladores modernos.

---

## Análise de segurança

* **Confusão e Difusão:** A difusão completa (onde a alteração de 1 bit no texto claro altera em média 50% dos bits do texto cifrado) é atingida após apenas **4 rounds**, devido às rotações ímpares ($\lll 7$ e $\lll 13$) combinadas com o efeito cascata do *carry* da adição modular.
* **Resistência a Ataques de Canal Lateral (Side-Channel):** O uso exclusivo de operações de tempo constante (Add, XOR, Rot) imuniza o Lince-ARX contra ataques de análise de tempo por cache (*Cache-timing attacks*), uma vulnerabilidade histórica comum em implementações de software do AES com tabelas de busca.
* **Criptoanálise Linear e Diferencial:** A alternância constante entre a álgebra XOR ($\mathbb{F}_2^{32}$) e a álgebra de adição ($\mathbb{Z}_{2^{32}}$) quebra as aproximações lineares e diferenciais, blindando o sistema contra ataques tradicionais para o número proposto de 16 rounds.

---

## Comparação com o AES

| Característica | AES-128 | Lince-ARX (Proposto) |
| :--- | :--- | :--- |
| **Tamanho de Chave** | 128 bits | 128 bits |
| **Tamanho de Bloco** | 128 bits | 128 bits |
| **Operações Primitivas** | Substituição (S-Box), Permutação de Linhas, MixColumns (GF($2^8$)) | Adição $\pmod{2^{32}}$, Rotação, XOR |
| **Simplicidade de Código** | Baixa a Média (Exige aritmética em Corpos Finitos e matrizes) | **Alta** (Apenas operadores lógicos e aritméticos padrão) |
| **Pegada de Memória** | Média (Exige tabelas de 256 bytes a múltiplos KB) | **Mínima** (Zero tabelas, ideal para sistemas embarcados/IoT) |
| **Imunidade a Cache-Timing** | Crítica (Exige extremo cuidado na implementação de software) | **Nativa** (Todas as operações executam em tempo constante) |
| **Velocidade (Software Puro)** | Moderada | **Altíssima** |
| **Velocidade (Hardware)** | Máxima (Via instruções dedicadas Intel AES-NI / ARM Crypto) | Moderada a Alta (Depende da eficiência de pipeline de arquitetura de uso geral) |
| **Escalabilidade** | Complexa (Mudar tamanho de bloco quebra a estrutura de matriz e S-Boxes) | **Fácil** (Escala nativamente mudando o tipo para palavras de 64 bits/bloco de 256 bits) |