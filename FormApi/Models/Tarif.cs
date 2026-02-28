using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace FormApi.Models;

public class Tarif //тарифы работы
{
    public Guid Id { get; set; } //код тарифа работы

    public string Name { get; set; } //наименование тарифа

    public string Description { get; set; } //описание тарифа

    public int Price { get; set; } //стоимость тарифа
}
