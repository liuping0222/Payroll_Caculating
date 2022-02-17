class PayCaculator:

    def __init__(self, gross_salary, insurance_base, housing_base, special_deduction):
        self.gross_salary = gross_salary
        self.insurance_base = insurance_base
        self.housing_base = housing_base
        self.special_deduction = special_deduction

    def income_tax(self, taxable_income):
        '''
        :param taxable_income: Income after deduction of non-taxable income and >= 0
        :return: tax and >= 0
        '''
        # level
        level = [0, 36000, 144000, 300000, 420000, 660000, 960000]
        # tax rate
        rate = [0.03, 0.10, 0.20, 0.25, 0.30, 0.35, 0.45]
        # quick deduction
        deduction = [0, 2520, 16920, 31920, 52920, 85920, 181920]
        tax_rate = 0
        deduction_amount = 0

        if taxable_income < 0:
            taxable_income = 0
        if level[0] <= taxable_income <= level[1]:
            tax_rate = rate[0]
            deduction_amount = deduction[0]
        elif taxable_income <= level[2]:
            tax_rate = rate[1]
            deduction_amount = deduction[1]
        elif taxable_income <= level[3]:
            tax_rate = rate[2]
            deduction_amount = deduction[2]
        elif taxable_income <= level[4]:
            tax_rate = rate[3]
            deduction_amount = deduction[3]
        elif taxable_income <= level[5]:
            tax_rate = rate[4]
            deduction_amount = deduction[4]
        elif taxable_income <= level[6]:
            tax_rate = rate[5]
            deduction_amount = deduction[5]
        else:
            tax_rate = rate[6]
            deduction_amount = deduction[6]

        income_tax = round(taxable_income * tax_rate - deduction_amount, 2)

        return income_tax

    def insurance(self, insurance_base, housing_base):
        '''
        The upper and lower limits of insurance use ShangHai's standards.
        :param insurance_base: including pension insurance, health insurance and unemployment insurance.
        :param housing_base: only including housing fund.
        :return: return the sum of three kinds of insurance and housing fund.
        '''
        upper = 31014
        lower = 5975
        # Checking whether the insurance_base is reasonable
        if insurance_base < lower:
            insurance_base = lower
        elif insurance_base > upper:
            insurance_base = upper
        # Checking housing_base
        if housing_base < lower:
            housing_base = lower
        elif housing_base > upper:
            housing_base = upper

        #  Each insurances' percentage uses  ShangHai's standards
        pensionInsurance = round(insurance_base * 0.08, 2)
        healthInsurance = round(insurance_base * 0.02, 2)
        unemploymentInsurance = round(insurance_base * 0.01, 2)
        # social_insurance is the sum of three kinds of insurance
        social_insurance = pensionInsurance + healthInsurance + unemploymentInsurance
        housingFund = housing_base * 0.12

        return social_insurance, housingFund

    def payroll(self):
        '''

        :param gross_salary: Pre-tax salaries for January to December
        :param insurance_base: Social Security Base for January to December
        :param housing_base: January to December Housing Provident Fund Base
        :return:
        '''
        cumulative_taxable_income = 0
        paid_tax = 0
        social_insurance_list = []
        housingFund_list = []
        month_tax_list = []
        accumulated_tax_paid = []
        net_pay = []
        cumulative_tax_list = []
        # Iterating to generate month's payroll data
        for month in range(1, 13):
            social_insurance, housingFund = self.insurance(self.insurance_base[month-1], self.housing_base[month-1])
            taxable_income = self.gross_salary[month-1] - 5000 - social_insurance - housingFund - self.special_deduction[month-1]
            # Total accumulated taxable income for the current month
            cumulative_taxable_income += taxable_income
            cumulative_tax = self.income_tax(cumulative_taxable_income)
            month_tax = max(0, cumulative_tax - paid_tax)
            # Total paid tax for the current month
            paid_tax += month_tax
            month_net_pay = self.gross_salary[month-1] - social_insurance - housingFund - month_tax

            # Storing monthly payroll data
            social_insurance_list.append(social_insurance)
            housingFund_list.append(housingFund)
            month_tax_list.append(month_tax)
            accumulated_tax_paid.append(paid_tax)
            net_pay.append(month_net_pay)
            cumulative_tax_list.append(max(0,cumulative_tax))

        # A positive number means that the tax paid is less than the tax due and need to pay back the tax. A negative number means that more tax has been paid than is due and a refund can be claimed.

        tax_refunds = max(0, cumulative_tax) - paid_tax

        return social_insurance_list, housingFund_list, month_tax_list, accumulated_tax_paid, net_pay, tax_refunds, cumulative_tax_list


    def bonus_tax(self, bonus):
        # level
        level = [0, 36000, 144000, 300000, 420000, 660000, 960000]
        # tax rate
        rate = [0.03, 0.10, 0.20, 0.25, 0.30, 0.35, 0.45]
        # quick deduction
        deduction = [0, 210, 1410, 2660, 4410, 7160, 15160]
        tax_rate = 0
        deduction_amount = 0

        if level[0] <= bonus <= level[1]:
            tax_rate = rate[0]
            deduction_amount = deduction[0]
        elif bonus <= level[2]:
            tax_rate = rate[1]
            deduction_amount = deduction[1]
        elif bonus <= level[3]:
            tax_rate = rate[2]
            deduction_amount = deduction[2]
        elif bonus <= level[4]:
            tax_rate = rate[3]
            deduction_amount = deduction[3]
        elif bonus <= level[5]:
            tax_rate = rate[4]
            deduction_amount = deduction[4]
        elif bonus <= level[6]:
            tax_rate = rate[5]
            deduction_amount = deduction[5]
        else:
            tax_rate = rate[6]
            deduction_amount = deduction[6]

        bonus_tax = round(bonus * tax_rate - deduction_amount, 2)

        return bonus_tax

    def bonus_divide(self, bonus):
        Unoptimised_bonus_tax = self.bonus_tax(bonus)
        Unoptimised_income_tax = PayCaculator(gross_salary, insurance_base, housing_base, special_deduction).payroll()[-1][-1] # cumulative_tax_list[-1], initial value
        Unoptimised_tax = Unoptimised_bonus_tax + Unoptimised_income_tax
        pre_tax = Unoptimised_tax  # used to store each step' values for comparing

        # Since bonuses are paid at the end of the year, add the portion to December.
        last_month_income = self.gross_salary[-1]
        for num in [0, 36000, 144000, 300000, 420000, 660000, 960000]:
            if num > bonus:
                break
            tmp_bonus_tax = self.bonus_tax(num)
            # as gross_salary[-1] is self-decreasing, just add the increment at each step
            self.gross_salary[-1] = last_month_income + bonus - num
            tmp_income_tax = PayCaculator(gross_salary, insurance_base, housing_base, special_deduction).payroll()[-1][-1] # cumulative_tax_list[-1], updating value
            optimised_tax = tmp_bonus_tax + tmp_income_tax
            # updating optimised values
            if optimised_tax < pre_tax:
                optimised_bonus = num
                optimised_income = bonus - num
                pre_tax = optimised_tax
        # the value of tax avoided
        difference = Unoptimised_tax - optimised_tax
        return Unoptimised_tax, optimised_tax, optimised_bonus, optimised_income, difference

    def output(self):
        # --- for displaying results of test cases ---
        social_insurance_list, housingFund_list, month_tax_list, accumulated_tax_paid, net_pay, tax_refunds, cumulative_tax = test.payroll()
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        for month in range(0, 12):
            print('\nMonth: ', months[month],
                  '\nGross Salary:', gross_salary[month],
                  '\nSocial Insurance: ', social_insurance_list[month],
                  '\nHousing Fund: ', housingFund_list[month],
                  '\nTax for Current Month: ', month_tax_list[month],
                  '\nAccumulated Tax Paid: ', accumulated_tax_paid[month],
                  '\nNet Pay: ', net_pay[month])
        # total data from Jan to Dec
        print("\n----Total Income from Jan to Dec ----",
              "\n Sum of Gross Income: ", sum(gross_salary),
              "\n Sum of Social Insurance: ", sum(social_insurance_list),
              "\n Sum of Social Insurance: ", sum(housingFund_list),
              "\n Sum of Paid: ", sum(month_tax_list),
              "\n Sum of tax due：", cumulative_tax[-1],
              "\n Sum of Net Pay: ", sum(net_pay))
        if tax_refunds > 0:
            print('You will need to make a back payment of', tax_refunds, 'Yuan.')
        elif tax_refunds < 0:
            print('You will get a tax refund of', -tax_refunds, 'Yuan.')
        else:
            print("You don't do anything.")

        # test def bonus()
        Unoptimised_tax, optimised_tax, optimised_bonus, optimised_income, difference = test.bonus_divide(90000)

        print('\nUnoptimised Total Tax: ', Unoptimised_tax,
              '\nOptimised Total Tax: ', optimised_tax,
              '\nOptimised Bonus: ', optimised_bonus,
              '\nAdded to Dec Income: ', optimised_income,
              '\nTax Saved: ', difference)
        return

# test case
gross_salary = [10000] * 6 + [6000] * 6
insurance_base = [10000] * 12
housing_base = [10000] * 12
special_deduction = [2000] * 12
test = PayCaculator(gross_salary, insurance_base, housing_base, special_deduction)
test.payroll()
test.output()

