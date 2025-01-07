using System.Linq.Expressions;
using System.Net;
using System.Net.Http.Headers;
using Microsoft.ML.OnnxRuntime.Tensors;
using Microsoft.ML.OnnxRuntime;
using Windows.Globalization.PhoneNumberFormatting;
using Windows.Devices.Printers;



namespace mobile_application;

public partial class MainPage : ContentPage
{

	//Model 
	//private List<string> _classNames { get; s
	public MainPage()
	{
		InitializeComponent();

	}
		public async void onTrainBtnClicked(object sender, EventArgs e)
		{
			var http_client = new HttpClient();

			try
			{
				var flask_url = "http://127.0.0.1:5000/get-file/export.xml";
				var response = await http_client.GetAsync(flask_url);
				Console.WriteLine("failed to connect");
				if (response.IsSuccessStatusCode)
				{
					var file_data = await response.Content.ReadAsByteArrayAsync();

					string file_name = "model.onnx";
					string file_path = Path.Combine("mobile_application/files", file_name);

					await File.WriteAllBytesAsync(file_path, file_data);

					await DisplayAlert("Success", $"file saved to: {file_path}", "OK");
				} 

				else
				{
					await DisplayAlert("Error", "failed to retrieve file", "OK");
				}
				
			}			
			
			catch (Exception ex)			{
				await DisplayAlert("Exception", $"an error occurred: {ex.Message}", "OK");
			
			}
		}

		// if train button clicked:
		// check if file exists in dir
		// if file does not exist, error message
		// if file exists, trigger ml_model project which will train and save an onnx model 
	



	//if predict button clicked:
	//check if file exists in given directory
	//if file does not exist return error message
	//if file exists, run the file through the model, which is in onnx format 
	//display result


	// private InferenceSession LoadModel()
	// {
	// 	using var modelStream = FileSystem.OpenAppPackageFileAsync("rf_iris.onnx").Result;

	// 	using var modelMemoryStream = new MemoryStream();
	// 	modelStream.CopyTo(modelMemoryStream);

	// 	var modelBytes = modelMemoryStream.ToArray();
	// 	InferenceSession inferenceSession = new InferenceSession(model: modelBytes);

	// 	return inferenceSession;

	// }

	// private string Predict(float[] inputData)
	// {	
	// 	// creates an array from the new input in a specified shape and length
	// 	var inputTensor = new DenseTensor<float>(inputData, new int[] { 1, inputData.Length});

	// 	// names input data to correspond with onnx input node
	// 	var input = NamedOnnxValue.CreateFromTensor("X", inputTensor);

	// 	// runs loaded model on new input
	// 	using IDisposableReadOnlyCollection<DisposableNamedOnnxValue> results = _inferenceSession.Run(new[]{input});

	// 	//retrieves first output of the onnx model in to a float array
	// 	var prediction = results.First().AsEnumerable<float>().ToArray();

	// 	int predictedClassIndex = Array.IndexOf(prediction, prediction.Max());

	// 	string[] classes = new[]{ "Iris setosa", "Iris versicolor", "Iris virginica" };

	// 	string predictedClass = classes[predictedClassIndex];

	// 	return predictedClass;
	// }

	// private List<string> LoadLabels()
	// {
	// 	// this should simply return a list of the labels
	// 	// in this case, ham or spam
	// }



	//App
	
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
