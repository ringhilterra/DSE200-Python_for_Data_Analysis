#!/usr/bin/env python

### ADD ARGPARSE to the main.
def findPayment(loan, r, m):
    """
    Calculate the monthly payment for a morgage

    Assumes: loan and r are floats, m an int
    Returns the monthly payment for a mortgage of size
    loan at a monthly rate of r for m months

    :param loan: Size of Loan.
    :param r: interest rate
    :param m: length of loan in months
    :returns: the monthly payment
    :rtype: float

    """
    return loan*((r*(1+r)**m)/((1+r)**m - 1))
    
class Mortgage(object):
    """Abstract class for building different kinds of mortgages"""
    def __init__(self, loan, annRate, months):
        """Create a new mortgage"""
        self.loan = loan
        self.rate = annRate/12.0
        self.months = months
        self.paid = [0.0]
        self.owed = [loan]
        self.payment = findPayment(loan, self.rate, months)
        self.legend = None #description of mortgage
    def makePayment(self):
        """Make a payment"""
        self.paid.append(self.payment)
        reduction = self.payment - self.owed[-1]*self.rate
        self.owed.append(self.owed[-1] - reduction)
    def getTotalPaid(self):
        """Return the total amount paid so far"""
        return sum(self.paid)
    def __str__(self):
        return self.legend

#Page 110, Figure 8.9
class Fixed(Mortgage):
    def __init__(self, loan, r, months):
        Mortgage.__init__(self, loan, r, months)
        self.legend = 'Fixed, ' + str(r*100) + '%'
        
class FixedWithPts(Mortgage):
    def __init__(self, loan, r, months, pts):
        Mortgage.__init__(self, loan, r, months)
        self.pts = pts
        self.paid = [loan*(pts/100.0)]
        self.legend = 'Fixed, ' + str(r*100) + '%, '\
                      + str(pts) + ' points'

#Page 111, Figure 8.10
class TwoRate(Mortgage):
    def __init__(self, loan, r, months, teaserRate, teaserMonths):
        Mortgage.__init__(self, loan, teaserRate, months)
        self.teaserMonths = teaserMonths
        self.teaserRate = teaserRate
        self.nextRate = r/12.0
        self.legend = str(teaserRate*100)\
                      + '% for ' + str(self.teaserMonths)\
                      + ' months, then ' + str(r*100) + '%'
    def makePayment(self):
        if len(self.paid) == self.teaserMonths + 1:
            self.rate = self.nextRate
            self.payment = findPayment(self.owed[-1], self.rate,
                                       self.months - self.teaserMonths)
        Mortgage.makePayment(self)

#Page 111, Figure 8.11
def compareMortgages(amt, years, fixedRate, pts, ptsRate,
                     varRate1, varRate2, varMonths):
    totMonths = years*12
    fixed1 = Fixed(amt, fixedRate, totMonths)
    fixed2 = FixedWithPts(amt, ptsRate, totMonths, pts)
    twoRate = TwoRate(amt, varRate2, totMonths, varRate1, varMonths)
    morts = [fixed1, fixed2, twoRate]
    for m in range(totMonths):
        for mort in morts:
            mort.makePayment()
    for m in morts:
        print m
        print ' Total payments = $' + str(int(m.getTotalPaid()))

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--amt',       type=int,    help='Amount of loan',          default=200000)
    parser.add_argument('-y', '--years',     type=int,    help='Length of loan in years', default=30)
    parser.add_argument('-f', '--fixedRate', type=float,  help='fixed rate',              default=0.07)
    parser.add_argument('-p', '--pts',       type=float,  help='Points',                  default=3.25)
    parser.add_argument('-P', '--ptsRate',   type=float,  help='fixed rate',              default=0.05)
    parser.add_argument('-v', '--varRate1',  type=float,  help='fixed rate',              default=0.045)
    parser.add_argument('-u', '--varRate2',  type=float,  help='fixed rate',              default=0.095)
    parser.add_argument('-m', '--varMonths', type=int,    help='Length of variable rate mortgage in months',default=48)


    params=vars(parser.parse_args())

    print params

    compareMortgages(**params)

