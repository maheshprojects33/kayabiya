from datetime import date
import calendar
from loan.models import *

from decimal import Decimal

# def calculate_accrued_interest(loan_amount, interest_rate, disbursed_date, end_date):
    
#     current_day = timezone.now().date()
#     calculation_till_date = end_date
#     days = (current_day + timedelta(days=1) - disbursed_date).days
#     converted_interest_rate = interest_rate / 100
#     calulated_days = Decimal(days / 365)

#     if current_day > calculation_till_date:
#     # If the current date is beyond the calculation period, Fine Starts
#         pass
#     else:
#         # Calculate the interest amount for each day
#         interest_amount = loan_amount * converted_interest_rate * calulated_days
#         rounded_value = interest_amount.quantize(Decimal('0.01'))
#         return rounded_value



    # '''
    # day 1 interest amount
    # interest_amount = loan_aount * interest_rate * (days / 365)  
    #                 = 25000 * 0.05 * (1/365)
    #                 = 3.42
    # day 2 interest amount
    # interest_amount = loan_aount * interest_rate * (days / 365)  
    #                 = 25000 * 0.05 * (2/365)
    #                 = 6.84
    # day 3 interest amount
    # interest_amount = loan_aount * interest_rate * (days / 365)  
    #                 = 25000 * 0.05 * (3/365)
    #                 = 10.26
    # '''

def get_monthly_interest_amount(loan_amount, loan_tenure, interest_rate, loan_account_number):
    
    today = date.today()
    loan_amount = Decimal(loan_amount)
    interest_rate = Decimal(interest_rate)
    loan_account = LoanAccount.objects.get(loan_account_number=loan_account_number)

    monthly_interests = []
    year = today.year
    month = today.month

    for i in range(int(loan_tenure)):
        # Calculate the year and month for each tenure period
        calc_month = (month + i - 1) % 12 + 1
        calc_year = year + ((month + i - 1) // 12)
        days_in_month = calendar.monthrange(calc_year, calc_month)[1]
        days_in_month_decimal = Decimal(days_in_month)

        monthly_interest = loan_amount * (interest_rate / Decimal('100')) * (days_in_month_decimal / Decimal('365'))
        monthly_interests.append(monthly_interest.quantize(Decimal('0.01')))

        b = LoanInterest.objects.create(
            loan=loan_account,
            interest_amount=monthly_interest,
            month=calc_month
        )

    return b

