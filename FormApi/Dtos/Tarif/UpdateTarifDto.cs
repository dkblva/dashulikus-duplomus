using System.ComponentModel.DataAnnotations;

namespace FormApi.Dtos.Tarif
{
    public class UpdateTarifDto
    {
        [Required]
        [StringLength(100, MinimumLength = 2, ErrorMessage = "Name must be between 2 and 100 characters.")]
        public string Name { get; set; } = null!;

        [StringLength(1000, ErrorMessage = "Description can't be longer than 1000 characters.")]
        public string Description { get; set; } = string.Empty;

        [Required]
        [Range(0, int.MaxValue, ErrorMessage = "Price must be a non-negative integer.")]
        public int Price { get; set; }
    }
}