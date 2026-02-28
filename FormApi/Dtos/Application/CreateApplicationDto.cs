using FormApi.Models;
using System.ComponentModel.DataAnnotations;

namespace FormApi.Dtos.Application;

public class CreateApplicationDto
{
    [Required]
    public string FullName { get; set; } = null!;

    [Required]
    public string PhoneNumber { get; set; } = null!; // номер телефона клиента
    public string Email { get; set; } = null!; //эл.почта клиента
    public string OrganizationName { get; set; } = null!; //наименование организации клиента
    public Guid SphereId { get; set; } //сфера деятельности организации
    public Guid TypeId { get; set; } //вид деятельности организации
    public Boolean Status { get; set; } // статус заявки
    public DateTime Created { get; set; } = DateTime.Now; //дата создания заявки
    public string? Comment { get; set; } //комментарий (optional)
}