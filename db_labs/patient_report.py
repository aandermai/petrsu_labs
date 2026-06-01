import pyodbc
from fpdf import FPDF
from datetime import datetime
import webbrowser
import os

def do_patients_report():
    class PDF(FPDF):
        def header(self):
            # Добавляем шрифты
            self.add_font("Roboto", style="", fname="Roboto/static/Roboto-Regular.ttf", uni=True)
            self.add_font("Roboto", style="B", fname="Roboto/static/Roboto-Bold.ttf", uni=True)
            
            # Заголовок отчета
            self.set_font("Roboto", style="B", size=16)
            self.cell(0, 10, "Отчет: Пациенты", align="C", ln=True)
            self.ln(5)
            

        def footer(self):
            self.set_y(-15)
            self.set_font("Roboto", size=8)
            self.cell(0, 10, f"{self.page_no()}", align="C")

    # Подключаемся к базе данных
    connect = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=192.168.112.103;'
        'DATABASE=db22203;'
        'UID=User013;'
        'PWD=User013@!71'
    )
    cursor = connect.cursor()

    # SQL запрос для получения данных пациентов
    sql_query = """
    SELECT 
        p.intPatientId,
        RTRIM(p.txtPatientSurname) + ' ' + 
        RTRIM(p.txtPatientName) + ' ' + 
        RTRIM(p.txtPatientSecondName) AS [ФИО],
        CONVERT(VARCHAR, p.datBirthday, 104) AS [Дата рождения],
        RTRIM(p.txtAdress) AS [Адрес],
        -- Статистика по процедурам
        (SELECT COUNT(*) FROM tblTreatmentVisit tv 
         JOIN tblTreatmentSet ts ON tv.intTreatmentSetId = ts.intTreatmentSetId 
         WHERE ts.intPatientId = p.intPatientId) AS [Всего проведенных процедур]
    FROM tblPatient p
    ORDER BY [ФИО];
    """

    cursor.execute(sql_query)
    patients = cursor.fetchall()

    # SQL запрос для получения процедур пациентов
    procedures_query = """
    SELECT 
        ts.intPatientId,
        RTRIM(tt.txtTreatmentTypeName) AS [Вид процедуры],
        CONVERT(VARCHAR, ts.datDateBegin, 104) AS [Дата начала],
        CONVERT(VARCHAR, ts.datDateEnd, 104) AS [Дата окончания],
        ts.intTreatmentSetCount AS [Назначено процедур],
        ts.intTreatmentSetCountFact AS [Проведено процедур],
        (ts.intTreatmentSetCount - ts.intTreatmentSetCountFact) AS [Осталось процедур],
        RTRIM(ts.txtTreatmentSetRoom) AS [Кабинет],
        ts.intTreatmentSetId
    FROM tblTreatmentSet ts
    JOIN tblTreatmentType tt ON ts.intTreatmentTypeId = tt.intTreatmentTypeId
    ORDER BY ts.intPatientId, ts.datDateBegin;
    """

    cursor.execute(procedures_query)
    procedures = cursor.fetchall()

    # SQL запрос для получения проведенных процедур
    visits_query = """
    SELECT 
        ts.intPatientId,
        ts.intTreatmentSetId,
        CONVERT(VARCHAR, tv.datTreatmentVisitDate, 104) AS [Дата проведения],
        RTRIM(tt.txtTreatmentTypeName) AS [Вид процедуры]
    FROM tblTreatmentVisit tv
    JOIN tblTreatmentSet ts ON tv.intTreatmentSetId = ts.intTreatmentSetId
    JOIN tblTreatmentType tt ON ts.intTreatmentTypeId = tt.intTreatmentTypeId
    ORDER BY ts.intPatientId, tv.datTreatmentVisitDate;
    """

    cursor.execute(visits_query)
    visits = cursor.fetchall()

    # Группируем данные
    patient_data = {}
    for patient in patients:
        patient_id, fio, birth_date, address, total_procedures = patient
        patient_data[patient_id] = {
            'fio': fio,
            'birth_date': birth_date,
            'address': address,
            'total_procedures': total_procedures,
            'treatments': [],
            'visits': []
        }

    # Группируем процедуры по пациентам
    for procedure in procedures:
        patient_id, treatment_type, start_date, end_date, planned_count, done_count, remaining, room, treatment_id = procedure
        if patient_id in patient_data:
            patient_data[patient_id]['treatments'].append({
                'type': treatment_type,
                'start_date': start_date,
                'end_date': end_date,
                'planned_count': planned_count,
                'done_count': done_count,
                'remaining': remaining,
                'room': room,
                'treatment_id': treatment_id
            })

    # Группируем проведенные процедуры по пациентам
    for visit in visits:
        patient_id, treatment_id, visit_date, treatment_type = visit
        if patient_id in patient_data:
            patient_data[patient_id]['visits'].append({
                'treatment_id': treatment_id,
                'date': visit_date,
                'type': treatment_type
            })

    # Создаем PDF документ
    pdf = PDF()
    pdf.add_page()

    # Добавляем шрифты
    pdf.add_font("Roboto", style="", fname="Roboto/static/Roboto-Regular.ttf", uni=True)
    pdf.add_font("Roboto", style="B", fname="Roboto/static/Roboto-Bold.ttf", uni=True)

    # Устанавливаем начальные параметры
    pdf.set_font("Roboto", size=12)

    # Создаем отчет для каждого пациента
    for patient_id, data in patient_data.items():
        # Информация о пациенте
        pdf.set_font("Roboto", style="B", size=14)
        pdf.cell(0, 10, f"Пациент: {data['fio']}", ln=True)
        pdf.set_font("Roboto", size=10)
        pdf.cell(0, 8, f"Дата рождения: {data['birth_date']}", ln=True)
        pdf.cell(0, 8, f"Адрес: {data['address']}", ln=True)
        pdf.ln(5)

        # Назначенные процедуры
        if data['treatments']:
            pdf.set_font("Roboto", style="B", size=12)
            pdf.cell(0, 10, "Назначенные процедуры:", ln=True)
            
            # Заголовки таблицы процедур
            pdf.set_fill_color(200, 200, 200)
            pdf.cell(50, 8, "Вид процедуры", border=1, fill=True)
            pdf.cell(22, 8, "Начало", border=1, fill=True)
            pdf.cell(25, 8, "Окончание", border=1, fill=True)
            pdf.cell(25, 8, "Назначено", border=1, fill=True)
            pdf.cell(25, 8, "Проведено", border=1, fill=True)
            pdf.cell(22, 8, "Осталось", border=1, fill=True)
            pdf.cell(20, 8, "Кабинет", border=1, fill=True, ln=True)
            
            # Данные процедур
            pdf.set_fill_color(255, 255, 255)
            pdf.set_font("Roboto", size=8)
            for treatment in data['treatments']:
                if pdf.get_y() > 250:
                    pdf.add_page()
                
                pdf.cell(50, 8, str(treatment['type']), border=1)
                pdf.cell(22, 8, str(treatment['start_date']), border=1)
                pdf.cell(25, 8, str(treatment['end_date']), border=1)
                pdf.cell(25, 8, str(treatment['planned_count']), border=1)
                pdf.cell(25, 8, str(treatment['done_count']), border=1)
                pdf.cell(22, 8, str(treatment['remaining']), border=1)
                pdf.cell(20, 8, str(treatment['room']), border=1, ln=True)
            
            pdf.ln(5)

        # Проведенные процедуры
        if data['visits']:
            pdf.set_font("Roboto", style="B", size=12)
            pdf.cell(0, 10, "Проведенные процедуры:", ln=True)
            
            # Заголовки таблицы посещений
            pdf.set_fill_color(200, 200, 200)
            pdf.cell(50, 8, "Дата проведения", border=1, fill=True)
            pdf.cell(60, 8, "Вид процедуры", border=1, fill=True, ln=True)
            
            # Данные посещений
            pdf.set_fill_color(255, 255, 255)
            pdf.set_font("Roboto", size=8)
            for visit in data['visits']:
                if pdf.get_y() > 250:
                    pdf.add_page()
                
                pdf.cell(50, 8, str(visit['date']), border=1)
                pdf.cell(60, 8, str(visit['type']), border=1, ln=True)
            
            pdf.ln(5)

        # Итог по пациенту
        pdf.set_font("Roboto", style="B", size=11)
        pdf.cell(0, 10, f"Всего проведенных процедур: {data['total_procedures']}", ln=True)
        pdf.ln(10)
        
        # Добавляем разрыв между пациентами
        if pdf.get_y() > 200:
            pdf.add_page()
        else:
            pdf.ln(5)

    current_dir = os.getcwd()
    pdf_path = os.path.join(current_dir, "Пациенты.pdf")
    pdf.output("Пациенты.pdf")


    webbrowser.open(pdf_path)
