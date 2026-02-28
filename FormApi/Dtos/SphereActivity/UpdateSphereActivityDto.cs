using System.ComponentModel.DataAnnotations;

namespace FormApi.Dtos.SphereActivity
{
    public class UpdateSphereActivityDto
    {
        [Required]
        public string NameSphere { get; set; } = null!;
    }
}