"""Data models.

TODO: refactor into full service classes"""

from dataclasses import dataclass, field

@dataclass
class Ingredient(object):
    """Represents an ingredient in a list"""
    name: str
    quantity: float
    unit: str

    # TODO: unit conversions on adding two of the same ingredient together

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __mul__(self, scalar: float):
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Ingredient(name=self.name, 
                          quantity=self.quantity*scalar,
                          unit=self.unit)

    def __rmul__(self, scalar: float):
        return self.__mul__(scalar)

@dataclass
class Recipe(object):
    """Represents recipe requirements and metadata"""
    name: str
    ingredients: list[Ingredient]
    portions: int
    cartegory: str = ''
    tags: list[str] = field(default_factory=list)

    def __str__(self):
        selfstr = f"{self.name} ({self.portions} portions)\n"
        for i in self.ingredients:
            selfstr += f"    " + str(i) + "\n"
        return selfstr


@dataclass
class Pantry(object):
    """Represents pantry inventory.
    ### TODO:
     - Add history tree tracking for undos"""
    ingredients: list[Ingredient]

@dataclass
class ShoppingList(object):
    """Represents contents of a shopping list"""
    ingredients: list[Ingredient]

    
"""
    def subtract_pantry(self, pantry: Pantry) -> None:
        \"""
        Subtracts pantry from current ingredient list.
        
        :param pantry: Pantry to subtract
        \"""
        pass
    
    def export_list(self, pantry: Pantry) -> None:
        \"""
        Returns shopping list as a csv file.
        TODO: accept specified output format from range of options
        \"""
        self.subtract_pantry(pantry=pantry)
        pass
"""