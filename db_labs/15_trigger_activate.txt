-- Смотрим исходные данные
SELECT * FROM tblTreatmentSet WHERE intTreatmentSetId = 1

-- Добавляем процедуру (триггер увеличит счетчик на 1)
INSERT INTO tblTreatmentVisit (intTreatmentSetId, datTreatmentVisitDate)
VALUES (1, '2025-03-02')

-- Проверяем, что счетчик увеличился
SELECT * FROM tblTreatmentSet WHERE intTreatmentSetId = 1

-- Удаляем процедуру (триггер уменьшит счетчик на 1)
DELETE FROM tblTreatmentVisit 
WHERE intTreatmentSetId = 1 AND datTreatmentVisitDate = '2025-03-02'

-- Проверяем, что счетчик уменьшился
SELECT * FROM tblTreatmentSet WHERE intTreatmentSetId = 1