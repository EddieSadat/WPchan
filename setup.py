import pandas as pd

df = pd.read_csv('wplist.csv')

# df.loc[len(df)] = ["Madoka", 'https://anilist.co/anime/9756/Mahou-Shoujo-MadokaMagica', True]
# df.to_csv('wplist.csv')

# msg = '## Suggested WPs\n'
# for row in range(len(df)):
#     if not df.iloc[row].Completed:
#         msg += f'- [{df.iloc[row].Title}](<{df.iloc[row].Link}>)\n'

# print(msg)


# msg = '## Completed WPs\n'
# for row in range(len(df)):
#     if df.iloc[row].Completed:
#         msg += f'- [{df.iloc[row].Title}](<{df.iloc[row].Link}>)\n'

# print(msg)



# msg = '## All WPs\n'
# for row in range(len(df)):
#     if not df.iloc[row].Completed:
#         msg += f'- [{df.iloc[row].Title}](<{df.iloc[row].Link}>)\n'
#     elif df.iloc[row].Completed:
#             msg += f'- ~~[{df.iloc[row].Title}](<{df.iloc[row].Link}>)~~ (Completed)\n'

# print(msg)


# print(df.drop(df.loc[df.Title == 'BECK'].index).reset_index(drop=True))


# new_row = ["TEST", "https://anilist.co/anime/57/BECK", True]
# df.loc[df['Title'] == 'BECK'] = new_row
# print(df)


# ### 100% completionist FLCL 
# ```
# Fri, 06-13: 1-2
# Sat, 06-14: 3-4
# Sun, 06-15: 5-6
# ------------------
# Mon, 06-16: 7
# Tue, 06-17: 8
# Wed, 06-18: 9
# Thu, 06-19: 10
# Fri, 06-20: 11-12
# Sat, 06-21: 13-14
# Sun, 06-22: 15-16
# ------------------
# Mon, 06-23: 17
# Tue, 06-24: 18
# ```


# from datetime import datetime, timedelta

# def generate_dates(start_date_str, num_days):
#     current_year = datetime.now().year
#     start_date = datetime.strptime(f"{current_year}-{start_date_str}", "%Y-%m-%d")
    
#     result = []
#     for i in range(num_days):
#         day = start_date + timedelta(days=i)
#         result.append(f"{day.strftime('%a')}, {day.strftime('%m-%d')}")
    
#     return result


# dates = generate_dates('06-13', 12)
# count = 0

# while count < len(dates):
#     print(dates[count])
#     count += 1



# from datetime import datetime, timedelta

# def generate_custom_dates(start_date_str, num_days):
#     current_year = datetime.now().year
#     start_date = datetime.strptime(f"{current_year}-{start_date_str}", "%Y-%m-%d")

#     result = []
#     count = 1

#     for i in range(num_days):
#         day = start_date + timedelta(days=i)
#         day_name = day.strftime('%a')
#         date_str = day.strftime('%m-%d')

#         # Determine if it's weekend (Fri/Sat/Sun)
#         if day_name in ['Fri', 'Sat', 'Sun']:
#             day_value = 2
#         else:
#             day_value = 1

#         if day_value == 1:
#             result.append(f"{day_name}, {date_str}: {count}")
#         else:
#             result.append(f"{day_name}, {date_str}: {count}-{count + 1}")

#         count += day_value

#     return result


# dates = generate_custom_dates('06-13', 12)
# for d in dates:
#     print(d)


# from datetime import datetime, timedelta

# def generate_dates_until_count(start_date_str, target_count):
#     current_year = datetime.now().year
#     start_date = datetime.strptime(f"{current_year}-{start_date_str}", "%Y-%m-%d")

#     result = []
#     count = 1
#     i = 0

#     while count <= target_count:
#         day = start_date + timedelta(days=i)
#         day_name = day.strftime('%a')
#         date_str = day.strftime('%m-%d')

#         # Weekend logic: Fri, Sat, Sun = +2
#         if day_name in ['Fri', 'Sat', 'Sun']:
#             increment = 2
#         else:
#             increment = 1

#         if increment == 1:
#             label = f"{count}"
#         else:
#             if count + 1 > target_count:
#                 # Don't go beyond target_count
#                 label = f"{count}"
#                 increment = 1
#             else:
#                 label = f"{count}-{count + 1}"

#         result.append(f"{day_name}, {date_str}: {label}")
#         count += increment
#         i += 1

#     return result



# dates = generate_dates_until_count('06-13', 18)
# msg = "'''\n"
# for d in dates:
#     if d[:3] == 'Sun':
#         msg += f'{d}\n------------------\n'
#     else:
#         msg += f'{d}\n'
# msg += "'''"
# print(msg)


print(df[df.Title == 'Grand Blue'].Title.to_string(index = False))
# df.loc[df.Title == 'Grand Blue']['Link']