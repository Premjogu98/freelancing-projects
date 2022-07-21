import csv

with open('employee_file2.csv', mode='w',newline='',encoding='utf-8') as csv_file:
    fieldnames = ['emp_name', 'dept', 'birth_month']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    writer.writerow({'emp_name': 'John Smith', 'dept': 'Accounting', 'birth_month': 'November'})
    writer.writerow({'emp_name': 'हिंदी शब्दकोश', 'dept': 'IT', 'birth_month': 'March'})