CREATE TRIGGER trg_after_insert_treatment_visit
ON tblTreatmentVisit
AFTER INSERT
AS
BEGIN
    UPDATE tblTreatmentSet 
    SET intTreatmentSetCountFact = intTreatmentSetCountFact + 1
    WHERE intTreatmentSetId IN (SELECT intTreatmentSetId FROM inserted)
END
