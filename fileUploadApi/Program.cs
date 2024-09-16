using Microsoft.AspNetCore.Server.Kestrel.Core;

var builder = WebApplication.CreateBuilder(args);

// resolves https redirection error
builder.WebHost.ConfigureKestrel(options =>
{
    options.ListenLocalhost(5170); // HTTP
    // options.ListenLocalhost(7035, listenOptions => // https 
    // {
    //     listenOptions.UseHttps();
    // });

    // resolves timeout error
    options.Limits.MinRequestBodyDataRate = new MinDataRate(100, TimeSpan.FromSeconds(10));
    options.Limits.MaxRequestBodySize = 100 * 1024 * 1024; // 100 MB
    options.Limits.RequestHeadersTimeout = TimeSpan.FromMinutes(2);
});

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

//app.UseHttpsRedirection();

app.MapPost("/uploadfile", async (HttpRequest httpRequest) =>
{
    if (!httpRequest.HasFormContentType)
    {
        app.Logger.LogError("Invalid content type: {ContentType}", httpRequest.ContentType);
        return Results.BadRequest("Invalid content type.");
    }

    try
    {
        var formCollection = await httpRequest.ReadFormAsync();
        var iFormFile = formCollection.Files["fileContent"];

        if (iFormFile is null || iFormFile.Length == 0)
        {
            app.Logger.LogError("No file content found.");
            return Results.BadRequest("No file content found.");
        }

        var localFilePath = Path.Combine("Files", iFormFile.FileName);
        await using var stream = iFormFile.OpenReadStream();
        await using var localFileStream = File.OpenWrite(localFilePath);

        await stream.CopyToAsync(localFileStream);

        return Results.NoContent();
    }
    catch (Exception ex)
    {
        app.Logger.LogError(ex, "An error occurred while processing the file upload.");
        return Results.BadRequest("An error occurred while processing the file upload.");
    }
})

.Produces(StatusCodes.Status201Created)
.WithName("UploadFile")
.WithOpenApi();

//Server

var filesDirectory = Path.Combine(Directory.GetCurrentDirectory(), "Files");

app.MapGet("/Files", async (string fileName) =>
{
    var filePath = Path.Combine(filesDirectory, fileName);

    if(!File.Exists(filePath))
    {
        return Results.NotFound("File not found.");
    }

    var fileStream = new FileStream(filePath, FileMode.Open, FileAccess.Read);
    var contentType = "application/octet-stream";

    return Results.File(fileStream, contentType, fileName);
})
.Produces(StatusCodes.Status200OK)
.Produces(StatusCodes.Status404NotFound)
.WithName("GetFile")
.WithOpenApi();

app.Run();
