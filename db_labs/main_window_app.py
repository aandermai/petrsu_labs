import pyodbc
from tkinter import *
from tkinter import ttk
from window_app import *
from cabinet_work_report import *
from patient_report import *
from doctor_report import *

connect = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=192.168.112.103; DATABASE=db22203; UID=User013; PWD=User013@!71')
cursor = connect.cursor()

root = Tk()
root.title("Главная форма")
root.geometry("1200x500")
root["bg"] = "white"

root_name_label = Label(root, text="Главная форма", font='Montserrat 20', background="white", pady=15)
root_name_label.pack()

view_patients_button = ttk.Button(root, text="Просмотр списка пациентов", command=view_patients)
view_patients_button.pack(pady=15)

cabinet_work_report_button = ttk.Button(root, text="Отчёт о работе кабинетов", command=do_cabinet_work_report)
cabinet_work_report_button.pack(pady=15)

patient_report_button = ttk.Button(root, text="Отчёт о пациентах", command=do_patients_report)
patient_report_button.pack(pady=15)

doctors_query = """
    SELECT 
        intDoctorId,
        RTRIM(txtDoctorName) AS [ФИО]
    FROM tblDoctor
    ORDER BY [ФИО];
    """
    
cursor.execute(doctors_query)
doctors = cursor.fetchall()


label = Label(root, text="Выберите доктора:", font=("Arial", 12), bg="white")
label.pack(pady=10)

doctor_var = StringVar()
doctor_combo = ttk.Combobox(root, textvariable=doctor_var, width=40)
doctor_combo['values'] = [doctor[1] for doctor in doctors]
doctor_combo.pack(pady=10)

cursor.execute("EXEC sp_doctor_patient_count")
rows = cursor.fetchall()
print("Результаты процедуры из задания 16:")
for row in rows:
    row[0] = row[0].rstrip()
    print(row)
print("\n")

def get_selected_doctor():
    selected_doctor = doctor_var.get()
    if selected_doctor:
        # Получаем ID выбранного доктора
        doctor_id = None
        for doc_id, doc_name in doctors:
            if doc_name == selected_doctor:
                doctor_id = doc_id
                break
        
        if doctor_id:
            print(f"Выбран доктор: {selected_doctor}, ID: {doctor_id}")
            try:
                # Проверка работы процедуры

                cursor.execute("EXEC CreateDoctorReportTempTable @DoctorId = ?", doctor_id)
                rows = cursor.fetchall()

                # Выводим результаты
                print("Результаты процедуры из задания 17:")
                for row in rows:
                    print(row)
            
                # Запускаем отчет
                do_doctor_report(doctor_id)
                
            except pyodbc.Error as e:
                print(f"Ошибка выполнения процедуры: {e}")
        else:
            print("Доктор не найден!")
    else:
        print("Выберите доктора!")


generate_doctor_button = ttk.Button(text="Отчёт о докторах", command=get_selected_doctor)
generate_doctor_button.pack(pady=15)

root.mainloop()