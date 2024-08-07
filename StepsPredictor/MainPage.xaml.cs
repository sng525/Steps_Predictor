namespace StepsPredictor;
using System.Text;
using CommunityToolkit.Maui.Alerts;
using CommunityToolkit.Maui.Core;
using CommunityToolkit.Maui.Storage;

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
