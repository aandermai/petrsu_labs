import pyodbc
from fpdf import FPDF
from datetime import datetime
import webbrowser
import os

def do_cabinet_work_report():
    class PDF(FPDF):
        def header(self):
            # Добавляем шрифты
            self.add_font("Roboto", style="", fname="Roboto/static/Roboto-Regular.ttf", uni=True)
            self.add_font("Roboto", style="B", fname="Roboto/static/Roboto-Bold.ttf", uni=True)
            
            # Заголовок отчета
            self.set_font("Roboto", style="B", size=16)
            self.cell(0, 10, "Отчет: Работа кабинетов", align="C", ln=True)
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

    # SQL запрос для получения данных
    sql_query = """
    SELECT 
        RTRIM(ts.txtTreatmentSetRoom) AS [Кабинет],
        CONVERT(VARCHAR, tv.datTreatmentVisitDate, 104) AS [Дата процедуры],
        RTRIM(p.txtPatientSurname) + ' ' + 
        RTRIM(p.txtPatientName) + ' ' + 
        RTRIM(p.txtPatientSecondName) AS [ФИО пациента],
        RTRIM(tt.txtTreatmentTypeName) AS [Вид процедуры],
        COUNT(*) OVER (PARTITION BY ts.txtTreatmentSetRoom) AS [Всего процедур в кабинете]
    FROM tblTreatmentVisit tv
    JOIN tblTreatmentSet ts ON tv.intTreatmentSetId = ts.intTreatmentSetId
    JOIN tblPatient p ON ts.intPatientId = p.intPatientId
    JOIN tblTreatmentType tt ON ts.intTreatmentTypeId = tt.intTreatmentTypeId
    ORDER BY ts.txtTreatmentSetRoom, tv.datTreatmentVisitDate;
    """

    cursor.execute(sql_query)
    rows = cursor.fetchall()

    # Создаем PDF документ
    pdf = PDF()
    pdf.add_page()

    # Добавляем шрифты
    pdf.add_font("Roboto", style="", fname="Roboto/static/Roboto-Regular.ttf", uni=True)
    pdf.add_font("Roboto", style="B", fname="Roboto/static/Roboto-Bold.ttf", uni=True)

    # Группируем данные по кабинетам
    cabinet_data = {}
    cabinet_procedures = {}

    for row in rows:
        cabinet, date, patient, procedure, total = row
        if cabinet not in cabinet_data:
            cabinet_data[cabinet] = []
            cabinet_procedures[cabinet] = 0
        cabinet_data[cabinet].append((date, patient, procedure))
        cabinet_procedures[cabinet] = total  

    # Устанавливаем начальные параметры
    pdf.set_font("Roboto", size=12)

    # Создаем отчет для каждого кабинета
    for cabinet, procedures in cabinet_data.items():
        # Заголовок кабинета
        pdf.set_font("Roboto", style="B", size=14)
        pdf.cell(0, 10, f"Кабинет: {cabinet}", ln=True)
        pdf.ln(2)
        
        # Таблица процедур
        pdf.set_font("Roboto", size=10)
        
        # Заголовки таблицы
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(30, 8, "Дата", border=1, fill=True)
        pdf.cell(70, 8, "ФИО пациента", border=1, fill=True)
        pdf.cell(70, 8, "Вид процедуры", border=1, fill=True, ln=True)
        
        # Данные процедур
        pdf.set_fill_color(255, 255, 255)
        for date, patient, procedure in procedures:
            # Переносим на новую страницу если нужно
            if pdf.get_y() > 250:
                pdf.add_page()
            
            pdf.cell(30, 8, str(date), border=1)
            pdf.cell(70, 8, str(patient), border=1)
            pdf.cell(70, 8, str(procedure), border=1, ln=True)
        
        # Итог по кабинету
        pdf.set_font("Roboto", style="B", size=11)
        pdf.cell(0, 10, f"Всего процедур в кабинете: {cabinet_procedures[cabinet]}", ln=True)
        pdf.ln(5)
        
        # Добавляем разрыв между кабинетами
        if pdf.get_y() > 220:
            pdf.add_page()
        else:
            pdf.ln(5)


    current_dir = os.getcwd()
    pdf_path = os.path.join(current_dir, "Пациенты.pdf")
    pdf.output("Пациенты.pdf")
    pdf.output("Работа кабинетов.pdf")
    webbrowser.open(pdf_path)

