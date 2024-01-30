# importing as libraries
import gspread #pip install gspread
import pandas as pd #pip install pandas
import framework as fw #my fuctions

fw.Clear()

# Spreadsheet configuration
SPREADSHEET_ID = '1Byk9WC8dvJYod1OAX5LYZh9zasOyeP_RWGAXf09-qHQ'
try:
    gc = gspread.service_account(filename='key.json')
except FileNotFoundError:
    print("Error: 'key.json' file not found. Please make sure the file is in the correct location.")
    # Encerrar o programa ou tomar outras medidas apropriadas
    exit()

sh = gc.open_by_key(SPREADSHEET_ID)
ws = sh.worksheet('engenharia_de_software')


#get sheet data 
data = ws.get_all_values()

# creat dataframe with pandas lib
df = pd.DataFrame(data[1:], columns=data[0])  # ignore first row (header)

# Select grade columns and convert to number
col_p1, col_p2, col_p3, col_school_absences = 3, 4, 5, 2

#converting to number
p1 = pd.to_numeric(df.iloc[:, col_p1], errors='coerce') 
p2 = pd.to_numeric(df.iloc[:, col_p2], errors='coerce')
p3 = pd.to_numeric(df.iloc[:, col_p3], errors='coerce')
school_absences = pd.to_numeric(df.iloc[:, col_school_absences], errors='coerce')


# adding columns 
situation = []
approved = []


for i in range(2, len(fw.Average(p1, p2, p3))): #read grades
    if fw.SchoolsAbsences(school_absences[i]): #if school_absences is true
        situation.append("Failed due to absence") #the situation is disapproved
        approved.append(0) #add zero in naf
    else: #else         
        average = fw.Average(p1, p2, p3).iloc[i] #save the average in a variable
        if average < 50: #if average is less than 50 (5.0)
            situation.append("Failed due to grades") #the situation is disapproved
            approved.append(0)
        elif 50 <= average < 70: #else if avarege is between 50 (5.0) and 70 (7.0)
            situation.append("Exam failed") #student will need to take the exam
            approved.append(fw.Naf(average)) #naf calculation
        else: 
            situation.append("Approved") #the situation is approved
            approved.append(0) #add zero in naf


# adding column in the DataFrame from 4th row of 7th column
df.iloc[2:, 6] = situation
df.iloc[2:, 7] = approved

# Log messages
print(' === Check the spreadsheet, the data is being updated ===')

# Updating spreadsheet with new information
try:
    for i, value in enumerate(situation):
        ws.update(range_name=f'G{i+4}', values=[[str(value)]], value_input_option='RAW')
    print(' === The situation was updated successfully. ===')
    for i, value in enumerate(approved):
        ws.update(range_name=f'H{i+4}', values=[[float(value)]], value_input_option='RAW')
    print('The Final Approval Grade was updated successfully.')
    print('Spreadsheet updated successfully.')
except Exception as e:
    print(f'Error updating spreadsheet: {e}')

print('=== APPLICATION TERMINATED ===')