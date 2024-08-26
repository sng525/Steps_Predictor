using System.Net.Http.Headers;

namespace StepsPredictor;

public partial class MainPage : ContentPage
{
    public MainPage()
    {
        InitializeComponent();
    }

    private async void UploadData_Clicked(object sender, EventArgs e)
    {
        PickOptions options = new PickOptions()
        {
            PickerTitle = "Please select your previous steps data."
        };
        var result = await FilePicker.PickAsync(options);

        if (result == null)
            return;
        else
        {
            var file = await ProcessFile(result);
            if (file)
            {
                await DisplayAlert(
                    "File uploaded successfully",
                    "The file has been uploaded successfully",
                    "OK"
                );
            }
            else
            {
                await DisplayAlert(
                    "An error occurred",
                    "An error occurred while uploading the file",
                    "OK"
                );
            }
            var uploadedFile = new UploadedFile(result.FileName);
            await Navigation.PushAsync(new PredictPage(uploadedFile));
        }
    }

    private static async Task<bool> ProcessFile(FileResult fileResult)
    {
        if (fileResult == null)
            return false;

        try
        {
            using var fileStream = File.OpenRead(fileResult.FullPath);

            byte[] bytes;

            using (var memoryStream = new MemoryStream())
            {
                await fileStream.CopyToAsync(memoryStream);
                bytes = memoryStream.ToArray();
            }

            using var fileContent = new ByteArrayContent(bytes);
            fileContent.Headers.ContentType = MediaTypeHeaderValue.Parse("multipart/form-data");

            using var form = new MultipartFormDataContent
            {
                { fileContent, "fileContent", Path.GetFileName(fileResult.FullPath) }
            };

            return await UploadFile(form);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An unexpected error occurred: {ex.Message}");
            return false;
        }
    }

    public static async Task<bool> UploadFile(MultipartFormDataContent form)
    {
        if (Connectivity.Current.NetworkAccess != NetworkAccess.Internet)
        {
            return false;
        }

        var client = new HttpClient
        {
            Timeout = TimeSpan.FromMinutes(5),
            BaseAddress = new Uri("http://localhost:5140/WalkingData")
        };

        try
        {
            var response = await client.PostAsync("uploadFile", form);
            response.EnsureSuccessStatusCode();
            return true;
        }
        catch
        {
            return false;
        }
    }
}
