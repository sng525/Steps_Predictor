namespace StepsPredictor;

public partial class PredictPage : ContentPage
{
	public PredictPage(UploadedFile file)
	{
		InitializeComponent();
		fileName.Text = file.FileName;
	}
	private async void CleanData_Clicked(object sender, EventArgs e)
	{
		var client = new HttpClient
        {
            Timeout = TimeSpan.FromMinutes(5),
            BaseAddress = new Uri("http://localhost:5140/WalkingData")
        };

		var response = await client.PostAsync("cleanData", null);
		if (response.IsSuccessStatusCode)
		{
			await DisplayAlert("Success", "Successfully cleaned the data.", "OK");
		}
		else
		{
			await DisplayAlert("Error", "Failed to clean the data.", "OK");
		}
	}
}