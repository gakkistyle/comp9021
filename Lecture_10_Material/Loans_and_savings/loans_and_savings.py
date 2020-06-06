# COMP9021 Term 3 2019


'''
A class Savings and a class Loans that both derive from a class Account,
allowing one to set the values of at most N-1 parameters from a list of
N parameters, and in case the values of N-1 parameters are set,
computing the value of the missing one.
'''


from math import log10
from numbers import Real


class Account:
    INTEREST = 'interest'
    REFERENCE_PERIOD = 'reference_period'
    TERM_AMOUNT = 'term_amount'
    DURATION = 'duration'
    INITIAL_SUM = 'initial_sum'
    FINAL_SUM = 'final_sum'
    nb_in_year = {'year' : 1, 'semester' : 2, 'quarter' : 4, 'month' : 12} 
    # - interest and reference_period have to be provided and their
    #   values cannot be changed.
    # - term_amount and duration can be either provided or computed.
    # These parameters need to be complemented with:
    # - final_sum for savings (either provided or computed), useless for
    #   loans since it has to be 0 (loan fully repaid);
    # - initial_sum for loans (either provided or computed), useless for
    #   savings since it is the same as term_amount.
    def __init__(self, *, interest, reference_period, term_amount, duration):
        # We will remove INITIAL_SUM from _unknowns when dealing with an
        # object of class Savings, and remove FINAL_SUM from _unknowns
        # when dealing with an object of class Loan.
        self._unknowns = {Account.INITIAL_SUM, Account.TERM_AMOUNT,
                          Account.FINAL_SUM, Account.DURATION
                         }
        self.set_interest(interest)
        self.set_reference_period(reference_period)
        self.set_effective_interest()
        self.set_term_amount(term_amount)
        self.set_duration(duration)
                
    def check_and_set_parameter(self, parameter, parameter_name, valid_types,
                                sign
                               ):
        self.check_type(parameter, parameter_name, valid_types)
        self.set_parameter(parameter, parameter_name, sign)
        
    def check_type(self, parameter, parameter_name, valid_type):
        if not isinstance(parameter, valid_type):
            raise TypeError(f'{parameter_name} should be of type {valid_type}')

    def set_parameter(self, parameter, parameter_name, sign):
        if parameter * sign < 0:
            raise ValueError(f'{parameter_name} should be of opposite sign')
        if parameter:
            if parameter_name in self._unknowns:
                if len(self._unknowns) == 1:
                    raise NoUnknownException(f'{parameter_name} is the only '
                                             'unknown parameter'
                                            )
                self._unknowns.remove(parameter_name)
        else:
            self._unknowns.add(parameter_name)
        setattr(self, '_' + parameter_name, parameter)
                                                        
    def set_interest(self, interest):
        self.check_type(interest, Account.INTEREST, Real)
        if interest == 0:
            raise ValueError('Interest should not be 0')          
        if interest < 0:
            raise ValueError('Interest should not be negative')
        self._interest = interest

    def set_reference_period(self, reference_period):
        if reference_period not in Account.nb_in_year:
            raise ValueError('Reference period should be one of '
                             f'{list(Account.nb_in_year)}'
                            )
        self._reference_period = reference_period

    def set_effective_interest(self):
        self.effective_interest =\
              ((1 + self._interest / Account.nb_in_year[self._reference_period]
               ) ** Account.nb_in_year[self._reference_period] - 1
              )

    def set_term_amount(self, term_amount):
        # An amount added to Savings account, and deducted from a Loans
        # account.
        self.check_and_set_parameter(term_amount, Account.TERM_AMOUNT, Real,
                                     2 * isinstance(self, Savings) - 1
                                    )

    def set_duration(self, duration):
        self.check_and_set_parameter(duration, Account.DURATION, int, 1)
        
    @property
    def interest(self):
        return self._interest

    @property
    def reference_period(self):
        return self._reference_period

    @property
    def term_amount(self):
        return self._term_amount

    @term_amount.setter
    def term_amount(self, term_amount):
        self.set_term_amount(term_amount)
        self.update()

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        self.set_duration(duration)
        self.update()

    def update(self):
        # solve() is specific to and defined in the subclasses Savings
        # and Loan.
        all_known = self.solve()
        print(f'Annual interest:\t {float(self.interest * 100):.2f}%')
        print('Reference period:\t', self.reference_period)
        if isinstance(self, Loan):
            if all_known or Account.INITIAL_SUM not in self._unknowns:
                print(f'Sum borrowed:\t\t {float(self.initial_sum):.2f}')
            else:
                print('Sum borrowed:\t\t Unknown')
        if all_known or Account.TERM_AMOUNT not in self._unknowns:
            if isinstance(self, Savings):
                print(f'Yearly deposits:\t {float(self.term_amount):.2f}')
            else:
                print(f'Monthly repayments:\t {float(self.term_amount):.2f}')
        else:
            if isinstance(self, Savings):
                print('Yearly deposits:\t Unknown')
            else:
                print('Monthly repayments:\t Unknown')
        if isinstance(self, Savings):
            if all_known or Account.FINAL_SUM not in self._unknowns:       
                print(f'Available sum:\t\t {float(self.final_sum):.2f}')
            else:
                print('Available sum:\t\t Unknown')
        if all_known or Account.DURATION not in self._unknowns:
            print('Duration (in years):\t', round(self.duration))
        else:
            print('Duration (in years):\t Unknown')
        print()


class Savings(Account):
    # term_amount is a yearly deposit
    def __init__(self, *, interest, reference_period='year', term_amount=0,
                 duration=0, final_sum=0
                ):
        super().__init__(interest=interest, reference_period=reference_period,
                         term_amount=term_amount, duration=duration
                        )
        self._unknowns.remove(Account.INITIAL_SUM)
        self.set_final_sum(final_sum)
        self.update()

    def set_final_sum(self, final_sum):
        self.check_and_set_parameter(final_sum, Account.FINAL_SUM, Real, 1)

    @property
    def final_sum(self):
        return self._final_sum

    @final_sum.setter
    def final_sum(self, final_sum):
        self.set_final_sum(final_sum)
        self.update()

    def solve(self):
        if len(self._unknowns) != 1:
            return False
        if Account.FINAL_SUM in self._unknowns:
            self._final_sum = self.term_amount / self.effective_interest\
                              * ((1 + self.effective_interest)
                                 ** (self.duration + 1) - 1
                                 - self.effective_interest
                                )
        elif Account.TERM_AMOUNT in self._unknowns:
            self._term_amount = self.final_sum * self.effective_interest\
                                / ((1 + self.effective_interest)
                                   ** (self.duration + 1) - 1
                                   - self.effective_interest
                                  )
        else:
            self._duration = log10(self.final_sum * self.effective_interest
                                   / self.term_amount
                                   + (1 + self.effective_interest)
                                  ) / log10(1 + self.effective_interest) - 1
        return True


class Loan(Account):
    # term_amount is a monthly repayment
    def __init__(self, *, interest, reference_period='year', term_amount=0,
                 duration=0, initial_sum=0
                ):
        super().__init__(interest=interest, reference_period=reference_period,
                         term_amount=term_amount, duration=duration
                        )
        self._unknowns.remove(Account.FINAL_SUM)
        self.set_initial_sum(initial_sum)
        self.update()

    def set_initial_sum(self, initial_sum):
        self.check_and_set_parameter(initial_sum, Account.INITIAL_SUM, Real, 1)

    @property
    def initial_sum(self):
        return self._initial_sum

    @initial_sum.setter
    def initial_sum(self, initial_sum):
        self.set_initial_sum(initial_sum)
        self.update()

    def solve(self):
        if len(self._unknowns) != 1:
            return False
        monthly_interest = (1 + self.effective_interest) ** (1 / 12) - 1
        if Account.INITIAL_SUM in self._unknowns:
            self._initial_sum = -self.term_amount\
                                * ((1 + monthly_interest)
                                   ** (12 * self.duration) - 1
                                  ) / monthly_interest\
                                  / (1 + monthly_interest)\
                                    ** (12 * self.duration)
        elif Account.TERM_AMOUNT in self._unknowns:
            self._term_amount = -self.initial_sum * (1 + monthly_interest)\
                                                    ** (12 * self.duration)\
                                * monthly_interest\
                                / ((1 + monthly_interest)
                                   ** (12 * self.duration) - 1
                                  )
        else:
            self._duration = log10(self.term_amount / (monthly_interest
                                                       * self.initial_sum
                                                       + self.term_amount
                                                      )
                                  ) / (12 * log10(1 + monthly_interest))
        return True


class NoUnknownException(Exception):
    pass


if __name__ == '__main__':
    print('TESTING SAVINGS\n')
    savings = Savings(term_amount=1000, interest=0.08, duration=25)
    savings.term_amount = 0
    savings.final_sum = 78954.42
    savings.duration = 0
    savings.term_amount = 1000.00
    print('\nTESTING LOANS\n')
    loan = Loan(initial_sum=100000, interest=0.08, duration=20,
                reference_period='month'
               )
    loan.initial_sum = 0
    loan.term_amount = -836.44
    loan.duration = 0
    loan.initial_sum = 100000.0
