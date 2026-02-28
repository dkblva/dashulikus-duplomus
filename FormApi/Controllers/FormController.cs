using Microsoft.AspNetCore.Mvc;
using System.Text;
using System.Text.Json;
using FormApi.Models;

namespace FormApi.Controllers;

[ApiController]
[Route("api/forms")]
public class FormController : ControllerBase
{
    [HttpPost]
    public async Task<IActionResult> Post([FromBody] FormData data)
    {
        try
        {
            using var client = new HttpClient();

            var json = JsonSerializer.Serialize(
                data,
                new JsonSerializerOptions
                {
                    PropertyNamingPolicy = JsonNamingPolicy.CamelCase
                }
            );

            var content = new StringContent(json, Encoding.UTF8, "application/json");

            var response = await client.PostAsync("http://127.0.0.1:8000/send", content);

            var result = await response.Content.ReadAsStringAsync();
            Console.WriteLine("Ответ от Python: " + result);

            return Ok(new { status = "sent_to_telegram" });
        }
        catch (Exception ex)
        {
            Console.WriteLine("Ошибка: " + ex.Message);
            return StatusCode(500, ex.Message);
        }
    }
}
