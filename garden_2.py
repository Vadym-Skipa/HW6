from abc import ABC, abstractmethod
import random


class GardenMetaClass(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class PlantsGetter:

    def __init__(self, plants):
        self.plants = plants

    def get_plant(self, type_of_plant_food="", variety_of_plant_food=""):
        list_of_plants = self.plants
        if type_of_plant_food:
            list_of_plants = list(filter(lambda plant: plant.type_of_plant_food == type_of_plant_food, list_of_plants))
        if variety_of_plant_food:
            list_of_plants = list(filter(lambda plant: plant.variety == variety_of_plant_food, list_of_plants))
        return list_of_plants


class Garden(PlantsGetter, metaclass=GardenMetaClass):
    def __init__(self, plants, pests, gardener):
        PlantsGetter.__init__(self, plants)
        self.pests = pests
        self.gardener = gardener

    def show_the_garden(self):
        print(f'The garden has such plants: {self.plants}')
        print(f'And such pests: {self.pests}')
        print(f'The maintainer of the garden is {self.gardener}')


class PlantFood(ABC):
    _id = 0
    STATES = ()

    def __init__(self, type_of_plant_food, state=0):
        self._type_of_plant_food = type_of_plant_food
        self._state = state
        self._index = self.__class__._id
        self.__class__._id += 1

    @property
    def state(self):
        return self.STATES[self._state]

    @property
    def type_of_plant_food(self):
        return self._type_of_plant_food

    @property
    def index(self):
        return self._index

    @abstractmethod
    def grow(self):
        raise NotImplementedError('Your method is not implemented.')

    @abstractmethod
    def is_ripe(self):
        raise NotImplementedError('Your method is not implemented.')


class Plant(ABC):

    def __init__(self, type_of_plant_food):
        self._type_of_plant_food = type_of_plant_food

    @property
    def type_of_plant_food(self):
        return self._type_of_plant_food

    @abstractmethod
    def grow_all(self):
        raise NotImplementedError('Your method is not implemented.')

    @abstractmethod
    def all_are_ripe(self):
        raise NotImplementedError('Your method is not implemented.')

    @abstractmethod
    def provide_harvest(self):
        raise NotImplementedError('Your method is not implemented.')

    @abstractmethod
    def variety(self):
        raise NotImplementedError('Your method is not implemented.')

    @abstractmethod
    def plant_foods(self):
        raise NotImplementedError('Your method is not implemented.')


class Tomato(PlantFood):
    STATES = ('nothing', 'flowering', 'green', 'red')

    def __init__(self, variety_of_tomato, state=0):
        super(Tomato, self).__init__("vegetable", state)
        self._variety_of_tomato = variety_of_tomato

    @property
    def variety(self):
        return self._variety_of_tomato

    def _change_state(self):
        if self._state < 3:
            self._state += 1
        print(self)

    def grow(self):
        self._change_state()

    def __str__(self):
        return f"{self.variety} tomato N{self.index} is {self.state}"

    def is_ripe(self):
        return self._state == 3


class TomatoBush(Plant):

    def __init__(self, number_of_tomatoes=0, variety_of_tomatoes='Simple', list_of_tomatoes=()):
        super(TomatoBush, self).__init__("vegetable")
        if number_of_tomatoes:
            self._list_of_tomatoes = [Tomato(variety_of_tomatoes) for _ in range(number_of_tomatoes)]
        else:
            self._list_of_tomatoes = list_of_tomatoes
        self._variety_of_tomatoes = variety_of_tomatoes

    def grow_all(self):
        for tomato in self._list_of_tomatoes:
            tomato.grow()

    def all_are_ripe(self):
        return all(tomato.is_ripe() for tomato in self._list_of_tomatoes)

    def provide_harvest(self):
        temp_tomatoes = tuple(filter(lambda tomato: tomato.is_ripe(), self._list_of_tomatoes))
        for tomato in temp_tomatoes:
            self._list_of_tomatoes.remove(tomato)
        if not self._list_of_tomatoes:
            del self
        return temp_tomatoes

    @property
    def variety(self):
        return self._variety_of_tomatoes

    @property
    def plant_foods(self):
        return self._list_of_tomatoes


class Apple(PlantFood):
    STATES = ('nothing', 'flowering', 'green', 'half-red', 'red')

    def __init__(self, variety_of_apple, state=0):
        super(Apple, self).__init__("fruit", state)
        self._variety_of_apple = variety_of_apple

    @property
    def variety(self):
        return self._variety_of_apple

    def _change_state(self):
        if self._state < 4:
            self._state += 1
        print(self)

    def grow(self):
        self._change_state()

    def __str__(self):
        return f"{self.variety} apple N{self.index} is {self.state}"

    def is_ripe(self):
        return self._state == 4


class AppleTree(Plant):

    def __init__(self, number_of_apples=0, variety_of_apples='Simple', list_of_apples=()):
        super(AppleTree, self).__init__("fruit")
        if number_of_apples:
            self._list_of_apples = [Apple(variety_of_apples) for _ in range(number_of_apples)]
        else:
            self._list_of_apples = list_of_apples
        self._variety_of_apples = variety_of_apples

    def grow_all(self):
        for apple in self._list_of_apples:
            apple.grow()

    def all_are_ripe(self):
        return all(apple.is_ripe() for apple in self._list_of_apples)

    def provide_harvest(self):
        temp_apples = tuple(filter(lambda apple: apple.is_ripe(), self._list_of_apples))
        for apple in temp_apples:
            self._list_of_apples.remove(apple)
        return temp_apples

    @property
    def variety(self):
        return self._variety_of_apples

    @property
    def plant_foods(self):
        return self._list_of_apples


class StarGardener(PlantsGetter):
    def __init__(self, name, plants):
        self.name = name
        PlantsGetter.__init__(self, plants)

    def harvest(self):
        print('Gardener is harvesting...')
        for plant in self.plants:
            if plant.all_are_ripe():
                plant.provide_harvest()
                print('Harvesting is finished.')
            else:
                print('Too early! Your plants is not ripe.')

    def handling(self):
        print('Gardner is working...')
        for plant in self.plants:
            plant.grow_all()
        print('Gardner is finished')

    def poison_pests(self):
        Garden().pests.quantity //= 2

    def check_states(self):
        for plant in self.plants:
            for plantfood in plant.plant_foods:
                if plantfood.state == 3:
                    return True
                return False


class Pests:

    def __init__(self, pests_type, quantity, type_of_plant_food="", variety_of_plant_food=""):
        self._pests_type = pests_type
        self.quantity = quantity
        self._type_of_plant_food = type_of_plant_food
        self._variety_of_plant_food = variety_of_plant_food

    @property
    def pests_type(self):
        return self._pests_type

    def eat(self):
        list_of_plant = Garden().get_plant(self._type_of_plant_food, self._variety_of_plant_food)
        for _ in range(self.quantity):
            if list_of_plant:
                temp = random.choice(list_of_plant)
                temp.plant_foods.remove(random.choice(temp.plant_foods))
            else:
                print("everything is already eaten")
                break


if __name__ == '__main__':
    # Creating list of instances for vegetables and fruits, pests and gardener
    tomato_bush = TomatoBush(4, "Red")
    apple_tree = AppleTree(3, "Golden")
    pests = Pests('worm', 5, "vegetable")
    tom = StarGardener('Tom', [tomato_bush, apple_tree])
    # creating only one garden instance with vegetables and fruits
    garden = Garden([tomato_bush, apple_tree], pests=pests, gardener=tom)
    garden.show_the_garden()
    state = tom.check_states()
    tom.poison_pests()
    pests.eat()
    # if not state:
    #     gardener.handling()
    for i in range(3):
        tom.handling()
    tom.harvest()
