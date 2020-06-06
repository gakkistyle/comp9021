# COMP9021 Practice 5 - Solutions


'''
Prompts the user for a year or a year and a month, the year being no earlier than 1753,
and displays the calendar for the period requested in the style of the Unix cal command,
but starting the week on Monday (not Sunday)
'''


field_width = 22


def calendar():
    month_names = 'January', 'February', 'March', 'April','May', 'June', 'July', 'August',\
                                                      'September', 'October', 'November', 'December'
    month_lengths = 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31
    print('I will display a calendar, either for a year or for a month in a year.\n'
          'The earliest year should be 1753.\n'
          "For the month, input at least the first three letters of the month's name."
         )
    correct_input = False
    month = 0
    while not correct_input:
        date = input('Input year, or year and month, or month and year: ')
        date = date.split()
        if len(date) == 0 or len(date) > 2:
            continue
        if len(date) == 1:
            try:
                year = int(date[0])
                correct_input = True
            except ValueError:
                print('Incorrect input. ', end = '')
            else:
                if year < 1753 or year > 9999999999999999:
                    print('Incorrect input. ', end = '')
                    correct_input = False
        else:
            date_0 = date[0].title()
            date_1 = date[1].title()
            try:
                month = date_0
                year = int(date_1)
            except ValueError:
                try:
                    month = date_1
                    year = int(date_0)
                except ValueError:
                    print('Incorrect input. ', end = '')
                    continue
            if len(month) < 3:
                print('Incorrect input. ', end = '')
                continue
            for i in range(12):
                if month_names[i].startswith(month):
                    month = i
                    correct_input = True
                    break
    # Number of days between 1 January 2000 and the requested date,being 1 January
    # of the requested year if no month has been input, positive for a date
    # after 1 January 2000, negative for a date before 1 January 2000.
    # If a month of March or later has been input and the input year is a leap year before 2000,
    # then the assignment is incorrect by one day, which is fixed in the following if statement.
    offset = (year - 2000) * 365 +\
                                 (year - 1997) // 4 - (year - 1901) // 100 + (year - 1601) // 400 +\
                                                                         sum(month_lengths[: month])
    if month > 2 and (year % 4 == 0 and year % 100 or year % 400 == 0):
        offset += 1
    # 1 January 2000 is a Saturday
    starting_day = (offset + 5) % 7
    if len(date) == 2:
        date = month_names[month] + ' ' + str(year)
        print(date.center(field_width))
        nb_of_days = 29 if month == 1 and (year % 4 == 0 and year % 100 or year % 400 == 0) else\
                                                                                month_lengths[month]
        for line in month_representation_lines(starting_day, nb_of_days):
            print(line)
    else:
        print(str(year).center(field_width * 3) + '\n')
        if year % 4 == 0 and year % 100 or year % 400 == 0:
            month_lengths[1] += 1
        months = [[month.center(field_width)] for month in month_names]
        for i in range(12):
            months[i].extend(month_representation_lines(starting_day, month_lengths[i]))
            starting_day = (starting_day + month_lengths[i]) % 7
        groups_of_three_months = [months[3 * i: 3 * (i + 1)] for i in range(4)]
        for group_of_three_months in groups_of_three_months:
            for month in group_of_three_months:
                month.extend([' ' * field_width] *
                                                 (max(map(len, group_of_three_months)) - len(month))
                            )
                lines = map(''.join, zip(*group_of_three_months))
            for line in lines:
                print(line)

def month_representation_lines(starting_day, nb_of_days):
    lines = [' Mo Tu We Th Fr Sa Su ']
    line = ' ' * 3 * starting_day
    for i in range(1, nb_of_days + 1):
        line += f'{i:3d}'
        starting_day = (starting_day + 1) % 7
        if starting_day == 0:
            lines.append(line + ' ')
            line = ''
    if line != '':
        line += ' ' * 3 * (7 - starting_day)
        lines.append(line + ' ')
    return lines
    

if __name__ == '__main__':
    calendar()
