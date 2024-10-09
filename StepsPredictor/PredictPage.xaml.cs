using System.Text.Json;

namespace StepsPredictor;

public partial class PredictPage : ContentPage
{
	private static readonly HttpClient _client = new HttpClient();

	public PredictPage(UploadedFile file)
	{
		InitializeComponent();
		fileName.Text = file.FileName;
	}
	private async void Predict_Clicked(object sender, EventArgs e)
	{
		fileName.Text = "";
		string url = "http://localhost:5004/predict";

		var response = await _client.GetAsync(url);

		if (response.IsSuccessStatusCode)
		{
			var resultData = await response.Content.ReadAsStringAsync();

			using (JsonDocument jdoc = JsonDocument.Parse(resultData))
			{
				// Access the prediction value
				if (jdoc.RootElement.TryGetProperty("prediction", out JsonElement predictionElement))
				{
					int predictionValue = predictionElement.GetInt32();
					lblResult.Text = $"Today's Steps Prediction: {predictionValue}";
				}
				else
				{
					lblResult.Text = "Prediction not found in the response.";
				}
			}
		}
		else
		{
			lblResult.Text = "Error: Unable to get prediction.";
		}

		/* var client = new HttpClient
        {
            Timeout = TimeSpan.FromMinutes(5),
            BaseAddress = new Uri("http://localhost:5140/")
        };

		var response = await client.PostAsync("WalkingData/cleanData", null);
		if (response.IsSuccessStatusCode)
		{
			await DisplayAlert("Success", "Successfully cleaned the data.", "OK");
		}
		else
		{
			await DisplayAlert("Error", "Failed to clean the data.", "OK");
		} */
	}
}