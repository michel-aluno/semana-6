"""
Entregável de Desenvolvimento em Python - Semana 06 (Sprint 6)
Sistema Bancário Orientado a Objetos (POO) com Abstração, Encapsulamento,
Herança, Polimorfismo, Métodos Especiais e Validações.
"""

from abc import ABC, abstractmethod
from typing import List


# =============================================================================
# 1. CLASSE AUXILIAR (COMPOSIÇÃO: Cliente "tem um" Endereco)
# =============================================================================
class Endereco:
    """Representa o endereço físico de um cliente."""

    def __init__(self, logradouro: str, numero: str, cidade: str, uf: str):
        self.logradouro = logradouro
        self.numero = numero
        self.cidade = cidade
        self.uf = uf

    def __str__(self) -> str:
        return f"{self.logradouro}, {self.numero} - {self.cidade}/{self.uf}"

    def __repr__(self) -> str:
        return f"Endereco(logradouro='{self.logradouro}', numero='{self.numero}')"


class Cliente:
    """Representa o titular de uma conta bancária."""

    def __init__(self, nome: str, cpf: str, email: str, endereco: Endereco):
        self._nome = nome
        self._cpf = cpf
        self.email = email  # Usa o setter com validação @property
        self.endereco = endereco

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def cpf(self) -> str:
        return self._cpf

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        if "@" not in valor or "." not in valor:
            raise ValueError(f"Formato de e-mail inválido: '{valor}'")
        self._email = valor

    def __str__(self) -> str:
        return f"{self.nome} (CPF: {self.cpf}) - {self.email}"

    def __repr__(self) -> str:
        return f"Cliente(nome='{self.nome}', cpf='{self.cpf}')"


# =============================================================================
# 2. CLASSE ABSTRATA (CONTRATO BASE)
# =============================================================================
class ContaBancaria(ABC):
    """Classe abstrata mãe para todas as contas do sistema."""

    def __init__(self, numero_conta: str, titular: Cliente, saldo_inicial: float = 0.0):
        self._numero_conta = numero_conta
        self._titular = titular
        self._saldo = 0.0
        self.saldo = saldo_inicial  # Usa a property para validar no construtor

    @property
    def numero_conta(self) -> str:
        return self._numero_conta

    @property
    def titular(self) -> Cliente:
        return self._titular

    @property
    def saldo(self) -> float:
        return self._saldo

    @saldo.setter
    def saldo(self, valor: float) -> None:
        if valor < 0:
            raise ValueError("O saldo de uma conta não pode ser negativo.")
        self._saldo = valor

    def depositar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("O valor de depósito deve ser estritamente positivo.")
        self._saldo += valor
        print(f"Depósito de R$ {valor:.2f} realizado na conta {self.numero_conta}.")

    # Método Abstrato obriga as filhas a implementarem regras próprias de saque (Polimorfismo)
    @abstractmethod
    def sacar(self, valor: float) -> bool:
        """Realiza a tentativa de saque aplicando taxas/regras específicas."""
        pass

    # Dunder Methods para representação e ordenação/comparação
    def __str__(self) -> str:
        return f"Conta {self.numero_conta} | Titular: {self.titular.nome} | Saldo: R$ {self.saldo:.2f}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(numero='{self.numero_conta}', saldo={self.saldo})"

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, ContaBancaria):
            return False
        return self.numero_conta == outro.numero_conta

    def __lt__(self, outro: "ContaBancaria") -> bool:
        return self.saldo < outro.saldo


# =============================================================================
# 3. CLASSES FILHAS (HERANÇA E POLIMORFISMO)
# =============================================================================
class ContaCorrente(ContaBancaria):
    """Conta corrente com limite de cheque especial e taxa de operação."""

    TAXA_SAQUE = 2.50

    def __init__(
        self,
        numero_conta: str,
        titular: Cliente,
        saldo_inicial: float = 0.0,
        limite_cheque_especial: float = 500.0,
    ):
        super().__init__(numero_conta, titular, saldo_inicial)
        self.limite_cheque_especial = limite_cheque_especial

    @property
    def limite_cheque_especial(self) -> float:
        return self._limite_cheque_especial

    @limite_cheque_especial.setter
    def limite_cheque_especial(self, valor: float) -> None:
        if valor < 0:
            raise ValueError("O limite do cheque especial não pode ser negativo.")
        self._limite_cheque_especial = valor

    # Sobrescrita de Método (Polimorfismo)
    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            raise ValueError("O valor de saque deve ser maior que zero.")

        valor_total = valor + self.TAXA_SAQUE
        saldo_disponivel = self.saldo + self.limite_cheque_especial

        if valor_total > saldo_disponivel:
            raise ValueError(
                f"Saldo insuficiente na Conta Corrente {self.numero_conta}. "
                f"Disponível com limite: R$ {saldo_disponivel:.2f} | Solicitado (+ taxa R$ {self.TAXA_SAQUE:.2f}): R$ {valor_total:.2f}"
            )

        self._saldo -= valor_total
        print(f"Saque de R$ {valor:.2f} (Taxa R$ {self.TAXA_SAQUE:.2f}) efetuado na CC {self.numero_conta}.")
        return True


class ContaPoupanca(ContaBancaria):
    """Conta poupança sem taxa de saque, porém limitada ao saldo real e com rendimento."""

    def __init__(
        self,
        numero_conta: str,
        titular: Cliente,
        saldo_inicial: float = 0.0,
        taxa_rendimento: float = 0.005,
    ):
        super().__init__(numero_conta, titular, saldo_inicial)
        self.taxa_rendimento = taxa_rendimento

    # Sobrescrita de Método (Polimorfismo)
    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            raise ValueError("O valor de saque deve ser maior que zero.")

        if valor > self.saldo:
            raise ValueError(
                f"Saldo insuficiente na Conta Poupança {self.numero_conta}. "
                f"Saldo atual: R$ {self.saldo:.2f} | Solicitado: R$ {valor:.2f}"
            )

        self._saldo -= valor
        print(f"Saque de R$ {valor:.2f} efetuado na CP {self.numero_conta}.")
        return True

    def aplicar_rendimento(self) -> None:
        """Aplica a taxa de rendimento mensal ao saldo atual."""
        rendimento = self.saldo * self.taxa_rendimento
        self._saldo += rendimento
        print(f"Rendimento de R$ {rendimento:.2f} aplicado na CP {self.numero_conta}.")


# =============================================================================
# 4. TESTES E DEMONSTRAÇÃO DO SISTEMA
# =============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("      DEMONSTRAÇÃO DO SISTEMA BANCÁRIO ORIENTADO A OBJETOS      ")
    print("=" * 70)

    # Criando Endereços
    end1 = Endereco("Rua das Flores", "123", "São Paulo", "SP")
    end2 = Endereco("Av. Brasil", "456", "Rio de Janeiro", "RJ")

    # Criando Clientes (Pelo menos 4 instâncias)
    c1 = Cliente("Ana Silva", "111.222.333-44", "ana@email.com", end1)
    c2 = Cliente("Bruno Costa", "222.333.444-55", "bruno@email.com", end2)
    c3 = Cliente("Carla Souza", "333.444.555-66", "carla@email.com", end1)
    c4 = Cliente("Daniel Oliveira", "444.555.666-77", "daniel@email.com", end2)

    # Instanciando Objetos de Contas (Mais de 10 objetos criados no total)
    cc1 = ContaCorrente("CC-101", c1, saldo_inicial=1000.0, limite_cheque_especial=500.0)
    cc2 = ContaCorrente("CC-102", c2, saldo_inicial=2500.0, limite_cheque_especial=1000.0)
    cp1 = ContaPoupanca("CP-201", c3, saldo_inicial=500.0)
    cp2 = ContaPoupanca("CP-202", c4, saldo_inicial=3000.0)

    lista_contas: List[ContaBancaria] = [cc1, cc2, cp1, cp2]

    # 1. Demonstração de Polimorfismo (Iterando sobre instâncias de classes filhas distintas)
    print("\n--- 1. DEMONSTRAÇÃO DE POLIMORFISMO (Operações de Saque em Massa) ---")
    valor_saque_padrao = 300.0
    for conta in lista_contas:
        try:
            print(f"\nTentando sacar R$ {valor_saque_padrao:.2f} de: {conta}")
            conta.sacar(valor_saque_padrao)
            print(f"-> Saldo final: R$ {conta.saldo:.2f}")
        except ValueError as e:
            print(f"-> FALHA NO SAQUE: {e}")

    # 2. Teste de Tratamento de Exceções e Validações com @property
    print("\n--- 2. TESTANDO REGRAS DE NEGÓCIO E VALIDAÇÕES DE ERRO ---")

    # Tentativa 1: E-mail inválido no setter do Cliente
    try:
        print("\n[Teste] Alterando e-mail do cliente para formato inválido...")
        c1.email = "email_sem_arroba.com"
    except ValueError as e:
        print(f"✓ Exceção Capturada com Sucesso: {e}")

    # Tentativa 2: Saldo inicial negativo
    try:
        print("\n[Teste] Criando conta com saldo inicial negativo...")
        ContaCorrente("CC-ERRADA", c1, saldo_inicial=-100.0)
    except ValueError as e:
        print(f"✓ Exceção Capturada com Sucesso: {e}")

    # Tentativa 3: Saque além do limite permitido na Conta Corrente
    try:
        print("\n[Teste] Saque excessivo na Conta Corrente (excedendo limite de cheque especial)...")
        cc1.sacar(5000.0)
    except ValueError as e:
        print(f"✓ Exceção Capturada com Sucesso: {e}")

    # 3. Uso de Métodos Especiais (Dunder) e Ordenação por Saldo
    print("\n--- 3. MÉTODOS ESPECIAIS E ORDENAÇÃO DE OBJETOS (__lt__ e __eq__) ---")

    print("\nLista de contas desordenada:")
    for c in lista_contas:
        print(f"  • {c}")

    # A ordenação utiliza nativamente o método dunder __lt__ implementado na classe mãe
    lista_contas.sort()

    print("\nLista de contas ORDENADA POR SALDO (Crescente via __lt__):")
    for c in lista_contas:
        print(f"  • {c}")

    print("\nTestando igualdade de contas (__eq__):")
    cc_duplicada = ContaCorrente("CC-101", c1, saldo_inicial=0.0)
    print(f"CC-101 é igual a CC-101 duplicada? {cc1 == cc_duplicada}")
    print(f"CC-101 é igual a CC-102? {cc1 == cc2}")

    print("\n" + "=" * 70)
    print("                     FIM DA DEMONSTRAÇÃO                        ")
    print("=" * 70)