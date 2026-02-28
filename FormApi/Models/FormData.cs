using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace FormApi.Models;

public class FormData //форма заявки
{
    public Guid Id { get; set; }
    public required string Name { get; set; }
    public required string Phone { get; set; }
}
