using System;

namespace StepsPredictor;

public class UploadedFile
{
    public string FileName { get; set; }
    public UploadedFile(string fileName)
    {
        FileName = fileName;
    }
}
