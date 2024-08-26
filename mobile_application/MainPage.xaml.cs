using System.Linq.Expressions;
using System.Net;
using System.Net.Http.Headers;


namespace mobile_application;

public partial class MainPage : ContentPage
{
	public MainPage()
	{
		InitializeComponent();
	}

	//https://www.youtube.com/watch?v=FGmVIJkTq_Y&t=419s
	
	private async void onFilePickerClicked(object sender, EventArgs e) {
		try{
			PickOptions options = new PickOptions(){
				PickerTitle = "Please select your file",
			};

			var fileResult = await FilePicker.PickAsync(options);

			if (fileResult != null){

				var result = await ProcessFile(fileResult);
			
				if(result)
					await DisplayAlert("File Uploaded Successfully.", 
					"The file has been uploaded successfully", 
					"ok");

				else 
					Console.WriteLine("File picking was canceled or failed.");
					await DisplayAlert("An error has occurred.", 
					"The file has not been uploaded", 
					"ok");		
			}
		}			
			catch{
				// user cancelled or something went wrong
	}
}

private static async Task<bool> ProcessFile(FileResult fileResult)
{
    if (fileResult == null)
    {
        Console.WriteLine("Error: FileResult is null.");
        return false;
    }

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
    catch (FileNotFoundException ex)
    {
        Console.WriteLine($"Error: File not found. {ex.Message}");
        return false;
    }
    catch (IOException ex)
    {
        Console.WriteLine($"Error: IO exception occurred while processing the file. {ex.Message}");
        return false;
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Error: An unexpected error occurred. {ex.Message}");
        return false;
    }
}

	public static async Task<bool> UploadFile(MultipartFormDataContent form){

		if(Connectivity.Current.NetworkAccess != NetworkAccess.Internet){
			return false;
		}
		
		var client = new HttpClient{
			Timeout = TimeSpan.FromMinutes(5),
			BaseAddress = new Uri("http://localhost:5170/")
		};

		try{
			var response = await client.PostAsync("uploadFile", form);
			response.EnsureSuccessStatusCode();

			return true;
		}
		catch(Exception ex){
			return false;
		}
	}
}
