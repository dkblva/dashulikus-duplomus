using FormApi.Models;
using System.ComponentModel.DataAnnotations;

namespace FormApi.Dtos.Solution
{
    public class UpdateSolutionDto
    {
        [Required]
        [StringLength(1000)]
        public string? Description { get; set; } //описание решения

        [Required]
        public Guid IdApplication { get; set; } //код заявки

        [Required]
        public Guid IdTarif { get; set; } //код тарифа работы
    }
}
