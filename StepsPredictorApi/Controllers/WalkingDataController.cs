using Microsoft.AspNetCore.Mvc;
using System.Text;
using System.Text.Json;

[ApiController]
[Route("[controller]")]
public class WalkingDataController : ControllerBase
{
    private readonly HttpClient _client;
    private readonly ILogger<WalkingDataController> _logger;
    public WalkingDataController(HttpClient client, ILogger<WalkingDataController> logger)
    {
        _client = client;
        _logger = logger;
    }

    [HttpPost("cleanData")]
    public async Task<IActionResult> CleanWalkingData()
    {
        // Get the raw data directory
        var rawDataDirectory = Path.Combine(Directory.GetCurrentDirectory(), "Files");

        if (rawDataDirectory == null)
        {
            return StatusCode(404, "No data file found.");
        }

        // Get all the files in the directory
        var filePaths = Directory.GetFiles(rawDataDirectory);

        if (filePaths.Length > 0)
        {
            var firstFilePath = filePaths[0];  // first file
            var rawData = await System.IO.File.ReadAllTextAsync(firstFilePath);

            // var jsonData = JsonSerializer.Serialize(rawData);

            var content = new StringContent(rawData, Encoding.UTF8, "application/json");
            var response = await _client.PostAsync("http://localhost:5004/clean-data", content);

            if (response.IsSuccessStatusCode)
            {
                var cleanedData = await response.Content.ReadAsStringAsync();
                var storagePath = Path.Combine(Directory.GetCurrentDirectory(), "CleanedFile");
                if (!Directory.Exists(storagePath))
                {
                    Directory.CreateDirectory(storagePath);
                }

                var fileName = "cleaned_file.json";
                var filePath = Path.Combine(storagePath, fileName);
                await System.IO.File.WriteAllTextAsync(filePath, cleanedData);

                return Ok(new { message = "Cleaned data stored successfully." });
            }
        }
        return StatusCode(500, "Error cleaning data");
    }

    // [HttpPost("uploadFile")]
    // [ProducesResponseType(StatusCodes.Status204NoContent)]
    // [ProducesResponseType(StatusCodes.Status400BadRequest)]
    // public async Task<IActionResult> UploadFileAsync()
    // {
    //     if (!Request.HasFormContentType)
    //     {
    //         return BadRequest();
    //     }
    //     try
    //     {
    //         var formCollection = await Request.ReadFormAsync();

    //         var iFormFile = formCollection.Files["fileContent"];

    //         if (iFormFile is null || iFormFile.Length == 0)
    //         {
    //             return BadRequest();
    //         }

    //         using var stream = iFormFile.OpenReadStream();

    //         var localFilePath = Path.Combine("Files", iFormFile.FileName);

    //         using var localFileStream = System.IO.File.OpenWrite(localFilePath);

    //         await stream.CopyToAsync(localFileStream);

    //         return NoContent();
    //     }
    //     catch (Exception ex)
    //     {
    //         _logger.LogError(ex, "An error occurred while uploading the file.");
    //         return BadRequest("An error occurred while uploading the file.");
    //     }
    // }
}
