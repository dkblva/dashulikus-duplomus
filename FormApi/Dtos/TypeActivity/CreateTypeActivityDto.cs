using FormApi.Models;
using System.ComponentModel.DataAnnotations;
namespace FormApi.Dtos.TypeActivity
{
    public class CreateTypeActivityDto
    {
        [Required]
    public string NameType { get; set; } = null!; //наименование
    }
}
