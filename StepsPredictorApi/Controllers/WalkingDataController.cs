using Microsoft.AspNetCore.Mvc;
using System.Text;
using System.Text.Json;

[ApiController]
[Microsoft.AspNetCore.Mvc.Route("[controller]")]
public class WalkingDataController : ControllerBase
{
    private readonly HttpClient _client;
    public WalkingDataController(HttpClient client)
    {
        _client = client;
    }

    [HttpPost("upload")]
    public async Task<IActionResult> UploadWalkingData([FromBody] JsonElement rawData)
    {
        var jsonData = JsonSerializer.Serialize(rawData);
        var content = new StringContent(jsonData, Encoding.UTF8, "application/json");
        var response = await _client.PostAsync("http://localhost:5001/clean-data", content);

        if (response.IsSuccessStatusCode)
        {
            var cleanedData = await response.Content.ReadAsStringAsync();

            return Ok(cleanedData);
        }
        return StatusCode(500, "Error cleaning data");
    }
}
