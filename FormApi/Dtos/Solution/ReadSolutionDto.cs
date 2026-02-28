using FormApi.Models;
using System.ComponentModel.DataAnnotations;

namespace FormApi.Dtos.Solution
{
    public class ReadSolutionDto
    {
        public Guid Id { get; set; } //код решения
        public string? Description { get; set; } //описание решения

        public Guid IdApplication { get; set; } //код заявки

        public Guid IdTarif { get; set; } //код тарифа работы
    }
}
