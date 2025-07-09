# Compilador C

Este projeto implementa um compilador de códigos em **C**. O objetivo é proporcionar uma implementação modular e extensível, dividida em diferentes estágios, como o **analisador léxico**, **analisador sintático** e **gerador de código**.

## Estrutura
- **`scanner/`**: Contém o analisador léxico (scanner) e a configuração de calibração (regex) para a tokenização do código-fonte.
	-  **`scanner.py`**: Implementação do analisador léxico.
	-  **`calibration.py`**: Contém as definições de regex específicas para possíveis linguagens do analisador léxico (palavras-chave, operadores, etc.).
- **`main.py`**: Ponto de entrada para executar o compilador.

## Analisador Léxico
O **analisador léxico** (ou scanner) é responsável por dividir o código-fonte em **tokens**. O projeto foi implementado de forma que o analisador léxico seja **expansível** e **genérico**, permitindo a fácil adição de novas linguagens ou tipos de tokens, apesar de a princípio o obejtivo ser apenas um compilador de códigos em C.

### Como funciona:
-   O analisador léxico usa **expressões regulares (regex)** para identificar padrões no código.
-   As definições de regex para os tokens são definidas no arquivo **`calibration.py`**.
### Exemplo de calibração:
```
KEYWORDS = {'int', 'return', 'if', 'else', 'while', 'for', 'break', 'continue', 'char', 'float', 'double', 'void', 'struct', 'typedef', 'const', 'static'}
COMMENT   = r'//.*|/\*[\s\S]*?\*/'
STRING    = r'"(\\.|[^"\\])*"'
CHAR      = r"'(\\.|[^'\\])'"
NUMBER    = r'\d+(\.\d+)?[fF]?'
ID        = r'[A-Za-z_][A-Za-z0-9_]*'
OP        = r'==|!=|<=|>=|&&|\|\||[-+*/%=<>&|^!~]'
SYMBOL    = r'[{}\[\]();,]'
NEWLINE   = r'\n'
SKIP      = r'[ \t]+'
MISMATCH  = r'.'
```
## Analisador Estático

## Analisador Semântico

## Gerador de código
## Execução
1. **Clonar o repositório**

2. **Instalar Dependências**
	Nenhuma dependência no momento

3. **Executar**
	Basta executar o arquivo `main.py`
	```
	python main.py
	```

## Exemplo de uso (Analisador Léxico)
### Entrada
```c
int main() {
    int x = 5;
    return x;
}
```
### Saída
```vbnet
type: KEYWORD   | value: 'int'
type: ID        | value: 'main'
type: SYMBOL    | value: '('
type: SYMBOL    | value: ')'
type: SYMBOL    | value: '{'
type: KEYWORD   | value: 'int'
type: ID        | value: 'x'
type: OP        | value: '='
type: NUMBER    | value: '5'
type: SYMBOL    | value: ';'
type: KEYWORD   | value: 'return'
type: ID        | value: 'x'
type: SYMBOL    | value: ';'
type: SYMBOL    | value: '}'

```
