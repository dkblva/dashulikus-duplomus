using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace FormApi.Models;

public class Application //заявки основная рабочая таблица
{
    public Guid Id { get; set; } //код заявки

    [Required(ErrorMessage = "ФИО обязательно для заполнения")]
    public string FullName { get; set; } = null!; //ФИО клиента
    public string? PhoneNumber { get; set; } // номер телефона клиента
    public string? Email { get; set; } //эл.почта клиента
    public string? OrganizationName { get; set; } //наименование организации клиента
    public Guid? SphereId { get; set; } //сфера деятельности организации
    public Guid? TypeId { get; set; } //вид деятельности организации
    public Boolean? Status { get; set; } // статус заявки
    public DateTime? Created { get; set; } = DateTime.Now; //дата создания заявки
    public string? Comment { get; set; } //комментарий

    
    public SphereActivity? SphereActivity { get; set; }
    public TypeActivity? TypeActivity { get; set; }
}
