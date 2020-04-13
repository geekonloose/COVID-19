import numpy as np
import matplotlib.pyplot as plt
import csv

plt.close('all')


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
    plt.semilogy(x, y, ls='--', color='grey')
    plt.annotate(f'every {doubling_days} days',
                 (no_of_days/2, y[int(len(y)/2)]), fontsize=8)


f1 = open('/mnt/0E48122648120D59/external_git_repo/covid_forked/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', 'r')
f2 = open('/mnt/0E48122648120D59/external_git_repo/covid_forked/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv', 'r')
f3 = open('/mnt/0E48122648120D59/external_git_repo/covid_forked/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv', 'r')
# f1 = open('D:/external_git_repo/covid_forked/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', 'r')
# f2 = open('D:/external_git_repo/covid_forked/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv', 'r')
# f3 = open('D:/external_git_repo/covid_forked/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv', 'r')
d1 = csv.reader(f1)    # first line is header
confirmed_data = list(d1)    # to retain the data
d2 = csv.reader(f2)    # first line is header
death_data = list(d2)    # to retain the data
d3 = csv.reader(f3)    # first line is header
recovered_data = list(d3)    # to retain the data
f1.close()
f2.close()
f3.close()
# print(list(confirmed_data))

countries = set()
for i in confirmed_data:
    countries.add(i[1])
countries.remove('Country/Region')
confirmed_dict = {}
for i in countries:
    confirmed_dict[i] = np.zeros(len(confirmed_data[0][4:]))
death_dict = {}
for i in countries:
    death_dict[i] = np.zeros(len(confirmed_data[0][4:]))
recovered_dict = {}
for i in countries:
    recovered_dict[i] = np.zeros(len(confirmed_data[0][4:]))

for i in confirmed_dict:
    for line in confirmed_data:
        if line[1] == i:
            confirmed_dict[i] += np.array(list(map(float,
                                                   line[4:])))

for i in death_dict:
    for line in death_data:
        if line[1] == i:
            death_dict[i] += np.array(list(map(float,
                                               line[4:])))

for i in recovered_dict:
    for line in recovered_data:
        if line[1] == i:
            recovered_dict[i] += np.array(list(map(float,
                                                   line[4:])))

dates = confirmed_data[0][4:]


# country = 'India'
# plt.plot(dates, confirmed_dict[country])
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.show()

first_confirmed_dict = {}
first_death_dict = {}
first_recovered_dict = {}

for i in countries:
    first_confirmed_dict[i] = []
    first_death_dict[i] = []
    first_recovered_dict[i] = []

threshold_confirmed = 100
threshold_death = 10
threshold_recovered = 10
no_of_days = 90
for i in countries:
    for j in confirmed_dict[i]:
        if j >= threshold_confirmed:
            first_confirmed_dict[i].append(j)
for i in countries:
    for j in recovered_dict[i]:
        if j >= threshold_recovered:
            first_recovered_dict[i].append(j)
for i in countries:
    for j in death_dict[i]:
        if j >= threshold_death:
            first_death_dict[i].append(j)

list_countries = ['Italy', 'India', 'Spain', 'China',
                  'France', 'United Kingdom', 'Iran', 'US', 'Japan', 'Korea, South']
color_list = ['#ef253c', '#05d69e', '#ffbe0a', 'black',
              '#1ae8ff',  '#6495ed', '#a4bd00', 'blue', '#8236ec', '#a33e48']

# death
plt.figure(figsize=(8, 6))
k = 0
for i in list_countries:
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
plt.xlim((0, 80))
plt.ylim((threshold_death, 5e4))
plt.yscale('log')
# plt.legend()
plt.figtext(0.01, 0.01, f'By Parth Patel (data from {dates[0]:} to {dates[-1]}) \nData source: https://github.com/CSSEGISandData/COVID-19',
            horizontalalignment='left', fontsize=8, color='grey')
plt.minorticks_on()
plt.grid(which='major', axis='both')
plt.tight_layout()
plt.show()
plt.savefig('Death', dpi=500)

# recovery
plt.figure(figsize=(8, 6))
k = 0
for i in list_countries:
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
plt.ylim((threshold_recovered, 9e4))
plt.yscale('log')
# plt.legend()
plt.figtext(0.01, 0.01, f'By Parth Patel (data from {dates[0]:} to {dates[-1]}) \nData source: https://github.com/CSSEGISandData/COVID-19',
            horizontalalignment='left', fontsize=7, color='grey')
plt.minorticks_on()
plt.grid(which='major', axis='both')
# plt.grid(which='minor', axis='both')

plt.tight_layout()
plt.show()
plt.savefig('recovered', dpi=500)

# confirmed
figure, ax = plt.subplots(figsize=(8, 6))
k = 0
for i in list_countries:
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
plt.ylim((threshold_confirmed, 1e6))
plt.yscale('log')
ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%d'))
# plt.legend()
plt.figtext(0.01, 0.01, f'By Parth Patel (data from {dates[0]:} to {dates[-1]}) \nData source: https://github.com/CSSEGISandData/COVID-19',
            horizontalalignment='left', fontsize=7, color='grey')
plt.minorticks_on()
plt.grid(which='major', axis='both')
# plt.grid(which='minor', axis='both')

plt.tight_layout()
plt.show()
plt.savefig('confirmed', dpi=500)

# rise confirmed
fig, ax = plt.subplots(figsize=(8, 6))
k = 0
for i in list_countries:
    rise_day_by_day = np.diff(first_confirmed_dict[i])
    plt.plot(rise_day_by_day, color=color_list[k], label=i)
    plt.annotate(i, (len(rise_day_by_day)-1, rise_day_by_day
                     [-1]+0.05*rise_day_by_day[-1]), color=color_list[k], fontsize=8)
    plt.ylabel('each day confirmed cases reported', fontsize=12)
    plt.xlabel(
        f'No of days since >= {threshold_confirmed} confirmed', fontsize=12)
    k += 1
plt.xlim((0, no_of_days))
plt.ylim((threshold_confirmed, 1e5))
plt.yscale('log')
ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%d'))
# plt.legend()
plt.figtext(0.01, 0.01, f'By Parth Patel (data from {dates[0]:} to {dates[-1]}) \nData source: https://github.com/CSSEGISandData/COVID-19',
            horizontalalignment='left', fontsize=7, color='grey')
plt.minorticks_on()
plt.grid(which='major', axis='both')
# plt.grid(which='minor', axis='both')

plt.tight_layout()
plt.savefig('rise_confirmed', dpi=500)
plt.show()

# rise recovered
threshold_recovered = 1
fig, ax = plt.subplots(figsize=(8, 6))
k = 0
for i in list_countries:
    rise_day_by_day = np.diff(first_recovered_dict[i])
    plt.plot(rise_day_by_day, color=color_list[k], label=i)
    plt.annotate(i, (len(rise_day_by_day)-1, rise_day_by_day
                     [-1]+0.05*rise_day_by_day[-1]), color=color_list[k], fontsize=8)
    plt.ylabel('each day recovered reported', fontsize=12)
    plt.xlabel(
        f'No of days since >= {threshold_recovered} recovered', fontsize=12)
    k += 1
plt.xlim((0, no_of_days))
plt.ylim((threshold_recovered, 9e3))
plt.yscale('log')
ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%d'))
# plt.legend()
plt.figtext(0.01, 0.01, f'By Parth Patel (data from {dates[0]:} to {dates[-1]}) \nData source: https://github.com/CSSEGISandData/COVID-19',
            horizontalalignment='left', fontsize=7, color='grey')
plt.minorticks_on()
plt.grid(which='major', axis='both')
# plt.grid(which='minor', axis='both')

plt.tight_layout()
plt.show()
plt.savefig('rise_recovered', dpi=500)

# rise_death
fig, ax = plt.subplots(figsize=(8, 6))
k = 0
for i in list_countries:
    rise_day_by_day = np.diff(first_death_dict[i])
    plt.plot(rise_day_by_day, color=color_list[k], label=i)
    plt.annotate(i, (len(rise_day_by_day)-1, rise_day_by_day
                     [-1]+0.05*rise_day_by_day[-1]), color=color_list[k], fontsize=8)
    plt.ylabel('each day deaths reported', fontsize=12)
    plt.xlabel(
        f'No of days since >= {threshold_death} death', fontsize=12)
    k += 1
plt.xlim((0, no_of_days))
plt.ylim((threshold_death, 3e3))
plt.yscale('log')
ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%d'))
# plt.legend()
plt.figtext(0.01, 0.01, f'By Parth Patel (data from {dates[0]:} to {dates[-1]}) \nData source: https://github.com/CSSEGISandData/COVID-19',
            horizontalalignment='left', fontsize=7, color='grey')
plt.minorticks_on()
plt.grid(which='major', axis='both')
# plt.grid(which='minor', axis='both')

plt.tight_layout()
plt.show()
plt.savefig('rise_death', dpi=500)
