import urllib.request
import matplotlib.pyplot as plt
plt.close('all')
dict_confirmed_daily = {}
dict_recovered_daily = {}
dict_death_daily = {}
# TT,AN,AP,AR,AS,BR,CH,CT,DD,DL,DN,GA,GJ,HP,HR,JH,JK,KA,KL,LA,LD,MH,ML,MN,MP,MZ,NL,OR,PB,PY,RJ,SK,TG,TN,TR,UP,UT,WB,
list_state = ['Total', "Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chandigarh", "Chhattisgarh", "Div & Daman", "Delhi", "DADRA AND NAGAR HAVELI", "Goa", "Gujarat",  "Himachal Pradesh", "Haryana", "Jharkhand", "Jammu and Kashmir",
              "Karnataka", "Kerala", "Lakshadweep", "Ladakh", "Maharashtra", "Meghalaya", "Manipur", "Madhya Pradesh", "Mizoram", "Nagaland", "Odisha", "Punjab", "Puducherry", "Rajasthan", "Sikkim", "Telangana", "Tamilnadu", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"]


for i in list_state:
    dict_confirmed_daily[i] = []
for i in list_state:
    dict_recovered_daily[i] = []
for i in list_state:
    dict_death_daily[i] = []


def read_parse(url, filename, dict):
    with urllib.request.urlopen(url) as response:
        html = response.read()

    f = open(filename, 'w')
    f.write(html.decode("utf-8"))
    f.close()
    dates = []
    f1 = open(filename, 'r')
    f1.readline()
    data = f1.readlines()
    for line in data:
        cols = line.split(',')
        dates.append(cols[0])
        k = 1
        for i in list_state:
            if cols[k] != '':
                dict[i].append(float(cols[k]))
            k += 1
    return dict, dates


def doubling_plot(no_of_days, start, threshold, doubling_days):
    x = [i for i in range(start, no_of_days, doubling_days)]
    y = [threshold]
    # doubling_days=3
    k = 0
    for i in range(0, no_of_days, doubling_days):
        if i % doubling_days == 0 and i != 0:
            y.append(2 * y[k-1])
        k += 1
    # fig, ax = plt.subplots(figsize=(8, 6))
    print(x, y)
    plt.plot(x, y, ls='--', color='grey')
    plt.annotate(f'every\n{doubling_days} days',
                 (x[-1], y[-1]), fontsize=8)


url1 = "http://api.covid19india.org/states_daily_csv/confirmed.csv"
url2 = "http://api.covid19india.org/states_daily_csv/recovered.csv"
url3 = "http://api.covid19india.org/states_daily_csv/deceased.csv"
dict_confirmed_daily, dates = read_parse(
    url1, 'confirmed_daily', dict_confirmed_daily)
dict_recovered_daily, dates = read_parse(
    url2, 'recovered_daily', dict_recovered_daily)
dict_death_daily, dates = read_parse(url3, 'death_daily', dict_death_daily)

dict_confirmed_cumulative = {}
dict_recovered_cumulative = {}
dict_death_cumulative = {}

for i in list_state:
    dict_confirmed_cumulative[i] = []
    dict_recovered_cumulative[i] = []
    dict_death_cumulative[i] = []

k = 0
for i in list_state:
    for j in range(len(dict_confirmed_daily[i])):
        dict_confirmed_cumulative[i].append(sum(dict_confirmed_daily[i][:j]))

for i in list_state:
    for j in range(len(dict_recovered_daily[i])):
        dict_recovered_cumulative[i].append(sum(dict_recovered_daily[i][:j]))


for i in list_state:
    for j in range(len(dict_death_daily[i])):
        dict_death_cumulative[i].append(sum(dict_death_daily[i][:j]))


first_confirmed_dict = {}
first_death_dict = {}
first_recovered_dict = {}

for i in list_state:
    first_confirmed_dict[i] = []
    first_death_dict[i] = []
    first_recovered_dict[i] = []

threshold_confirmed = 1000
threshold_death = 10
threshold_recovered = 100
no_of_days = 35
for i in list_state:
    for j in dict_confirmed_cumulative[i]:
        if j >= threshold_confirmed:
            first_confirmed_dict[i].append(j)
for i in list_state:
    for j in dict_recovered_cumulative[i]:
        if j >= threshold_recovered:
            first_recovered_dict[i].append(j)
for i in list_state:
    for j in dict_death_cumulative[i]:
        if j >= threshold_death:
            first_death_dict[i].append(j)


states = ['Gujarat', 'Tamilnadu',
          'Maharashtra', 'Madhya Pradesh', 'Delhi']
color_list = ['#ef253c', '#05d69e', '#ffbe0a', 'black',
              '#1ae8ff',  '#6495ed', '#a4bd00', 'blue', '#8236ec', '#a33e48']
# recovery
figure, ax = plt.subplots(figsize=(8, 6))
k = 0
for i in states:
    plt.plot(first_recovered_dict[i], label=i, color=color_list[k])
    # , marker='o', markerfacecolor='white', markeredgecolor=color_list[k]
    plt.annotate(i, (len(first_recovered_dict[i])-1, first_recovered_dict[i]
                     [-1]+0.05*first_recovered_dict[i][-1]), color=color_list[k], fontsize=8)
    plt.ylabel('Recovered', fontsize=12)
    plt.xlabel(
        f'No of days since >= {threshold_recovered} recovery', fontsize=12)
    k += 1
doubling_plot(no_of_days, 0, threshold_recovered, 3)
doubling_plot(no_of_days, 0, threshold_recovered, 5)
doubling_plot(no_of_days, 0, threshold_recovered, 7)
plt.xlim((0, no_of_days))
plt.ylim((threshold_recovered, 5e3))
plt.yscale('log')
ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%d'))
# plt.legend()
plt.figtext(0.01, 0.01, f'By Parth Patel (data from {dates[0]:} to {dates[-1]}) \nData source: covid19india.org/',
            horizontalalignment='left', fontsize=7, color='grey')
plt.minorticks_on()
plt.grid(which='major', axis='both')
plt.savefig('recovered_state')
plt.show()


# confirmed
figure, ax = plt.subplots(figsize=(8, 6))
k = 0
for i in states:
    plt.plot(first_confirmed_dict[i], label=i, color=color_list[k])
    # , marker='o', markerfacecolor='white', markeredgecolor=color_list[k]
    plt.annotate(i, (len(first_confirmed_dict[i])-1, first_confirmed_dict[i]
                     [-1]+0.05*first_confirmed_dict[i][-1]), color=color_list[k], fontsize=8)
    plt.ylabel('Confirmed', fontsize=12)
    plt.xlabel(
        f'No of days since >= {threshold_confirmed} confirmed', fontsize=12)
    k += 1
# every # days cases doubled
doubling_plot(no_of_days, 0, threshold_confirmed, 3)
doubling_plot(no_of_days, 0, threshold_confirmed, 5)
doubling_plot(no_of_days, 0, threshold_confirmed, 7)
plt.xlim((0, no_of_days))
plt.ylim(threshold_confirmed, 3e4)
plt.yscale('log')
ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%d'))
# plt.legend()
plt.tight_layout()
plt.figtext(0.01, 0.01, f'By Parth Patel (data from {dates[0]:} to {dates[-1]}) \nData source: covid19india.org/',
            horizontalalignment='left', fontsize=7, color='grey')
plt.minorticks_on()
plt.grid(which='major', axis='both')
# plt.grid(which='minor', axis='both')

plt.tight_layout()
plt.tight_layout()
plt.savefig('confirmed_state', dpi=500)
# plt.show()


# death
figure, ax = plt.subplots()
k = 0
for i in states:
    plt.plot(first_death_dict[i], label=i, color=color_list[k])
    # , marker='o', markerfacecolor='white', markeredgecolor=color_list[k]
    plt.annotate(i, (len(first_death_dict[i])-1, first_death_dict[i]
                     [-1]+0.05*first_death_dict[i][-1]), color=color_list[k], fontsize=8)
    plt.ylabel('Deaths', fontsize=12)
    plt.xlabel(f'No of days since {threshold_death}th death', fontsize=12)
    k += 1
doubling_plot(no_of_days, 0, threshold_death, 3)
doubling_plot(no_of_days, 0, threshold_death, 5)
doubling_plot(no_of_days, 0, threshold_death, 7)
plt.xlim((0, no_of_days))
plt.ylim((threshold_death, 5e3))
plt.yscale('log')
ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%d'))
# plt.legend()
plt.figtext(0.01, 0.01, f'By Parth Patel (data from {dates[0]:} to {dates[-1]}) \nData source: covid19india.org/',
            horizontalalignment='left', fontsize=8, color='grey')
plt.minorticks_on()
plt.grid(which='major', axis='both')
plt.tight_layout()
plt.savefig('Death_state', dpi=500)
plt.show()
