using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

using System.Security.Policy;

namespace FormApi.Models
{
    public class Solution //решение по заявке
    {
        public Guid Id { get; set; } //код решения
        public string Description { get; set; } //описание решения
        public Guid IdApplication { get; set; } //код заявки
        public Guid IdTarif { get; set; } //код тарифа работы


        public Tarif Tarif { get; set; }
        public Application Application { get; set; }
    }
}
