class Category:
    def __init__(self, name):
        self.name = name.title()
        self.total = 0.0
        self.ledger = []

    def __repr__(self):
        s = f"{'*'*int(((30-len(self.name))/2))}{self.name}{'*'*int(((30-len(self.name))/2))}\n"
        for i in self.ledger:
            s += f"{i['description'][:23]}{' '*(30-len(i['description'][:23])-len(str('{:>7.2f}'.format(i['amount']))[:7]))}{str('{:>7.2f}'.format(i['amount']))[:7]}\n"

        s += f"Total: {self.get_balance()}"
        return s

    def deposit(self, amount, *args):
        description = args[0] if args else ''
        self.total += amount
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, *args):
        can_withdraw = self.check_funds(amount)

        description = args[0] if args else ''

        if can_withdraw:
            self.total -= amount
            self.ledger.append({"amount": -amount, "description": description})

        return can_withdraw

    def get_balance(self):
        return self.total

    def transfer(self, amount, instance):
        can_transfer = self.check_funds(amount)

        if can_transfer:
            self.withdraw(amount, f"Transfer to {instance.name}")
            instance.deposit(amount, f"Transfer from {self.name}")

        return can_transfer

    def check_funds(self, amount):
        if amount > self.total:
            return False

        return True


def create_spend_chart(categories):
    header = "Percentage spent by category\n"

    spent_amounts = []
    # Get total spent in each category
    for category in categories:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])
        spent_amounts.append(round(spent, 2))

        print(spent, spent_amounts)

    # Calculate percentage rounded down to the nearest 10
    total = round(sum(spent_amounts), 2)
    spent_percentage = list(map(lambda amount: int((((amount / total) * 10) // 1) * 10), spent_amounts))


    
    chart = ""
    for value in reversed(range(0, 101, 10)):
        chart += str(value).rjust(3) + '|'
        for percent in spent_percentage:
            if percent >= value:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"


    footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"

    max_len = 0
    for n in categories:
        if len(n.name) >= max_len:
            max_len = len(n.name)

    name_list = []
    for l in categories:
        if len(l.name) < max_len:
            name_list.append(f"{l.name}{' '*(max_len - len(l.name))}")
        else:
            name_list.append(l.name)

    new_line = '     '
    for i in range(max_len):
        for item in name_list:
            new_line = new_line + item[i] + '  '
        footer += f"{new_line}\n"
        new_line = '     '

    return (header + chart + footer).rstrip("\n")


