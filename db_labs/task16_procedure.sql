CREATE OR ALTER PROCEDURE sp_doctor_patient_count AS
BEGIN
	SET NOCOUNT ON;

	CREATE TABLE #DoctorPatientCount (DoctorFullName NVARCHAR(100), PatientCount INT);

	INSERT INTO #DoctorPatientCount (DoctorFullName, PatientCount)
	SELECT tblDoctor.txtDoctorName, COUNT(DISTINCT tblTreatmentSet.intPatientId)
	FROM tblDoctor
	LEFT JOIN tblTreatmentSet ON tblDoctor.intDoctorId = tblTreatmentSet.intDoctorId
	GROUP BY tblDoctor.txtDoctorName;

	SELECT * FROM #DoctorPatientCount;
END;