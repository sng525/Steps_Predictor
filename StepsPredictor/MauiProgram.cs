﻿namespace StepsPredictor;
using CommunityToolkit.Maui;
using CommunityToolkit.Maui.Storage;
using Microsoft.Maui.Hosting;
using Microsoft.Extensions.DependencyInjection;


public static class MauiProgram
{
	public static MauiApp CreateMauiApp()
	{
		var builder = MauiApp.CreateBuilder();
		builder
			.UseMauiApp<App>()
			.UseMauiCommunityToolkit()
			.ConfigureFonts(fonts =>
			{
				fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
				fonts.AddFont("OpenSans-Semibold.ttf", "OpenSansSemibold");
			});
			
		builder.Services.AddSingleton(FolderPicker.Default);

		return builder.Build();
	}
}
