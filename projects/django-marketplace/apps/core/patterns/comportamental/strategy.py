from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


# ==========================================
# ESTRATEGIA ABSTRACTA (Strategy Interface)
# ==========================================

class ProviderSelectionStrategy(ABC):
    """
    Interfaz abstracta para estrategias de selección de proveedor.
    Define el contrato que todas las estrategias concretas deben cumplir.
    """
    
    @abstractmethod
    def select_provider(
        self,
        order_data: Dict[str, Any],
        available_providers: List[str]
    ) -> str:
        pass
    
    def get_strategy_name(self) -> str:
        return self.__class__.__name__

# ==========================================
# ESTRATEGIAS CONCRETAS (Concrete Strategies)
# ==========================================

class StandardSelectionStrategy(ProviderSelectionStrategy):
    
    def select_provider(
        self,
        order_data: Dict[str, Any],
        available_providers: List[str]
    ) -> str:

        weight = order_data.get('weight', 0)
        fragility = order_data.get('fragility', 'ninguna')
        priority = order_data.get('priority', 'normal')
        
        # Regla 1: Frágil y no urgente → Cuidado ecológico
        if fragility != 'ninguna' and priority != 'urgente':
            if 'ecobike' in available_providers:
                return 'ecobike'
        
        # Regla 2: Peso alto → Capacidad tradicional
        if weight > 5000:  # > 5kg
            if 'paqz' in available_providers:
                return 'paqz'
        
        # Regla 3: Urgente → Velocidad
        if priority == 'urgente':
            if 'motoya' in available_providers:
                return 'motoya'
        
        # Regla 4: Default → MotoYA (balanceado)
        if 'motoya' in available_providers:
            return 'motoya'
        
        # Fallback: Primer proveedor disponible
        return available_providers[0] if available_providers else 'motoya'

class EcoFriendlySelectionStrategy(ProviderSelectionStrategy):
    
    def select_provider(
        self,
        order_data: Dict[str, Any],
        available_providers: List[str]
    ) -> str:

        weight = order_data.get('weight', 0)
        priority = order_data.get('priority', 'normal')
        
        # Prioridad 1: EcoBike siempre que sea posible
        if 'ecobike' in available_providers:
            # EcoBike tiene limitaciones físicas
            if weight <= 10000 and priority != 'urgente':  # <= 10kg y no urgente
                return 'ecobike'
        
        # Prioridad 2: MotoYA (menor huella que camiones)
        if 'motoya' in available_providers:
            return 'motoya'
        
        # Última opción: PaqueteríaZ
        if 'paqz' in available_providers:
            return 'paqz'
        
        # Fallback
        return available_providers[0] if available_providers else 'ecobike'

class CostOptimizedSelectionStrategy(ProviderSelectionStrategy):

    # Costos estimados por proveedor (simulados)
    COST_STRUCTURE = {
        'paqz': {'base': 50, 'per_kg': 10},      # Económico para peso
        'ecobike': {'base': 40, 'per_kg': 15},   # Tarifa plana baja
        'motoya': {'base': 80, 'per_kg': 20}     # Premium
    }
    
    def select_provider(
        self,
        order_data: Dict[str, Any],
        available_providers: List[str]
    ) -> str:
        """
        Selecciona proveedor minimizando costo estimado.
        """
        weight_kg = order_data.get('weight', 0) / 1000
        priority = order_data.get('priority', 'normal')
        
        # Si es urgente, solo MotoYA cumple (costo no importa)
        if priority == 'urgente':
            return 'motoya' if 'motoya' in available_providers else available_providers[0]
        
        # Calcular costo estimado para cada proveedor disponible
        costs = {}
        for provider in available_providers:
            if provider in self.COST_STRUCTURE:
                structure = self.COST_STRUCTURE[provider]
                estimated_cost = structure['base'] + (structure['per_kg'] * weight_kg)
                costs[provider] = estimated_cost
        
        # Seleccionar el más económico
        if costs:
            cheapest_provider = min(costs, key=costs.get)
            return cheapest_provider
        
        # Fallback: PaqueteríaZ (generalmente más económico)
        return 'paqz' if 'paqz' in available_providers else available_providers[0]

class WeightBasedSelectionStrategy(ProviderSelectionStrategy):
    
    def select_provider(
        self,
        order_data: Dict[str, Any],
        available_providers: List[str]
    ) -> str:
        """
        Selecciona proveedor basado exclusivamente en peso.
        """
        weight = order_data.get('weight', 0)
        
        if weight < 2000:  # < 2kg
            if 'ecobike' in available_providers:
                return 'ecobike'
        elif weight <= 8000:  # 2-8kg
            if 'motoya' in available_providers:
                return 'motoya'
        else:  # > 8kg
            if 'paqz' in available_providers:
                return 'paqz'
        
        # Fallback
        return available_providers[0] if available_providers else 'motoya'

# ==========================================
# CONTEXTO (Context)
# ==========================================

class ProviderSelector:
    
    def __init__(self, strategy: Optional[ProviderSelectionStrategy] = None):
        self._strategy = strategy or StandardSelectionStrategy()
    
    def set_strategy(self, strategy: ProviderSelectionStrategy) -> None:
        self._strategy = strategy
    
    def select_provider(
        self,
        order_data: Dict[str, Any],
        available_providers: List[str]
    ) -> str:
        return self._strategy.select_provider(order_data, available_providers)
    
    def get_current_strategy_name(self) -> str:
        return self._strategy.get_strategy_name()

# ==========================================
# UTILIDADES
# ==========================================

# Mapeo de nombres de estrategias a clases (facilita selección dinámica)
STRATEGY_REGISTRY = {
    'standard': StandardSelectionStrategy,
    'eco': EcoFriendlySelectionStrategy,
    'cost': CostOptimizedSelectionStrategy,
    'weight': WeightBasedSelectionStrategy
}


def get_strategy_by_name(name: str) -> ProviderSelectionStrategy:
    strategy_class = STRATEGY_REGISTRY.get(name.lower())
    if not strategy_class:
        available = ', '.join(STRATEGY_REGISTRY.keys())
        raise ValueError(f'Estrategia no válida: {name}. Disponibles: {available}')
    
    return strategy_class()
