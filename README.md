# Sistema Bancário Orientado a Objetos (Sprint 6)

Projeto de desenvolvimento do Sistema Bancário em Python orientado a objetos, aplicando conceitos de **Abstração**, **Encapsulamento**, **Herança**, **Polimorfismo**, **Validação com `@property`** e **Métodos Especiais (Dunder Methods)**.

---

## 📐 Diagrama de Classes (Mermaid)

```mermaid
classDiagram
    class Endereco {
        +str logradouro
        +str numero
        +str cidade
        +str uf
        +__str__() str
    }

    class Cliente {
        -str _nome
        -str _cpf
        -str _email
        +Endereco endereco
        +nome str
        +cpf str
        +email str
    }

    class ContaBancaria {
        <<Abstract>>
        -str _numero_conta
        -Cliente _titular
        -float _saldo
        +numero_conta str
        +titular Cliente
        +saldo float
        +depositar(float valor)
        +sacar(float valor)* bool
        +__eq__(object) bool
        +__lt__(ContaBancaria) bool
    }

    class ContaCorrente {
        -float _limite_cheque_especial
        +float TAXA_SAQUE
        +sacar(float valor) bool
    }

    class ContaPoupanca {
        +float taxa_rendimento
        +sacar(float valor) bool
        +aplicar_rendimento()
    }

    Cliente "1" *-- "1" Endereco : Composição
    ContaBancaria "1" o-- "1" Cliente : Agregação/Composição
    ContaBancaria <|-- ContaCorrente : Herança ("É um")
    ContaBancaria <|-- ContaPoupanca : Herança ("É um")