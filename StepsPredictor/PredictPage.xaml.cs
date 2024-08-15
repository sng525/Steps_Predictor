namespace StepsPredictor;

public partial class PredictPage : ContentPage
{
	public PredictPage(UploadedFile file)
	{
		InitializeComponent();
		fileName.Text = file.FileName;
	}
	private async void PredictSteps_Clicked(object sender, EventArgs e){
		
	}
}