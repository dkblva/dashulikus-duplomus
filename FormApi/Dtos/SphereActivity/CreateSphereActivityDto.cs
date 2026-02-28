using FormApi.Models;
using System.ComponentModel.DataAnnotations;
namespace FormApi.Dtos.SphereActivity
{
    public class CreateSphereActivityDto
    {
        [Required]
    public string NameSphere { get; set; } = null!; //наименование
    }
}
