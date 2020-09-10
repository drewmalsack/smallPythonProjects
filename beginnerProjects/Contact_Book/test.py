import re
if __name__ == '__main__':
    #pattern = re.compile(r'[a-z]+,\s[0-9a-z]+,\s^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', re.IGNORECASE)
    pattern = re.compile(r'[a-z]+[,]\s[0-9a-z]+[,]\s[a-z0-9]+[@][a-z]+[.][a-z]+', re.IGNORECASE)
    print(re.search(pattern, "Andrew, 262, drewmalsack@gmail.com"))
