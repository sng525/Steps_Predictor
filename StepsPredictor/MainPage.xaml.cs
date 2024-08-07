namespace StepsPredictor;

public partial class MainPage : ContentPage
{
    public MainPage()
    {
        InitializeComponent();
    }

    private async void UploadData_Clicked(object sender, EventArgs e)
    {
        var result = await FilePicker.PickAsync(new PickOptions {});
        if (result == null)
            return;

        fileName.Text = result.FileName;

    }
}
a