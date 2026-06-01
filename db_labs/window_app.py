import pyodbc
from datetime import *
from tkcalendar import *
from tkinter import *
from tkinter import ttk

print("Подключаемся к базе данных...")
connect = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=192.168.112.103; DATABASE=db22203; UID=User013; PWD=User013@!71')
print("Успешное подключение!")
cursor = connect.cursor()


def add_patient(root):
    def add_patient_to_db():
        sql_query = "INSERT tblPatient (txtPatientSurname, txtPatientName, txtPatientSecondName, datBirthday, txtAdress) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(sql_query, (surname_field.get(), name_field.get(), second_name_field.get(), dob_field.get(), address_field.get()))
        connect.commit()
        print("Данные успешно добавлены!")
        window.destroy()
        root.destroy()
        view_patients()
        


    window = Tk()
    window.title("Новый пациент")
    window.geometry("1280x500")
    window["bg"] = "white"

    window_name_label = Label(window, text="Добавление пациента", font='Montserrat 20', background="white", pady=15)
    window_name_label.pack()

    info_frame = Frame(window, bg="white")
    info_frame.pack(padx=20, pady=20)

    # Фамилия
    surname_frame = Frame(info_frame, bg="white")
    surname_label = Label(surname_frame, text="Фамилия:", bg="white", width=15, anchor="w")
    surname_field = ttk.Entry(surname_frame, width=30)
    surname_frame.pack(fill=X, pady=8)
    surname_label.pack(side=LEFT)
    surname_field.pack(side=LEFT, fill=X, expand=True, padx=(10, 0))

    # Имя
    name_frame = Frame(info_frame, bg="white")
    name_label = Label(name_frame, text="Имя:", bg="white", width=15, anchor="w")
    name_field = ttk.Entry(name_frame, width=30)
    name_frame.pack(fill=X, pady=8)
    name_label.pack(side=LEFT)
    name_field.pack(side=LEFT, fill=X, expand=True, padx=(10, 0))

    # Отчество
    second_name_frame = Frame(info_frame, bg="white")
    second_name_label = Label(second_name_frame, text="Отчество:", bg="white", width=15, anchor="w")
    second_name_field = ttk.Entry(second_name_frame, width=30)
    second_name_frame.pack(fill=X, pady=8)
    second_name_label.pack(side=LEFT)
    second_name_field.pack(side=LEFT, fill=X, expand=True, padx=(10, 0))

    # Дата рождения
    dob_frame = Frame(info_frame, bg="white")
    dob_label = Label(dob_frame, text="Дата рождения:", bg="white", width=15, anchor="w")
    dob_field = DateEntry(dob_frame, date_pattern='dd.MM.yyyy', width=28)
    dob_frame.pack(fill=X, pady=8)
    dob_label.pack(side=LEFT)
    dob_field.pack(side=LEFT, fill=X, expand=True, padx=(10, 0))

    # Адрес
    address_frame = Frame(info_frame, bg="white")
    address_label = Label(address_frame, text="Адрес:", bg="white", width=15, anchor="w")
    address_field = ttk.Entry(address_frame, width=30)
    address_frame.pack(fill=X, pady=8)
    address_label.pack(side=LEFT)
    address_field.pack(side=LEFT, fill=X, expand=True, padx=(10, 0))

    button_frame = Frame(window, bg="white")
    add_button = ttk.Button(button_frame, text='Добавить', command=add_patient_to_db)
    cancel_button = ttk.Button(button_frame, text='Отменить', command=window.destroy)
    add_button.pack(side=RIGHT)
    cancel_button.pack(side=LEFT)
    button_frame.pack(fill=X, padx=150, pady=15)
    

def view_procedures(values):

    window = Tk()
    window.title("Процедуры")
    window.geometry("1280x500")
    window["bg"] = "white"

    patient_info_frame = Frame(window, bg="white")
    fio_field = Label(patient_info_frame, text=f"ФИО: {values[0]}", font=40, bg="white")
    dob_field = Label(patient_info_frame, text=f"Дата рождения: {values[1]}", font=40, bg="white") 
    address_field = Label(patient_info_frame, text=f"Адрес: {values[2]}", font=40, bg="white")
    patient_info_frame.pack(anchor=W, padx=25, pady=15)
    fio_field.pack(anchor=W)
    dob_field.pack(anchor=W)
    address_field.pack(anchor=W)

    procedure_label = Label(window, text="Процедуры", bg="white", font="Montserrat 20")
    procedure_label.pack(anchor=N)


    procedures_info = []
    name = values[0].split()
    cursor.execute("SELECT tblTreatmentType.txtTreatmentTypeName, "
               "tblTreatmentSet.datDateBegin, "
               "tblTreatmentSet.datDateEnd, "
               "tblTreatmentSet.intTreatmentSetCount, "
               "tblTreatmentSet.intTreatmentSetCountFact, "
               "tblDoctor.txtDoctorName "
               "FROM tblTreatmentType "
               "INNER JOIN tblTreatmentSet ON tblTreatmentType.intTreatmentTypeId = tblTreatmentSet.intTreatmentTypeId "
               "INNER JOIN tblDoctor ON tblTreatmentSet.intDoctorId = tblDoctor.intDoctorId "
               "INNER JOIN tblPatient ON tblTreatmentSet.intPatientId = tblPatient.intPatientId "
               "WHERE tblPatient.txtPatientSurname = ? AND "
               "tblPatient.txtPatientName = ? AND "
               "tblPatient.txtPatientSecondName = ?", 
               (name[0], name[1], name[2]))
    
    rows = cursor.fetchall()
    for row in rows:
        procedures_info.append((row[0].strip(),
                                row[1].strftime("%d.%m.%Y"),
                                row[2].strftime("%d.%m.%Y"),
                                row[3],
                                row[4],
                                row[5].strip()))
        
    add_button = ttk.Button(window, text="Назначение процедуры", command=lambda: add_procedures(values, window))
    add_button.pack(side=BOTTOM, pady=15)

    table = ttk.Treeview(window, columns=("procedure_form", "start_date", "end_date",
                                   "amount_appointed_procedures", "amount_conducted_procedures",
                                     "doctor_name"), show="headings")
    scrollbar = ttk.Scrollbar(window, orient=VERTICAL, command=table.yview)
    table.pack(fill=BOTH, expand=1, side=LEFT)
    scrollbar.pack(side=RIGHT, fill=Y)

    table.heading("procedure_form", text="Вид процедуры", )
    table.heading("start_date", text="Дата начала курса")
    table.heading("end_date", text="Дата окончания курса")
    table.heading("amount_appointed_procedures", text="Количество назначенных процедур")
    table.heading("amount_conducted_procedures", text="Количество проведенных процедур")
    table.heading("doctor_name", text="ФИО доктора")
    
    table.column("#1", anchor=S)
    table.column("#2", anchor=S)
    table.column("#3", anchor=S)
    table.column("#4", anchor=S)
    table.column("#5", anchor=S)
    table.column("#6", anchor=S)

    for procedure in procedures_info:
        table.insert("", END, values=procedure)
 

def add_procedures(values, window2):
    def add_procedure_to_db():
        procedure_rooms = {
            "Общий осмотр": "101",
            "ЭКГ": "102",
            "УЗИ сердца": "103",
            "МРТ головного мозга": "104",
            "Удаление зуба": "105",
            "Обследование на рак кожи": "106",
            "Физиотерапия": "107",
            "Рентгенография": "108",
            "Консультация психиатра": "109",
            "Процедура вправления вывиха": "110"
        }
        info = [procedure_form_box.get(), doctor_box.get(), star_date_entry.get_date(), end_date_entry.get_date(), amount_procedures_counter.get()]
        patient_name = values[0].split()
        cursor.execute("SELECT intPatientId FROM tblPatient WHERE txtPatientSurname = ? AND txtPatientName = ? AND txtPatientSecondName = ?", (patient_name[0], patient_name[1], patient_name[2]))
        patient_id = cursor.fetchone()[0]

        cursor.execute("SELECT intTreatmentTypeId FROM tblTreatmentType WHERE txtTreatmentTypeName = ?", 
                      (info[0]))
        treatment_type_id = cursor.fetchone()[0]
        room = procedure_rooms.get(info[0])

        cursor.execute("SELECT intDoctorId FROM tblDoctor WHERE txtDoctorName = ?", 
                      (info[1]))
        doctor_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO tblTreatmentSet (intPatientId, intTreatmentTypeId, intDoctorId, 
                                       datDateBegin, datDateEnd, intTreatmentSetCount, intTreatmentSetCountFact, txtTreatmentSetRoom)
            VALUES (?, ?, ?, ?, ?, ?, 0, ?)
                       """, (patient_id, treatment_type_id, doctor_id, info[2], info[3], info[4], room))
        connect.commit()
        window.destroy()
        window2.destroy()
        view_procedures(values)


    window = Tk()
    window.title("Назначение процедуры")
    window.geometry("1280x500")
    window["bg"] = "white"

    cursor.execute("SELECT txtTreatmentTypeName FROM tblTreatmentType")
    rows = cursor.fetchall()
    procedures = []
    for row in rows:
        procedures.append(row[0].strip())

    cursor.execute("SELECT txtDoctorName FROM tblDoctor")
    rows = cursor.fetchall()
    doctors = []
    for row in rows:
        doctors.append(row[0].strip())


    add_procedures_label = Label(window, text="Назначение процедуры", bg="white", font="Montserrat 20")
    add_procedures_label.pack(anchor=N)

    patient_info_frame = Frame(window, bg="white")
    name_field = Label(patient_info_frame, text=f"ФИО: {values[0]}", bg="white", font=40)
    dob_field = Label(patient_info_frame, text=f"Дата рождения: {values[1]}", bg="white", font=40)
    patient_info_frame.pack(fill=X, padx=25, pady=10)
    name_field.pack(anchor=W)
    dob_field.pack(anchor=W)

    # Основной фрейм для формы
    form_frame = Frame(window, bg="white")
    form_frame.pack(fill=X, padx=25, pady=10)

    # Вид процедуры
    procedure_frame = Frame(form_frame, bg="white")
    procedure_form_label = Label(procedure_frame, text="Вид процедуры:", bg="white", width=25, anchor="w")
    procedure_form_box = ttk.Combobox(procedure_frame, values=procedures)
    procedure_frame.pack(fill=X, pady=5)
    procedure_form_label.pack(side=LEFT)
    procedure_form_box.pack(side=LEFT, fill=X, expand=True, padx=(10, 0))

    # Доктор
    doctor_frame = Frame(form_frame, bg="white")
    doctor_label = Label(doctor_frame, text="Доктор:", bg="white", width=25, anchor="w")
    doctor_box = ttk.Combobox(doctor_frame, values=doctors)
    doctor_frame.pack(fill=X, pady=5)
    doctor_label.pack(side=LEFT)
    doctor_box.pack(side=LEFT, fill=X, expand=True, padx=(10, 0))

    # Дата начала курса
    start_date_frame = Frame(form_frame, bg="white")
    start_date_label = Label(start_date_frame, text="Дата начала курса:", bg="white", width=25, anchor="w")
    star_date_entry = DateEntry(start_date_frame, date_pattern='dd.MM.yyyy')
    start_date_frame.pack(fill=X, pady=5)
    start_date_label.pack(side=LEFT)
    star_date_entry.pack(side=LEFT, fill=X, expand=True, padx=(10, 0))

    # Дата окончания курса
    end_date_frame = Frame(form_frame, bg="white")
    end_date_label = Label(end_date_frame, text="Дата окончания курса:", bg="white", width=25, anchor="w")
    end_date_entry = DateEntry(end_date_frame, date_pattern='dd.MM.yyyy')
    end_date_frame.pack(fill=X, pady=5)
    end_date_label.pack(side=LEFT)
    end_date_entry.pack(side=LEFT, fill=X, expand=True, padx=(10, 0))

    # Количество процедур
    amount_procedures_frame = Frame(form_frame, bg="white")
    amount_procedures_label = Label(amount_procedures_frame, text="Количество процедур:", bg="white", width=25, anchor="w")
    amount_procedures_counter = ttk.Spinbox(amount_procedures_frame, from_=1, to=100)
    amount_procedures_frame.pack(fill=X, pady=5)
    amount_procedures_label.pack(side=LEFT)
    amount_procedures_counter.pack(side=LEFT, fill=X, expand=True, padx=(10, 0))

    cancel_button = ttk.Button(window, text="Отменить", command=window.destroy)
    cancel_button.pack(side=LEFT, padx=150, pady=15)

    add_button = ttk.Button(window, text="Добавить", command=add_procedure_to_db)
    add_button.pack(side=RIGHT, padx=150, pady=15)


def view_patients():
    root = Tk()
    root.title("Пациенты")
    root.geometry("1280x500")
    root["bg"] = "white"

    root_name_label = Label(root, text="Пациенты", font='Montserrat 20', background="white", pady=15)
    root_name_label.pack()

    # Создаём кнопки добавления и удаления пациентов из таблицы
    add_patinet_btn = ttk.Button(root, text="Добавить пациента", width=20, command=lambda: add_patient(root))
    add_patinet_btn.pack(side=BOTTOM, pady=15)

    patients = []
    cursor.execute("SELECT * FROM tblPatient")
    rows = cursor.fetchall()
    for row in rows:
        patients.append((f"{row[1].strip()} {row[2].strip()} {row[3].strip()}", #ФИО
                        row[4].strftime('%d.%m.%Y'), # ДР
                        row[5].strip()))  # Адрес
            
    table = ttk.Treeview(root, columns=("name", "DOB", "address"), show="headings")
    scrollbar = ttk.Scrollbar(table, orient=VERTICAL, command=table.yview)
    table.pack(fill=BOTH, expand=1, side=LEFT)
    scrollbar.pack(side=RIGHT, fill=Y)

    table.heading("name", text="ФИО", )
    table.heading("DOB", text="Дата рождения")
    table.heading("address", text="Адрес")

    table.column("#1", anchor=S, width= 500, stretch=NO)
    table.column("#2", anchor=S, width=150, stretch=NO)
    table.column("#3", anchor=S)


    for person in patients:
        table.insert("", END, values=person)

    # Добавляем обработку двойного клика
    def on_double_click(event):
        item = table.selection()[0]
        values = table.item(item, "values")
        view_procedures(values)

    table.bind("<Double-1>", on_double_click) 

    root.mainloop()

if __name__ == "__main__":
    view_patients()