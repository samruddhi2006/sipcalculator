import matplotlib.pyplot as plt
import csv
import os

Name = input("Enter your name: ")

# to validate number entry and input
def get_positive_float(prompt):
    while True:
        # Ask user for input
        value = input(prompt)
        # Try to convert to float
        try:
            number = float(value)
            # Check if positive
            if number <= 0:
                print("Please enter a positive number.")
            else:
                return number
        except ValueError:
            print("Invalid input. Please enter a number.")

# to get lumpsum investment functionality
def get_optional_lumpsum():
    response = input("Do you want to add a lumpsum investment? (y/n): ").lower()
    if response == 'y':
        return get_positive_float("Enter the lumpsum investment amount: ")
    return 0

# for investment frequency
def plan():
    while True:
        frequency = input("Enter investment frequency monthly/yearly (m / y) : ").lower()
        if frequency ==  "y" :
            yearly_investment = get_positive_float("Enter Yearly Investment Amount: ")
            mi = yearly_investment/12
        else:
            monthly_investment = get_positive_float("Enter Monthly Investment Amount: ")
            mi = monthly_investment
        return mi

# to calculate SIP and lumpsum
def calculate_sip(mi, err, tp, lumpsum):
    i=err/12/100
    M=tp*12

    SIP=mi*((((1+i)**(M))-1)*(1+i))/i
    lumpsum_value = lumpsum * ((1+i) ** M)
    total_value  = SIP + lumpsum_value
    return SIP, lumpsum_value, total_value

# to show yearly growth table
def show_yearly_summary(mi, err, tp):
    print("\n------- Yearly Summary -------")
    print(f"{'Year':<5} {'Invested So Far':<20} {'Value at Year-End':<20}")
    r = err / 12 / 100
    for year in range(1, int(tp)+1):
        months = year * 12
        invested = mi * months
        fv = mi *(((1 + r) ** months - 1) * (1 + r)) / r
        print(f"{year:<5} ₹ {round(invested):<22} ₹ {round(fv):<18}")

# for yearly SIP graph
def plot_yearly_growth(mi, err, tp):
    r = err / 12 / 100
    x_years = []
    y_values = []
    for year in range(1, int(tp) + 1):
        months = year * 12
        fv = mi * (((1 + r) ** months - 1) * (1 + r)) / r
        x_years.append(year)
        y_values.append(round(fv, 2))
    
    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(x_years, y_values, marker='o', color='green', linestyle='-')
    plt.title("📈 SIP Growth Over Time")
    plt.xlabel("Year")
    plt.ylabel("Investment Value (₹)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# To save output to csv file using csv module
def save_summary_to_csv(Name, mi, err, tp, fv, lumpsum_value, total_invested, returns):
    filename = "sip_summary.csv"
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write header  if new file
        if not file_exists:
            writer.writerow(["Name", "Monthly Investment", "Rate (%)", "Years", "Final Value", "Lumpsum Value", "Total Invested", "Gain"])
        writer.writerow([Name, mi, err, tp, round(fv), round(lumpsum_value), round(total_invested), round(returns)])
    print(f"\n Summary saved to '{filename}' successfully.")



# Main script

mi = plan()
# mi=get_positive_float("Enter Monthly Investment : ")
err=get_positive_float("Enter the  Expected return rate : ")
tp=get_positive_float("Enter the time period (in years) : ")
lumpsum = get_optional_lumpsum()

sip_value, lumpsum_value, fv = calculate_sip(mi, err, tp, lumpsum)

show_yearly_summary(mi, err, tp)
plot_yearly_growth(mi, err, tp)

total_invested = mi * tp * 12 + lumpsum
returns = fv - total_invested

print("\n-------- 📊 SIP Summary ----------")
print(f"Name of Investor :            {Name}")
print(f"Future Value of SIP :       ₹ {round(sip_value, 2)} ")
print(f"Future value of Lumpsum :   ₹ {round(lumpsum_value, 2)}")
print(f"Total Invested Amount :     ₹ {round(total_invested, 2)}")
print(f"Estimated Returns :         ₹ {round(returns, 2)}")
print(f"Total Future Value :        ₹ {round(fv, 2)}")

save_summary_to_csv(Name, mi, err, tp, fv, lumpsum_value, total_invested, returns)
