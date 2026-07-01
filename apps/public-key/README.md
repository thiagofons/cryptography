# Criptografia de Chave Pública

| Grupo algébrico escolhido |
| :--- |
| Grupo multiplicativo $(\mathbb{Z}/p\mathbb{Z})^*$ |

## Definição formal do grupo algébrico

O grupo multiplicativo dos inteiros módulo $p$, denotado formalmente por $(\mathbb{Z}/p\mathbb{Z})^*$ ou $\mathbb{Z}_p^*$, é o conjunto de todas as classes de equivalência dos inteiros de $1$ a $p-1$ que são coprimos com $p$. 

Para fins criptográficos e segurança computacional, adota-se um número $p$ que seja um **Primo de Safe** (Primo Seguro), definido pela relação:

$$p = 2q + 1$$

onde $q$ também é um número primo grande (conhecido como Primo de Sophie Germain). 

Sob essa configuração, a ordem do grupo é $\text{ord}((\mathbb{Z}/p\mathbb{Z})^*) = p - 1 = 2q$. Pelo Teorema de Lagrange, os únicos subgrupos possíveis dentro desta estrutura possuem ordens contidas no conjunto de divisores $\{1, 2, q, 2q\}$, blindando o sistema contra ataques de fatoração de subgrupos (como o algoritmo de Pohlig-Hellman).

## Descrição da operação

A operação interna que define a estrutura de grupo deste conjunto é a **Multiplicação Modular**. Dados dois elementos quaisquer $a, b \in (\mathbb{Z}/p\mathbb{Z})^*$, a operação é computada como:

$$a \cdot b \equiv (a \times b) \pmod p$$

A estrutura satisfaz rigorosamente as quatro propriedades fundamentais de um Grupo Abeliano:
1. **Fechamento:** O resultado de $(a \times b) \pmod p$ sempre pertence ao intervalo $[1, p-1]$.
2. **Associatividade:** $(a \cdot b) \cdot c \equiv a \cdot (b \cdot c) \pmod p$.
3. **Elemento Identidade:** O número $1$ atua como elemento neutro, onde $a \cdot 1 \equiv a \pmod p$.
4. **Elemento Inverso:** Para cada elemento $a$, existe um único inverso $a^{-1}$ tal que $a \cdot a^{-1} \equiv 1 \pmod p$, calculável computacionalmente através do Algoritmo Estendido de Euclides.
5. **Comutatividade:** $a \cdot b \equiv b \cdot a \pmod p$.

Computacionalmente, a operação estendida mais crítica para os protocolos Diffie-Hellman e ElGamal é a **Exponenciação Modular** ($g^x \pmod p$), executada de forma altamente eficiente através de algoritmos de multiplicação binária repetida (como o método *Square-and-Multiply*).

## Elemento gerador

Um elemento $g \in (\mathbb{Z}/p\mathbb{Z})^*$ é considerado um **gerador** (ou raiz primitiva módulo $p$) se a sua ordem for igual à ordem do grupo ($p-1$). Isso significa que o conjunto de suas potências sucessivas reconstrói todo o grupo criptográfico:

$$\langle g \rangle = \{g^1 \pmod p, g^2 \pmod p, \dots, g^{p-1} \pmod p\} = (\mathbb{Z}/p\mathbb{Z})^*$$

No código implementado, dado que $p = 2q + 1$, a validação matemática para assegurar que um número aleatório $g$ seja um gerador legítimo utiliza o Pequeno Teorema de Fermat, testando as ordens dos fatores primos de $p-1$:

```python
# Fermat's Little Theorem verification for primitive root
if pow(g, 2, p) != 1 and pow(g, q, p) != 1:
    return g  # g is a valid generator of the group