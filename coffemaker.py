import json

class Drink:
    """
    drink class which provides the information of name and the ingredients used to prepare it.
    """
    def __init__(self, name, ingredients) -> None:
        """
        drink object will accept name and ingredients as a dict object
        """
        self.drink_name = name
        self.ingredients = ingredients
    
    def set_ingredients(self, new_ingredients):
        """
        method to update the ingredients for a drink
        """
        self.ingredients = new_ingredients
    
    def get_ingredients(self):
        """
        method to return the igredients and their quantities
        """
        return self.ingredients
    
    def get_drink_name(self):
        """
        method to return the drink name
        """
        return self.drink_name


class Inventory:
    """
    inventory class which provides and tracks the information related to ingredients and their quantities
    """
    def __init__(self, items_quatity: dict) -> None:
        self.items = items_quatity
    

    def get_ingredient(self, ingredient_name):
        return self.items.get(ingredient_name, None)


    def get_ingredient_quantity(self):
        """
        to return the igredients and their quantities
        """
        return self.items


    def update_ingredient(self, ingredient_name, ingredient_quantity):
        """
        method to update inventory for each order
        """
        if self.items.get(ingredient_name, 'None') is not 'None':
            self.items[ingredient_name] -= ingredient_quantity

    def add_new_ingredient(self, new_ingredient: str, new_ingredient_quantity: int):
        """
        method to add new ingredients to the available list, //for future requirements
        """
        # check if ingredient being added is already present
        if self.items.get(new_ingredient, 'new') is 'new' and new_ingredient_quantity > 0:
            self.items[new_ingredient] = int(new_ingredient_quantity)
        else:
            print('Cannot add new ingredient')


    def refill_ingredient(self, ingredient_name, ingredient_quantity):
        """
        method to refill a particular ingredient
        """
        try:
            if int(ingredient_quantity) > 0 :
                if self.items.get(ingredient_name, 'None') is not 'None':
                    self.items[ingredient_name] += int(ingredient_quantity)
                    print('updated {} quantity to: {}'.format(ingredient_name, ingredient_quantity))
                else:
                    print('No such ingredient available to refill, use add ingredient')
            else:
                print('Please add ingredients in positive values')
        except Exception as e:
            print('Exception occurred when refilling the ingredients for {}'.format(ingredient_name))
            print('Error Message: {}'.format(e))


class Coffee_machine():
    """
    coffee machine class which contains the core logic to prepare drinks
    """
    def __init__(self, outlets, inventory) -> None:
        self.outlets = outlets
        self.inventory = inventory
        self.menu = {}


    def get_menu(self):
        """
        method to print the menu
        """
        print('Menu:')
        print('\n'.join(self.menu.keys()))
    

    def display_ingredient_quantity(self):
        print(self.inventory.get_ingredient_quantity())

    
    def add_drink(self, drink: Drink):
        """
        add a drink to the menu
        """
        self.menu[drink.get_drink_name()] = drink
        print('Added drink {} to the menu'.format(drink.get_drink_name()))
    

    def get_drink(self, drink_name):
        """
        get the drink object
        """
        return self.menu.get(drink_name)
    

    def check_drink(self, drink_name):
        """
        method to check if a drink is being served
        """
        if self.menu.get(drink_name, 'Not there') is 'Not there':
            return False
        else:
            return True
    

    def check_availability(self, drink_name):
        try:
            if self.check_drink(drink_name):
                drink = self.get_drink(drink_name)
                drink_ingredients = drink.get_ingredients()

                # check if each ingredient is available in inventory
                for ingredient, value in drink_ingredients.items():
                    if self.inventory.get_ingredient(ingredient) is None:
                        return "{} cannot be prepared because {} is not available".format(drink_name, ingredient)
                    else:
                        if value <= self.inventory.get_ingredient(ingredient):
                            pass
                        else:
                            return "{} cannot be prepared because {} is not available".format(drink_name, ingredient)
                
                return "available"
            else:
                 return "{} cannot be prepared because it is not available in menu".format(drink_name)
        except Exception as e:
            print('Error: {}'.format(e))
            return "{} cannot be prepared because of exception".format(drink_name)
    

    def prepare_drink(self, drink_name):
        """
        method to prepare a drink
        """
        drink = self.get_drink(drink_name)
        drink_ingredients = drink.get_ingredients()
        
        for ingredient, value in drink_ingredients.items():
            self.inventory.update_ingredient(ingredient, value)
        return "{} is prepared".format(drink_name)


    def order(self, drinks):
        """
        method to prepare a drink
        """
        if len(drinks) > self.outlets:
            print('Can prepare only {} drinks at a time'.format(self.outlets))

        output = []

        for drink_name in drinks[:self.outlets]:
            drink_status = self.check_availability(drink_name)
            
            if drink_status is not "available":
                output.append(drink_status)
            else:
                output.append(self.prepare_drink(drink_name))
        
        return '\n'.join(output)


def main():
    """
    main method with all functional test cases
    """
    with open('input.json') as f:
        input_data = json.load(f)
    
    data = input_data.get('machine')
    
    # create inventory and coffee machine objects
    inventory = Inventory(data.get('total_items_quantity'))
    coffee_machine = Coffee_machine(data['outlets']['count_n'], inventory)

    # create drink objects and add them to coffee machine
    for name, ingredients in data['beverages'].items():
        coffee_machine.add_drink(Drink(name, ingredients))

    print("\n")
    print(coffee_machine.display_ingredient_quantity())

    print("\n")
    print(coffee_machine.get_menu())

    print("\nOdering hot_tea, hot_coffee and black_tea -")
    print(coffee_machine.order(['hot_tea', 'hot_coffee', 'black_tea']))

    print("\n")
    print(coffee_machine.display_ingredient_quantity())

    print('Adding ingredients')
    inventory.refill_ingredient('hot_water', 1000)
    inventory.refill_ingredient('ginger_syrup', 100)
    inventory.refill_ingredient('hot_milk', 1000)
    inventory.refill_ingredient('sugar_syrup', 700)
    inventory.refill_ingredient('tea_leaves_syrup', 300)

    print("\nOdering hot_tea, hot_coffee and green_tea -")
    print(coffee_machine.order(['hot_tea', 'hot_coffee', 'black_tea']))

    print("\n")
    print(coffee_machine.display_ingredient_quantity())

    print("\nOdering green_tea, hot_coffee and black_tea -")
    print(coffee_machine.order(['hot_tea', 'hot_coffee', 'black_tea']))

    print("\n")
    print(coffee_machine.display_ingredient_quantity())

if __name__ == '__main__':
    main()