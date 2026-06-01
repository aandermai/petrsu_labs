CREATE TRIGGER trg_after_delete_treatment_visit  
ON tblTreatmentVisit
AFTER DELETE
AS
BEGIN
    UPDATE tblTreatmentSet 
    SET intTreatmentSetCountFact = intTreatmentSetCountFact - 1
    WHERE intTreatmentSetId IN (SELECT intTreatmentSetId FROM deleted)
END