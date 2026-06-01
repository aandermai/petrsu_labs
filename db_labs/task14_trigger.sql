CREATE TRIGGER trg_prevent_dublicate_procedure_per_day
ON tblTreatmentVisit
AFTER INSERT, UPDATE
AS
BEGIN
    IF EXISTS (
        SELECT 1 
        FROM inserted i
        JOIN tblTreatmentSet ts ON ts.intTreatmentSetId = i.intTreatmentSetId
        JOIN tblTreatmentVisit tv ON tv.intTreatmentSetId = ts.intTreatmentSetId
        WHERE tv.datTreatmentVisitDate = i.datTreatmentVisitDate
        AND tv.intTreatmentVisitId != i.intTreatmentVisitId
    )
    BEGIN
        RAISERROR('У пациента уже есть процедура на этот день', 16, 1)
        ROLLBACK TRANSACTION
    END
END