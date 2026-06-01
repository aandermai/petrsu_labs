CREATE OR ALTER PROCEDURE CreateDoctorReportTempTable
    @DoctorId INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Создаем временную таблицу
    CREATE TABLE #DoctorReport (
        DoctorId INT,
        DoctorFullName NVARCHAR(255),
        DoctorSpeciality NVARCHAR(100),
        EmploymentDate DATE,
        PatientFullName NVARCHAR(255),
        TreatmentTypeName NVARCHAR(100),
        StartDate DATE,
        EndDate DATE,
        CreatedDateTime DATETIME DEFAULT GETDATE()
    );
    
    INSERT INTO #DoctorReport (
        DoctorId, 
        DoctorFullName, 
        DoctorSpeciality, 
        EmploymentDate, 
        PatientFullName, 
        TreatmentTypeName, 
        StartDate, 
        EndDate
    )
    SELECT 
        d.intDoctorId,
        RTRIM(d.txtDoctorName) AS DoctorFullName,
        RTRIM(d.txtSpecialist) AS DoctorSpeciality,
        d.datDoctorWork AS EmploymentDate,
        RTRIM(p.txtPatientSurname) + ' ' + 
        RTRIM(p.txtPatientName) + ' ' + 
        RTRIM(p.txtPatientSecondName) AS PatientFullName,
        RTRIM(tt.txtTreatmentTypeName) AS TreatmentTypeName,
        ts.datDateBegin AS StartDate,
        ts.datDateEnd AS EndDate
    FROM tblDoctor d
    JOIN tblTreatmentSet ts ON d.intDoctorId = ts.intDoctorId
    JOIN tblPatient p ON ts.intPatientId = p.intPatientId
    JOIN tblTreatmentType tt ON ts.intTreatmentTypeId = tt.intTreatmentTypeId
    WHERE d.intDoctorId = @DoctorId
    ORDER BY PatientFullName;

    SELECT * FROM #DoctorReport ORDER BY PatientFullName;
    
    PRINT 'Временная таблица #DoctorReport создана и заполнена данными для доктора ID: ' + CAST(@DoctorId AS NVARCHAR(10));
END;