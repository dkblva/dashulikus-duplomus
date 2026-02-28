using System.ComponentModel.DataAnnotations;

namespace FormApi.Dtos.TypeActivity
{
    public class UpdateTypeActivityDto
    {
        [Required]
        public string NameType { get; set; } = null!;
    }
}