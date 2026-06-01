import pyodbc
from fpdf import FPDF
from datetime import datetime
import webbrowser
import os

connect = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=192.168.112.103; DATABASE=db22203; UID=User013; PWD=User013@!71')
cursor = connect.cursor()

def do_doctor_report(doctor_id):
        class PDF(FPDF):
            def header(self):
                # Добавляем шрифты
                self.add_font("Roboto", style="", fname="Roboto/static/Roboto-Regular.ttf", uni=True)
                self.add_font("Roboto", style="B", fname="Roboto/static/Roboto-Bold.ttf", uni=True)
                
                # Заголовок отчета
                self.set_font("Roboto", style="B", size=16)
                self.cell(0, 10, "Отчет: Доктор", align="C", ln=True)
                self.ln(5)

            def footer(self):
                self.set_y(-15)
                self.set_font("Roboto", size=8)
                self.cell(0, 10, f"{self.page_no()}", align="C")

        # SQL запрос для получения информации о докторе
        doctor_info_query = """
        SELECT 
            RTRIM(txtDoctorName) AS [ФИО],
            RTRIM(txtSpecialist) AS [Специальность],
            CONVERT(VARCHAR, datDoctorWork, 104) AS [Дата приема]
        FROM tblDoctor
        WHERE intDoctorId = ?;
        """

        cursor.execute(doctor_info_query, doctor_id)
        doctor_info = cursor.fetchone()

        # SQL запрос для получения курсов процедур доктора
        procedures_query = """
        SELECT 
            RTRIM(p.txtPatientSurname) + ' ' + 
            RTRIM(p.txtPatientName) + ' ' + 
            RTRIM(p.txtPatientSecondName) AS [ФИО пациента],
            RTRIM(tt.txtTreatmentTypeName) AS [Вид процедуры],
            CONVERT(VARCHAR, ts.datDateBegin, 104) AS [Дата начала],
            CONVERT(VARCHAR, ts.datDateEnd, 104) AS [Дата окончания]
        FROM tblTreatmentSet ts
        JOIN tblPatient p ON ts.intPatientId = p.intPatientId
        JOIN tblTreatmentType tt ON ts.intTreatmentTypeId = tt.intTreatmentTypeId
        WHERE ts.intDoctorId = ?
        ORDER BY [ФИО пациента];
        """

        cursor.execute(procedures_query, doctor_id)
        procedures = cursor.fetchall()

        # Создаем PDF документ
        pdf = PDF()
        pdf.add_page()

        # Добавляем шрифты
        pdf.add_font("Roboto", style="", fname="Roboto/static/Roboto-Regular.ttf", uni=True)
        pdf.add_font("Roboto", style="B", fname="Roboto/static/Roboto-Bold.ttf", uni=True)

        # Информация о докторе
        pdf.set_font("Roboto", style="B", size=14)
        pdf.cell(0, 10, f"Доктор: {doctor_info[0]}", ln=True)
        pdf.set_font("Roboto", size=12)
        pdf.cell(0, 8, f"Специальность: {doctor_info[1]}", ln=True)
        pdf.cell(0, 8, f"Дата приема на работу: {doctor_info[2]}", ln=True)
        pdf.ln(10)

        # Курсы процедур
        if procedures:
            pdf.set_font("Roboto", style="B", size=12)
            pdf.cell(0, 10, "Назначенные курсы процедур:", ln=True)
            
            # Заголовки таблицы
            pdf.set_fill_color(200, 200, 200)
            pdf.cell(70, 8, "ФИО пациента", border=1, fill=True)
            pdf.cell(50, 8, "Вид процедуры", border=1, fill=True)
            pdf.cell(30, 8, "Дата начала", border=1, fill=True)
            pdf.cell(40, 8, "Дата окончания", border=1, fill=True, ln=True)
            
            # Данные процедур
            pdf.set_fill_color(255, 255, 255)
            pdf.set_font("Roboto", size=8)
            for procedure in procedures:
                if pdf.get_y() > 250:
                    pdf.add_page()
                
                pdf.cell(70, 8, str(procedure[0]), border=1)
                pdf.cell(50, 8, str(procedure[1]), border=1)
                pdf.cell(30, 8, str(procedure[2]), border=1)
                pdf.cell(40, 8, str(procedure[3]), border=1, ln=True)
            
            pdf.ln(5)
        else:
            pdf.set_font("Roboto", size=12)
            pdf.cell(0, 10, "Нет назначенных курсов процедур", ln=True)

        # Итог
        pdf.set_font("Roboto", style="B", size=12)
        pdf.cell(0, 10, f"Всего курсов процедур: {len(procedures)}", ln=True)
        pdf.ln(10)

        current_dir = os.getcwd()
        pdf_path = os.path.join(current_dir, "Доктор.pdf")
        pdf.output("Доктор.pdf")

        webbrowser.open(pdf_path)